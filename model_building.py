#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 19:18:19 2023

@author: obinnadinneya
"""

import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv('eda_data.csv')
df.columns


#choose relevant columns (without Age_years because of the missing values)
df_model = df[['Salary','company_size', 'company_type', 'company_sector','company_industry','company_revenue',
                'company_text', 'State','python_yn','spark_yn', 'excel_yn', 
                'aws_yn', 'SAS_yn', 'job_simp','seniority', 'des_length']]

#create a dummy dataframe
df_dum = pd.get_dummies(df_model)


#TRAIN TEST SPLIT
X = df_dum.drop(columns='Salary')
y = df_dum.Salary
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#LINEAR REGERESSION IN STATS MODEL VS SKLEARN
import statsmodels.api as sm

X_train_with_intercept = sm.add_constant(X_train)
model = sm.OLS(y_train, X_train_with_intercept)
model.fit().summary()


#SKLEARN
from sklearn.linear_model import LinearRegression,Lasso
from sklearn.model_selection import cross_val_score

lmodel = LinearRegression()
lmodel.fit(X_train,y_train)

#CROSS VALIDATION
np.mean(cross_val_score(lmodel, X_train,y_train, scoring='neg_mean_absolute_error'))




#lasso regression
#works well for a case of a very sparse matrix due to dummy varibles and helps to normalize values

lm_l = Lasso()
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l, X_train,y_train, scoring='neg_mean_absolute_error'))

#tuning the model for best alpha parameter
alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lm_l, X_train,y_train, scoring='neg_mean_absolute_error')))
    
plt.plot(alpha,error)

err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]



#randomn randomn forrest
from sklearn.ensemble import RandomForestClassifier
rfc =RandomForestClassifier()

np.mean(cross_val_score(rfc, X_train,y_train, scoring='neg_mean_absolute_error'))

#Use grid search to tune this 
from sklearn.model_selection import GridSearchCV


#We will do a randomized gridsearch
from sklearn.model_selection import RandomizedSearchCV
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt', 'log2']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
print(random_grid)

rf_random = RandomizedSearchCV(rfc,param_distributions = random_grid, n_iter = 100, cv = 5, verbose=2, n_jobs= -1, scoring='neg_mean_absolute_error')
# Fit the random search model
rf_random.fit(X_train,y_train)

#Best estimator and score (slight improvement)
rf_random.best_estimator_
rf_random.best_score_


#LETS WORK ON TEST SET DATA NOW FOR EACH MODEL

#PREDICTIONS
tpred_lm = lmodel.predict(X_test)
tpred_lm_l = lm_l.predict(X_test)
tpred_rfc = rf_random.predict(X_test)


pred_dict = {'tpred_lm' : tpred_lm,'tpred_lm_l': tpred_lm_l,'tpred_rfc':tpred_rfc}

#MEAN ABSOLUTE ERROR
from sklearn import metrics
for i in pred_dict:
    MAE = metrics.mean_absolute_error(y_test,pred_dict[i])
    MSE = metrics.mean_squared_error(y_test,pred_dict[i])
    RMSE = np.sqrt(MSE)
    R2 = metrics.r2_score(y_test,pred_dict[i])
    
    print(f"Results for {i}")
    print(f'MAE: {MAE}')
    print(f'MSE: {MSE}')
    print(f'RMSE: {RMSE}')
    print(f'R^2: {R2}')
    print('\n')
    
#all models look pretty good at predicting Salary

#Combining Models to see if it performs better
MAE = metrics.mean_absolute_error(y_test,((tpred_lm+tpred_rfc)/2))
MSE = metrics.mean_squared_error(y_test,((tpred_lm+tpred_rfc)/2))
RMSE = np.sqrt(MSE)
R2 = metrics.r2_score(y_test,((tpred_lm+tpred_rfc)/2))
print("Results for tpred_lm+tpred_rfc")
print(f'MAE: {MAE}')
print(f'MSE: {MSE}')
print(f'RMSE: {RMSE}')
print(f'R^2: {R2}')

#Better Rsquared value error is stilll around $2600










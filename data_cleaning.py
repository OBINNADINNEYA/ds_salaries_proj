#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:08:48 2023

@author: obinnadinneya
"""

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 

df = pd.read_csv('Data scientist.csv')

#salary estimate
#remove rows with no salary estimates
df = df.dropna(subset=['salary estimate'])
salary = df['salary estimate'].apply(lambda x : x.split('/')[0])
salary
minus_cd = salary.apply(lambda x : x.replace('$',"").replace(",",""))
df['Salary'] = minus_cd
df.info()

#company reviews 
import re
ratings = df['company'].apply(lambda x: x.split()[-1])
pattern = r'^(?![0-9]+\.[0-9]+$).*'
replacement = "-1"
ratings = [re.sub(pattern, replacement, item) for item in ratings]
df['company_rating'] = ratings
df['company_rating'] = df['company_rating'].apply(lambda x : x.replace(' ',""))
df['company_rating'] = df['company_rating'].astype(float)

#company age
df['age'] = df['company_founded'].apply(lambda x : 2023 - x if x != -1 else x )


#company name 
df['company_text'] = df.apply(lambda x: x['company'] if x['company_rating'] < 0 else x['company'][:-3], axis = 1)


#state of company
df['State'] = df['location'].apply(lambda x : x.split(',')[-1])
df['State'] = df['State'].apply(lambda x : 'CA' if x == 'California' else x)
df['State'].value_counts()


#parsing of job description for python, rstudio, SAS, excel  
df['python_yn'] = df['job description'].apply(lambda x : 1 if 'pyhton' in x.lower() else 0)
df['python_yn'].value_counts()

df['python_yn'] = df['job description'].apply(lambda x : 1 if 'python' in x.lower() else 0)
df['python_yn'].value_counts()
df['Rstudio_yn'] = df['job description'].apply(lambda x : 1 if 'r studio' in x.lower() else 0)
df['Rstudio_yn'].value_counts()

df['Rstudio_yn'] = df['job description'].apply(lambda x : 1 if ' R ' in x.lower() else 0)
df['Rstudio_yn'].value_counts()

df['spark_yn'] = df['job description'].apply(lambda x : 1 if 'spark' in x.lower() else 0)
df['spark_yn'].value_counts()

df['excel_yn'] = df['job description'].apply(lambda x : 1 if 'excel' in x.lower() else 0)
df['excel_yn'].value_counts()

df['aws_yn'] = df['job description'].apply(lambda x : 1 if 'aws' in x.lower() else 0)
df['aws_yn'].value_counts()

df['SAS_yn'] = df['job description'].apply(lambda x : 1 if 'sas' in x.lower() else 0)
df['SAS_yn'].value_counts()




#Drop first column
df_out = df.drop(columns='Unnamed: 0', axis =1)
df_out



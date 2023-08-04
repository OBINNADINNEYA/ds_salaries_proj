#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 08:43:23 2023

@author: obinnadinneya
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd


path = '/Users/obinnadinneya/Desktop/OBI_PORTFOLIO/ds_salary_proj/chromedriver'
service = Service(path)
options = Options()
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)

l=list()
o={}

target_url ="https://api.scrapingdog.com/scrape?api_key=64cb93b2a017b719c0114c4b&url=https://www.glassdoor.com/Job/toronto-python-jobs-SRCH_IL.0,7_IC2281069_KO8,14.htm&dynamic=false"


driver.get(target_url)

driver.maximize_window()
time.sleep(2)

resp = driver.page_source
driver.close()

soup=BeautifulSoup(resp,'html.parser')

allJobsContainer = soup.find("ul",{"class":"css-7ry9k1"})

allJobs = allJobsContainer.find_all("li")

for job in allJobs:
    try:
        o["name-of-company"]=job.find("div",{"class":"d-flex justify-content-between align-items-start"}).text
    except:
        o["name-of-company"]=None

    try:
        o["name-of-job"]=job.find("a",{"class":"jobLink css-1rd3saf eigr9kq2"}).text
    except:
        o["name-of-job"]=None

    try:
        o["location"]=job.find("div",{"class":"d-flex flex-wrap css-11d3uq0 e1rrn5ka2"}).text
    except:
        o["location"]=None

    try:
        o["salary"]=job.find("div",{"class":"css-3g3psg pr-xxsm"}).text
    except:
        o["salary"]=None

    l.append(o)

    o={}

print(l)

df = pd.DataFrame(l)
df.to_csv('jobs.csv', index=False, encoding='utf-8')
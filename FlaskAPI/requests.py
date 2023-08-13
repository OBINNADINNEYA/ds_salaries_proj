#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 16:00:57 2023

@author: obinnadinneya
"""

import requests
from data_input import data_in

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Type" : "application/json"}
#send input data as a json file 
data = {'input' : data_in}

r = requests.get(URL,headers=headers, json=data)


r.json()
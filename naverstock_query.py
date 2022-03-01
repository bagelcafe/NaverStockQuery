from email.mime import base
import pandas as pd
import numpy as np
import requests
import re
import bs4
from bs4 import BeautifulSoup
import time
import urllib.request as req
import sys
import io
import csv
import os
from selenium import webdriver
import ast

start_time = time.time()

file='KOSPI200_sise_0301.csv'

with open(file, newline='', encoding='utf-8-sig') as f:
    reader=csv.reader(f)
    kospi200_list = list(reader)

#print(kospi200_list)

# Search cash value
def search_corp_cash(corp_code):
    url = f"https://navercomp.wisereport.co.kr/v2/company/c1030001.aspx?cmp_cd={corp_code}&cn="
    response = requests.get(url).text.encode('utf-8')
    response = bs4.BeautifulSoup(response, 'html.parser')

    options = webdriver.ChromeOptions()
    options.add_argument("headless") # 크롬 창이 보이지 않게
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome('G:\My Documents\chromedriver.exe', options=options)
    driver.implicitly_wait(1000)
    driver.get(url)

    button = driver.find_element_by_xpath('/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/table[2]/tbody/tr/td[3]/a')
    button.click()

    response = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    try:
        for line in response.find('table', {'class': 'gHead01 all-width data-list'}).findAll('th')[:6]:
            if line.find('div'):
                print(line.find('div').find(text=True, recursive=False), end=' ')
            else:
                print(line.text, end=' ')

        print()

        text ='0'
        for line in response.findAll('tr', {'class':'lvl3'}):
            data = line.findAll('td')
            if '현금및' in data[0].text:
                #for col in data[:-2]:
                col = data[5]
                text = str(col.text).strip()
                print(text, end=' ')
        
        if text == '0':
            text = search_corp_cash(corp_code)
            print(text, end=' ')

    except:
        print("AttributeError")
        text="AttributeError"

    print("OK")
    driver.quit()
    time.sleep(5)
    
    return text

kospi200_cash = list()
cash_list = list()

for code, name, sise in kospi200_list:
    print("code=", code)
    cash = search_corp_cash(code)
    data = code,name,sise,cash
    kospi200_cash.append(data)

    cash = cash.replace(",", "")
    sise = sise.replace(",", "")
    
    if cash =='':
        cash = search_corp_cash(code)

    print(cash)

    if cash =="":
        cash='0'
        
    int_cash= float(cash)
    int_sise = float(sise)

    if int_cash > int_sise:
        cash_list.append(data)


#print("Kospi 200 Sise and Cash=", kospi200_cash)
with open ('KOSPI200_sise_cash_0301.csv', 'w', newline='', encoding='utf-8-sig') as f: ## with 블록안에서 open, 블록밖에서 자동으로 close.
    writer = csv.writer(f)
    writer.writerows(kospi200_cash)

with open ('KOSPI200_final_cash_0301.csv', 'w', newline='', encoding='utf-8-sig') as f: ## with 블록안에서 open, 블록밖에서 자동으로 close.
    writer = csv.writer(f)
    writer.writerows(cash_list)

#BaseUrl = 'http://finance.naver.com/sise/entryJongmok.nhn?&page='

#target = response.find('table', {'id':'faaFVlanREZS', 'class':'haFVlanREZS gHead01 all-width data-list'})
#print(target)

#find_by_id=response.find_all('div',{'class':'class1'})
'''
result= response.find('div', id='faaFVlanREZS')
table=response.find('table',{'class':'gHead01 all-width data-list'})
table_class=response.select('table class')
'''

"""
<table class="haFVlanREZS gHead01 all-width data-list" summary="IFRS연결 연간 재무 정보를 제공합니다."><caption class="blind">"재무분석 리스트"</caption><thead><tr><th>9191</th><th>9191</th><th>9191</th><th>9191</th><th>9191</th><th>9191</th><th>9191</th></tr></thead><tbody><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr><tr style="display: none;"><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td><td>9,191</td></tr></tbody></table>
BeautifulSoup

with open ('KOSPI200.csv', 'w', newline='',encoding='utf-8-sig') as f: ## with 블록안에서 open, 블록밖에서 자동으로 close.
    writer = csv.writer(f)
    writer.writerows(kospi200_list)
"""

#print(kospi200_list)
"""
with open ('KOSPI200_sise.csv', 'w', newline='', encoding='utf-8-sig') as f: ## with 블록안에서 open, 블록밖에서 자동으로 close.
    writer = csv.writer(f)
    writer.writerows(kospi200_sise_list)
"""

end_time=time.time()
print("Running time=", (end_time-start_time)/60)

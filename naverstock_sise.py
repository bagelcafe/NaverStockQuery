from email.mime import base
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import time
import urllib.request as req
import sys
import io
import csv
import os

start_time = time.time()

file='KOSPI_sise_0225.csv'

with open(file, newline='', encoding="utf-8") as f:
    reader=csv.reader(f)
    new_item_list = list(reader)

print(new_item_list)
#new_df = pd.DataFrame(new_item_list, columns_name)
#print(new_df['kospi_name'])

code = '005930'
URL = f"https://finance.naver.com/item/main.nhn?code={code}"
r = requests.get(URL)
df2 = pd.read_html(r.text)[3]
#print(df2)

BaseUrl = 'http://finance.naver.com/sise/entryJongmok.nhn?&page='
kospi200_list = list()

for i in range(1, 21):
    url = BaseUrl + str(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    items = soup.find_all('td', {'class': 'ctg'})

    for item in items:
        print(item)
        txt = item.a.get('href') # https://finance.naver.com/item/main.nhn?code=006390
        k = re.search('[\d]+', txt) ##정규표현식 사용. [\d] 숫자표현, + : 반복
        if k:
            code = k.group()
            name = item.text
            data = code, name
            #print(data)
            kospi200_list.append(data)


with open ('KOSPI200.csv', 'w', newline='',encoding='utf-8-sig') as f: ## with 블록안에서 open, 블록밖에서 자동으로 close.
    writer = csv.writer(f)
    writer.writerows(kospi200_list)

kospi200_sise_list = list()
for code, name in kospi200_list:
    for no, kospi_name,sise in new_item_list:
        if name == kospi_name:
            data = code, name, sise
            kospi200_sise_list.append(data)

#print(kospi200_sise_list)
with open ('KOSPI200_sise_0225.csv', 'w', newline='', encoding='utf-8-sig') as f: ## with 블록안에서 open, 블록밖에서 자동으로 close.
    writer = csv.writer(f)
    writer.writerows(kospi200_sise_list)
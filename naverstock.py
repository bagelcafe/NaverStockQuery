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
sosoks = ['0','1']
item_code_list =[]

def return_value(address, i=0):    
    res = requests.get(address)
    soup = BeautifulSoup(res.content.decode('euc-kr','replace'),'html.parser')
    
    section = soup.find('tbody')
    items= section.find_all('tr', onmouseover="mouseOver(this)")
    for item in items :
        i=i+1
        basic_info = item.get_text()
        sinfo = basic_info.split("\n")
        print(i,sinfo)
        
        #if i==4 or i ==14 or i==12 or i==26 or i==28 or i==35 or i==38 or i==48:
        #    print("\t" + sinfo[1] +"\t\t"+sinfo[2]+"\t\t\t"+sinfo[15]+" "+sinfo[16])
        #    item_roe = sinfo[16]
        #else:
        #    print("\t" + sinfo[1] +"\t\t"+sinfo[2]+"\t\t\t"+sinfo[15]+" "+sinfo[20])
        #    item_roe = sinfo[20]
            
        item_code= sinfo[1]
        item_name= sinfo[2]
        item_total= sinfo[15]
        
        result=item_code,item_name,item_total
        item_code_list.append(result)
        time.sleep(8) # 20번째마다 랜덤하게 2~4초정도 쉬어주기

baseaddress='https://finance.naver.com/sise/sise_market_sum.naver?&page='
for i in range(1,10):
    return_value(baseaddress+str(i))
    
df = pd.DataFrame(item_code_list)
df.columns=['item_code','item_name', 'item_total']
print(df)

with open ('KOSPI_sise_0225.csv', 'w', newline='', encoding='utf-8') as f1: ## with 블록안에서 open, 블록밖에서 자동으로 close.
    writer = csv.writer(f1)
    writer.writerows(item_code_list)
import requests
from bs4 import BeautifulSoup
import pandas as pd

TTB_Key = 'ttbkjw12431355001'
Title = '혼자 공부하는 파이썬 - 1:1 과외하듯 배우는 프로그래밍 자습서, 개정판'
URL = f'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={TTB_Key}&Query={Title}&QueryType=Title&MaxResults=3&start=1&SearchTarget=Book&output=xml&Version=20131101'

# API로 데이터 불러오기
rq = requests.get(URL)
soup = BeautifulSoup(rq.text, 'xml')



for item in soup.find_all('item'):
    isbn = item.find('isbn').text
    title = item.find('title').text
    price = item.find('priceSales').text
print(isbn)
print(title)
print(price)



URL2 = f'http://www.aladin.co.kr/ttb/api/ItemOffStoreList.aspx?ttbkey={TTB_Key}&itemIdType=ISBN&ItemId={isbn}&output=xml'
rq2 = requests.get(URL2)
soup = BeautifulSoup(rq2.text, 'xml')

offStoreInfo_elements = soup.find_all('offStoreInfo')

for offStoreInfo in offStoreInfo_elements:
    offCode = offStoreInfo.find('offCode').text
    offName = offStoreInfo.find('offName').text
    link = offStoreInfo.find('link').text
            
print(offCode)
print(offName)
print(link)
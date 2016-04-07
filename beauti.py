# -- coding: utf-8 --
import csv
import io
import urllib
import requests
import sys
import urllib.request
from bs4 import BeautifulSoup
import urllib
import codecs
import time
import json
import base64
from time import sleep
from gunicorn.http.errors
#url="http://www.twse.com.tw/ch/trading/fund/BFI82U/BFI82U_print.php?begin_date=20160330&end_date=20160329&report_type=day&language=ch&save=csv"
#url="http://finance.yahoo.com/d/quotes.csv?s=^TWII&f=l1"
#while(True):
#    CSVReader = csv.reader(io.TextIOWrapper(urllib.request.urlopen(url)))
#    for row in CSVReader:
#         print(row)
#         sleep(2)
#LimitRequestLine

first = requests.get('http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php')
first.encoding = 'big5'
soup = BeautifulSoup(first.text,"html.parser")

a={}

for hey in soup.select('input'):
    if 'hidden' in hey.get('type'):
        if hey.get('name') =='html':
            print(hey.get('name'))
       #print(hey.get('value'))
            a[hey.get('name')] = base64.b64encode(hey.get('value').encode('utf-8'))
        elif hey.get('name')=='dirname':
            a[hey.get('name')] ='BWIBBU_d20160407'

data=a
print(data)
res2 = requests.post('http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_print.php?language=ch&save=csv',params=a,stream=True)
TodayFeatureResponse = urllib.request.urlopen(res2.url)
#for row in csv.reader(io.TextIOWrapper(TodayFeatureResponse)):
for row in csv.reader(codecs.iterdecode(TodayFeatureResponse,"Latin-1")):
    print(row)

print("========================================================================")
TodayFeature={  #setting the post query data
              'syear':'2016',
              'smonth':'4',
              'sday':'1',
              'eyear':'2016',
              'emonth':'4',
              'eday':'1'
         #       'DATA_DATE':'2016/4/1',
         #       'DATA_DATE1':'2016/4/1',
         #       'DATA_DATE_Y':'2016',
         #       'DATA_DATE_M':'4',
         #       'DATA_DATE_D':'1',
         #       'DATA_DATE_Y1':'2016',
         #       'DATA_DATE_M1':'4',
         #       'DATA_DATE_D1':'1',
         #       'syear':'2016',
         #       'smonth':'4',
         #       'sday':'1',
         #       'eyear':'2016',
         #       'emonth':'4',
         #       'eday':'1',
         #       'datestart':"2016/4/1",
         #       'dateend':'2016/4/1'
        }
FeatureRequest= requests.post('http://www.taifex.com.tw/chinese/3/7_12_8dl.asp',data=TodayFeature,allow_redirects=False)
print(FeatureRequest.headers['Location'])
URLRedirect = "http://www.taifex.com.tw"+FeatureRequest.headers['Location']
RealCSVFile = requests.get(URLRedirect)
print(RealCSVFile.url)

TodayFeatureResponse = urllib.request.urlopen(RealCSVFile.url)
#for row in csv.reader(io.TextIOWrapper(TodayFeatureResponse)):
for row in csv.reader(codecs.iterdecode(TodayFeatureResponse,"Latin-1")):
    print(row)


# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Parameter Define
# = = = = = = = = = = = = = = = = = = = = = = = = = = =
stocks  = ['2881',
        '2882',
        '0050']

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Function
# = = = = = = = = = = = = = = = = = = = = = = = = = = =
def getStockInfo(quote):
    req = requests.session()
    req.get('http://mis.twse.com.tw/stock/index.jsp',headers = {'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'})
    #response = req.get('http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={}&json=1&delay=0&_{}'.format(quote,int(time.time()*1000)))
    response = req.get('http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={}'.format(quote))
    print(response.url)
    jstr = json.loads(response.text)
    return jstr

def displayStockInfo(jobj):
    for i in range(0, 3, 1):
        print("%s %s %.2f %.2f %.2f " % (jobj['msgArray'][i]['ch'] , jobj['msgArray'][i]['n'] , float(jobj['msgArray'][i]['y']), float(jobj['msgArray'][i]['pz']), (float(jobj['msgArray'][i]['pz']) - float(jobj['msgArray'][i]['y']))))

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# mian function
# = = = = = = = = = = = = = = = = = = = = = = = = = = =
if __name__ == '__main__':
    url = '|'.join(['tse_%s.tw' % (stocks[n]) for n in range(len(stocks))])

    data = getStockInfo(url)
    displayStockInfo(data)

urla ="http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_2881.tw"
hi= requests.session()
hi.get('http://mis.twse.com.tw/stock/index.jsp',headers = {'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'})
test = hi.get(urla)
jastr = json.loads(test.text)
print(jastr['msgArray'][0]['v'])
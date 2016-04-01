# coding=utf-8
import csv
import io
import urllib
import requests
import sys
import urllib.request
from bs4 import BeautifulSoup
import urllib
from time import sleep
#url="http://www.twse.com.tw/ch/trading/fund/BFI82U/BFI82U_print.php?begin_date=20160330&end_date=20160329&report_type=day&language=ch&save=csv"
#url="http://finance.yahoo.com/d/quotes.csv?s=^TWII&f=l1"
#while(True):
#    CSVReader = csv.reader(io.TextIOWrapper(urllib.request.urlopen(url)))
#    for row in CSVReader:
#         print(row)
#         sleep(2)


import requests
import time
import json



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
# coding=utf-8
import csv
import io
import urllib
import requests
import sys
import urllib.request
from bs4 import BeautifulSoup
import urllib
import chardet
from time import sleep
url="http://www.twse.com.tw/ch/trading/fund/BFI82U/BFI82U_print.php?begin_date=20160330&end_date=20160329&report_type=day&language=ch&save=csv"
#url="http://finance.yahoo.com/d/quotes.csv?s=^TWII&f=l1"
while(True):
    CSVReader = csv.reader(io.TextIOWrapper(urllib.request.urlopen(url)))
    for row in CSVReader:
         print(row)
        # sleep(2)
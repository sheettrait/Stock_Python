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
r = urllib.request.urlopen('http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php')
#print(chardet.detect(r.read()))
soup = BeautifulSoup(r, "html.parser")


#print(soup.select('.basic2')[12].text.decode('unicode-escape'))
print(soup.select('.basic2')[1].text)
print(soup.select('.basic2')[2].text)
print(soup.select('.basic2')[3].text)
print(soup.select('.basic2')[4].text)
print(soup.select('.basic2')[5].text)
print(soup.select('.basic2')[6].text)
print(soup.select('.basic2')[7].text)
print(soup.select('.basic2')[8].text)
print(soup.select('.basic2')[9].text)
print(soup.select('.basic2')[10].text)
print(soup.select('.basic2')[11].text)
#for x in range(soup.select('.basic2').__len__()):
#    if x%4 != 0:
#        print(soup.select('.basic2')[x].text)
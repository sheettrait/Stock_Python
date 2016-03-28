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
print(soup.select('.basic2')[11].text)
print(soup.select('.basic2')[12].text)
print(soup.select('.basic2')[13].text)
print(soup.select('.basic2')[14].text)
print(soup.select('.basic2')[15].text)
print(soup.select('.basic2')[16].text)
print(soup.select('.basic2')[17].text)
print(soup.select('.basic2')[18].text)
print(soup.select('.basic2')[19].text)
print(soup.select('.basic2')[20].text)
print(soup.select('.basic2')[21].text)
#for x in range(soup.select('.basic2').__len__()):
#    if x%4 != 0:
#        print(soup.select('.basic2')[x].text)
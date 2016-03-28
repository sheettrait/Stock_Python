# coding=utf-8
import io
import urllib
import requests
import sys
import urllib.request
from bs4 import BeautifulSoup
from yahoo_finance import Share
import urllib

class GetData():
    def __init__(self):
        self.Responese = urllib.request.urlopen('http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php')
        self.soup = BeautifulSoup(self.Responese,"html.parser")
        print("2323")
        for x in range(self.soup.select('.basic2').__len__()):
            if x > 5 and ((x%5)!=2):
                print(self.soup.select('.basic2')[x].text)
    #def GripData(self):
        
a = GetData()
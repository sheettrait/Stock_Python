# coding=utf-8
import csv
import io
import urllib
import requests
import sys
import urllib.request
import tkinter
import datetime
import threading
import json
import codecs
from bs4 import BeautifulSoup
from yahoo_finance import Share
import urllib
from pip._vendor.distlib.compat import raw_input
from tkinter import Label, Entry, Frame
from tkinter.constants import INSERT
from time import sleep

while(True):
    url="http://mis.twse.com.tw/stock/data/futures_side.txt"   
    FeatureIntTimeResponse = requests.get(url)
    FeatureInfo=json.loads(FeatureIntTimeResponse.text)
    Stage=float(FeatureInfo['msgArray'][0]['h'])-float(FeatureInfo['msgArray'][0]['l'])
    PowerStage = int(float(FeatureInfo['msgArray'][0]['z'])+float(Stage*0.618))
    WeakStage = int(float(FeatureInfo['msgArray'][0]['z'])+float(Stage*0.382))
    print(WeakStage)
    print(PowerStage)
    print(FeatureInfo['msgArray'][0]['z'])
    sleep(3)
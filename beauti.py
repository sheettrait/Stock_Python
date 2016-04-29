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
from shutil import copyfileobj
from openpyxl import Workbook
from openpyxl import load_workbook

wb = load_workbook('20160429Detail.xlsx')
ws = wb.active

for row in ws.rows:
    print(row[3].value)
import json
import requests
from time import sleep
class Feature():
    def __init__(self):
        self.GetInfo()
        self.PowerStage=0
        self.PowerSatisfy=0
        self.MiddleStage=0
        self.WeakStage=0
        self.WeakSatisfy=0
        
    def GetInfo(self):
        while True:
            self.url="http://mis.twse.com.tw/stock/data/futures_side.txt"   
            self.Response = requests.get(self.url)
            self.Feature=json.loads(self.Response.text)
            print(self.Feature['msgArray'][0])
            difference = float(self.Feature['msgArray'][0]['h'])-float(self.Feature['msgArray'][0]['l'])
            self.MiddleStage = (float(self.Feature['msgArray'][0]['l'])+float(self.Feature['msgArray'][0]['h']))/2
            self.PowerStage = float(self.Feature['msgArray'][0]['l']) + difference*1.382
            self.PowerSatisfy = float(self.Feature['msgArray'][0]['l']) + difference*1.618
            self.WeakStage = float(self.Feature['msgArray'][0]['h']) - difference*1.382
            self.WeakSatisfy = float(self.Feature['msgArray'][0]['h']) - difference*1.618
            print("====================")
            print(self.PowerSatisfy)
            print(self.PowerStage)
            print(self.MiddleStage)
            print(self.WeakStage)
            print(self.WeakSatisfy)
            sleep(1)
        
a = Feature()
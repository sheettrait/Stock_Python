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


class InTimeData():
    def __init__(self):
        self.IntimeRquest = requests.session()
        self.IntimeRquest.get('http://mis.twse.com.tw/stock/index.jsp',headers = {'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'})
        self.IntimeStock=[]
        self.InTimeFeature=[]
        self.PowerStage=0
        self.WeakStage=0
                
    def GetInTimeStockInfo(self,StockNumber):
        url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_"+StockNumber.__str__()+".tw"
        IntimeResponse = self.IntimeRquest.get(url)
        StockInfo = json.loads(IntimeResponse.text)
        self.IntimeStock.append(StockInfo)
        print(StockInfo)
    
    def FeatureInTime(self):        #Get Feature Price In time 
        url="http://mis.twse.com.tw/stock/data/futures_side.txt"   
        FeatureIntTimeResponse = requests.get(url)
        FeatureInfo=json.loads(FeatureIntTimeResponse.text)
        Stage=float(FeatureInfo['msgArray'][0]['h'])-float(FeatureInfo['msgArray'][0]['l'])
        self.PowerStage = int(float(FeatureInfo['msgArray'][0]['z'])+float(Stage*0.618))
        self.WeakStage = int(float(FeatureInfo['msgArray'][0]['z'])+float(Stage*0.382))
        self.InTimeFeature.append(int(float(FeatureInfo['msgArray'][0]['z'])))
  #      self.InTimeFeature[0]= int(float(FeatureInfo['msgArray'][0]['y']))-int(float(FeatureInfo['msgArray'][0]['z']))
        self.InTimeFeature.append(int(float(FeatureInfo['msgArray'][0]['y']))-int(float(FeatureInfo['msgArray'][0]['z'])))  
        self.InTimeFeature.append(self.PowerStage)
        self.InTimeFeature.append(self.WeakStage)                   





class GetData():
    def __init__(self):
        self.Responese = urllib.request.urlopen('http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php')
        self.soup = BeautifulSoup(self.Responese,"html.parser")
        self.TargetPERatio = 0  # raw_input("Please input the PERatio")
        self.TargetEPS = 0      #raw_input("Please input the EPS")
        self.AllData=[]
        self.TrendThreeMen=[]
        self.HistoryData=[]
#####################
    def SearchPERatio(self):
        for x in range(8,503,5):
       # for x in range(8,self.soup.select('.basic2').__len__(),5):
            if self.soup.select('.basic2')[x].text != '-':
                if float(self.soup.select('.basic2')[x].text) <=float(self.TargetPERatio) :
                    QueryPrice = Share(self.soup.select('.basic2')[x-2].text+'.TW') #Query the API
        
                    if QueryPrice.get_earnings_share()!=None and float(QueryPrice.get_earnings_share())>=self.TargetEPS:                     # Get EPS
                        self.AllData.append(self.soup.select('.basic2')[x-2].text)  # StockNumber
                        self.AllData.append(QueryPrice.get_open())                  # Get FinalPrice
                        self.AllData.append(self.soup.select('.basic2')[x].text)    # Get PERatio
                        self.AllData.append(QueryPrice.get_earnings_share())

    def YahooAPI(self,StockNumber):
        TempURL = "http://finance.yahoo.com/d/quotes.csv?s="+StockNumber+".TW&f=gherl1n"
    
    def DayMoving(self,StockNumber):        #個股的平均線
        PrehistoryURL = "http://real-chart.finance.yahoo.com/table.csv?s="+StockNumber+".TW"
        CSVReader = csv.reader(io.TextIOWrapper(urllib.request.urlopen(PrehistoryURL)))
        self.HistoryData.append(StockNumber)
        Day=0
        MovingPrice=0
        for row in CSVReader:            #Moving Days 
            if row[6]=='Adj Close':
                print(row)
                continue
            Day = Day+1
            MovingPrice = float(row[6])+MovingPrice
            if Day==5:
                self.HistoryData.append(float(MovingPrice/5))
            elif Day==15:
                self.HistoryData.append(float(MovingPrice/15))
            elif Day==30:
                self.HistoryData.append(float(MovingPrice/30))
                break
        return self.HistoryData
     
    def ThreeMenDollar(self): #三大法人
        Today = datetime.datetime.now().strftime("%Y%m%d")
        url = "http://www.twse.com.tw/ch/trading/fund/BFI82U/BFI82U_print.php?begin_date="+Today+"&report_type=day&language=ch&save=csv" 
        self.ThreeMenResponse = urllib.request.urlopen(url)
        CSVReader = csv.reader(io.TextIOWrapper(urllib.request.urlopen(url)))
      #  for row in CSVReader:
      #      print(row)
    
    def FeatureToday(self): #期貨 http://www.taifex.com.tw/chinese/3/7_12_8.asp
        
   #     TodayFeature={  #setting the post query data
   #           'syear':datetime.datetime.now().strftime("%Y"),
   #           'smonth':datetime.datetime.now().strftime("%m"),
   #           'sday':datetime.datetime.now().strftime("%d"),
   #           'eyear':datetime.datetime.now().strftime("%Y"),
   #           'emonth':datetime.datetime.now().strftime("%m"),
   #           'eday':datetime.datetime.now().strftime("%d"),
   #     }
        TodayFeature={  #setting the post query data
              'syear':'2016',
              'smonth':'4',
              'sday':'1',
              'eyear':'2016',
              'emonth':'4',
              'eday':'1'
        }
        FeatureRequest= requests.post('http://www.taifex.com.tw/chinese/3/7_12_8dl.asp',data=TodayFeature,allow_redirects=False)
        URLRedirect = "http://www.taifex.com.tw"+FeatureRequest.headers['Location']
        RealCSVFile = requests.get(URLRedirect)
        print(RealCSVFile.history)
        self.TodayFeatureResponse = urllib.request.urlopen(RealCSVFile.url)
 #       for row in csv.reader(codecs.iterdecode(self.TodayFeatureResponse,"Latin-1")):
       #for row in csv.reader(io.TextIOWrapper(self.TodayFeatureResponse)):
  #          print(row)

class GUI(GetData):
    
    def __init__(self):
        super().__init__()
####################### initial interface #######################
        self.InTimeObject = InTimeData()
        self.InTimeObject.FeatureInTime()
        
       
        self.interface = tkinter.Tk()
        self.interface.title("HI")
        
        self.inputPERatio = Label()
        self.inputPERatio["text"]="Input Ratio"
        self.inputPERatio.grid(row=0,column=0)
        self.inputPREField = Entry(self.interface)
        self.inputPREField.bind('<Return>',self.GetTextFromPREField)
        self.inputPREField.grid(row=0,column=1)
        
        self.inputEPS = Label()
        self.inputEPS["text"]="Input EPS"
        self.inputEPS.grid(row=1,column=0)
        self.inputEPSField = Entry(self.interface)
        self.inputEPSField.bind('<Return>',self.GetTextFromEPSField)
        self.inputEPSField.grid(row=1,column=1)
        
        self.inputVolume = Label()
        self.inputVolume["text"]="Input Volume"
        self.inputVolume.grid(row=2,column=0)
        self.inputVolumeField = Entry(self.interface)
        self.inputVolumeField.bind('<Return>',self.GetTextFromEPSField)
        self.inputVolumeField.grid(row=2,column=1)
        
        self.inputWannaPrice = Label()
        self.inputWannaPrice["text"]="Input Close Price"
        self.inputWannaPrice.grid(row=3,column=0)
        self.inputWannaPriceField = Entry(self.interface)
        self.inputWannaPriceField.bind('<Return>',self.GetTextFromEPSField)
        self.inputWannaPriceField.grid(row=3,column=1)
         
        self.CheckButton = tkinter.Button(text="Enter")
        self.CheckButton.bind('<Button-1>',self.OutputData)
        self.CheckButton.grid(row=4)
        
      #  self.Feature = Label()
      #  self.Feature["text"] = "三大法人期貨"
      #  self.Feature.grid(row=0,column=4)
      #  self.FeatureField = tkinter.Text(height=10,width=80)
      #  self.FeatureField.grid(row=1,column=4)
        
        self.FutureBoxLabel=Label()
        self.FutureBoxLabel["text"]="三大法人期貨口數"
        self.FutureBoxLabel.grid(row=0,column=4)
        self.FutureBox = tkinter.Listbox()
        self.FutureBox.grid(row=1,column=4)
                
        
        self.Threemen = Label()
        self.Threemen["text"] = "三大法人"
        self.ThreemenBox=tkinter.Listbox()
        self.ThreemenBox.grid(row=10,column=10)
        
        self.Threemen.grid(row=3,column=4)
        self.ThreemenField = tkinter.Text(height=10,width=80)
        self.ThreemenField.grid(row=6,column=4)
        
        self.InTimeFeatureLabel = Label()
        self.InTimeFeatureLabel["text"]="台指現況"
        self.InTimeFeatureLabel.grid(row=0,column=8)
        self.InTimeFeatureLabelField = tkinter.Text(height=10,width=20)
        self.InTimeFeatureLabelField.grid(row=1,column=8)
        self.PrintInTimeFuture()
        self.FeatureToday()
        self.PrintFeautre()
        
        
#        self.PrintFeautre_thread = threading.Thread(target=self.PrintFeautre)
#        self.PrintFeautre_thread.start()
        
        self.ThreeMenDollar()
        self.PrintThreeMen()
     #   self.PrinThreeMenDollar_thread = threading.Thread(target=self.PrintThreeMen())
     #   self.PrinThreeMenDollar_thread.start()
####################### initial interface #######################        
        self.interface.mainloop()
        
        
    def PrintInTimeFuture(self):
        self.InTimeFeatureLabelField.insert(INSERT,self.InTimeObject.InTimeFeature)
        
    def PrintFeautre(self):
       # for row in csv.reader(io.TextIOWrapper(self.TodayFeatureResponse)):
       count=0
       for row in csv.reader(codecs.iterdecode(self.TodayFeatureResponse,"Latin-1")):
            self.FutureBox.insert(count+1,row[2]+"\t"+row[13])
            count =count+1
            if count==4:
                break
         #   self.FeatureField.insert(INSERT, row[1:4])    
            
    def PrintThreeMen(self):
        count =0
        for row in csv.reader(codecs.iterdecode(self.ThreeMenResponse,"Latin-1")):
            self.ThreemenBox.insert(count+1,row)
            #self.ThreemenField.insert(INSERT,row[1:2])
        
    def GetTextFromVolumeField(self,event):
        self.TargetPERatio = float(self.inputtVolumeField.get())
        
    def GetTextFromWannaPriceField(self,event):
        self.TargetPERatio = float(self.inputWannaPriceField.get())
        
    def GetTextFromPREField(self,event):
        self.TargetPERatio = float(self.inputPREField.get())
        
    def GetTextFromEPSField(self,event):
        self.TargetEPS=float(self.inputEPSField.get())
        self.SearchPERatio()
        
    def OutputData(self,event):
        for x in range(self.AllData.__len__()):     #Output the outcome 
            print(self.AllData[x])
        print(self.AllData.__len__())
        for x in range(int(self.AllData.__len__()/4)):
            for y in range(0,4,1):
                #tkinter.Text(self.interface,text='hello').grid(row=3+x,column=y)
               # self.guitext.insert(INSERT,"hello...").grid(row=3+x,column=y)
               
               self.temp = tkinter.Text(self.interface,height=3,width=3)
               self.temp.insert(INSERT,self.AllData[x*4+y])
               self.temp.grid(row=5+x,column=y)




b = GUI()
#a = InTimeData()
#a.FeatureInTime()
#a.Initial_LowHight()
#a.GetInTimeStockInfo(2330)
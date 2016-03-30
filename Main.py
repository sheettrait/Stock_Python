# coding=utf-8
import csv
import io
import urllib
import requests
import sys
import urllib.request
import tkinter
import datetime
from bs4 import BeautifulSoup
from yahoo_finance import Share
import urllib
from pip._vendor.distlib.compat import raw_input
from tkinter import Label, Entry
from tkinter.constants import INSERT, DISABLED
class GetData():
    def __init__(self):
        self.Responese = urllib.request.urlopen('http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php')
        self.soup = BeautifulSoup(self.Responese,"html.parser")
        self.TargetPERatio = 0  # raw_input("Please input the PERatio")
        self.TargetEPS = 0      #raw_input("Please input the EPS")
        self.AllData=[]
        self.TrendThreeMen=[]
        self.HistoryData=[]
    def SearchPERatio(self):
        for x in range(8,203,5):
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
        CSVReader = csv.reader(io.TextIOWrapper(urllib.request.urlopen(url)))
        for row in CSVReader:
            print(row)
    
    def FeatureToday(self): #期貨
        
        TodayFeature={  #setting the post query data
              'syear':datetime.datetime.now().strftime("%Y"),
              'smonth':datetime.datetime.now().strftime("%m"),
              'sday':datetime.datetime.now().strftime("%d"),
              'eyear':datetime.datetime.now().strftime("%Y"),
              'emonth':datetime.datetime.now().strftime("%m"),
              'eday':datetime.datetime.now().strftime("%d"),
        }

        FeatureRequest= requests.post('http://www.taifex.com.tw/chinese/3/7_12_6dl.asp',data=TodayFeature,allow_redirects=False)
        URLRedirect = "http://www.taifex.com.tw"+FeatureRequest.headers['Location']
        RealCSVFile = requests.get(URLRedirect)
        response = urllib.request.urlopen(RealCSVFile.url)
        for row in csv.reader(io.TextIOWrapper(response)):
    #for x in range(row.__len__()):
            print(row)
            
            
class GUI(GetData):
    
    def __init__(self):
        super().__init__()
####################### initial interface #######################
        self.interface = tkinter.Tk()
        self.interface.title("HI")
 #       self.newLabel=Label()
   #     self.guitext = tkinter.Text(self.interface,height=2,width=3)
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
        self.CheckButton = tkinter.Button(text="Enter")
        self.CheckButton.bind('<Button-1>',self.OutputData)
        self.CheckButton.grid(row=2)
        self.Threemen = Label()
        self.Threemen["text"] = "三大法人"
        self.Threemen.grid(row=0,column=4)
        self.ThreemenField = tkinter.Text()
        self.ThreemenField.grid(row=1,column=4)
####################### initial interface #######################        
    #    self.guitext.grid()
        self.interface.mainloop()
        
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
               tkinter.Label(self.interface,text=self.AllData[4*x+y]).grid(row=3+x,column=y)
    #    for r in range(self.AllData.__len__()%4):
    #        for c in range(4):
    #            tkinter.Text(self.interface,height=1,width=1,borderwidth=1).grid(row=3+r,column=c)

b = GUI()
b.FeatureToday()
b.ThreeMenDollar()
#b.DayMoving("2891")
#print(b.HistoryData)
#b.getihi()
#a = GetData()
#a.SearchPERatio()
#print(a.AllData)
#print("sss")
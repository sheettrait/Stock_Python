# coding=Big5
import json
import requests
import sqlite3
import os.path
import os 
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from time import sleep

class DataBase():
    
    def __init__(self):
        self.TodayDate = datetime.datetime.date(datetime.datetime.now()).__str__()+"-Data.db" 
        self.ResultToday = datetime.datetime.date(datetime.datetime.now()).__str__()+"-Result.db"
        self.CreateDataBase()
        self.BuyInformation=[0,0,0,0] # [0] = flag, [1] = price ,[2] postitve or negative
        self.Record=[]
       
    def CreateDataBase(self):
        if(os.path.isfile(self.TodayDate)==False):
            self.connection = sqlite3.connect(self.TodayDate)
            self.dbcommand = self.connection.cursor()
            self.dbcommand.execute("CREATE TABLE Futures(Date , Time , Close , High , Low)")
            self.connection.commit()      
            self.resultconnect = sqlite3.connect(self.ResultToday)
            self.resultcommand = self.resultconnect.cursor()
            self.resultcommand.execute("CREATE TABLE Result(Action , Price , Share)")
            self.resultconnect.commit()
        else:
            self.connection = sqlite3.connect(self.TodayDate)
            self.dbcommand = self.connection.cursor()
            self.resultconnect = sqlite3.connect(self.ResultToday)
            self.resultcommand = self.resultconnect.cursor()
    
    def ResetInfromation(self):
        for x in range(0,4,1):
            self.BuyInformation[x]=0
    
    def InsertResult(self,expression,finalprice,share):
        self.resultcommand.execute("INSERT INTO Result VALUES (?,?,?)",(expression,finalprice,share))
        self.resultconnect.commit()
    
    def exeBuy(self):
        os.startfile("D:\\Futures\\Buy\\FutureBuy.application")
        
    def exeSell(self):
        os.startfile("D:\\Futures\\Sell\\ConsoleApplication1.application")
    
    def BuyOrSell(self,NowPrice):
        NowTime = datetime.datetime.now()
        ######################### if the point less or more 4points than previous data 
        for row in self.dbcommand.execute("SELECT * FROM Futures ORDER BY Time DESC LIMIT 10"):
     #       print(row)
            if NowPrice - float(row[2]) > 4:   #### should be bottom 
                if self.BuyInformation[0]==0:
                    print("做多新倉 "+NowPrice.__str__()+" "+NowTime.__str__())
                    self.BuyInformation[0] = 1
                    self.BuyInformation[1] = NowPrice
                    self.BuyInformation[2] = "Positive"
                    self.BuyInformation[3] = NowTime
                    self.InsertResult("做多新倉",NowPrice.__str__(),"1")
                    #self.exeBuy()
                 #   self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多新倉",NowPrice.__str__()))
                 #   self.resultconnect.commit()
            elif NowPrice - float(row[2]) < -4:
                if self.BuyInformation[0]==0:
                    print("做空新倉 "+NowPrice.__str__()+" "+NowTime.__str__())
                    self.BuyInformation[0] = 1
                    self.BuyInformation[1] = NowPrice
                    self.BuyInformation[2] = "Negative"
                    self.BuyInformation[3] = NowTime
                    self.InsertResult("做空新倉",NowPrice.__str__(),"1")
                    #self.exeSell()
                #    self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多新倉",NowPrice.__str__()))
                #    self.resultconnect.commit()
        ################################################################################
    
    def Process(self,NowPrice):
        if self.BuyInformation[0]==1:
            ######################### 多單 #########################
            if self.BuyInformation[2]=="Positive":
                if float(NowPrice) - float(self.BuyInformation[1]) > 15:
                    self.ResetInfromation()
                    print("做多大賺平倉" + NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                    self.InsertResult("做多平倉",NowPrice.__str__(),"0")
                    #self.exeSell()
                #    self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多平倉",NowPrice.__str__()))
                #    self.resultconnect.commit()
                elif float(NowPrice) - float(self.BuyInformation[1]) < 15 and float(NowPrice) - float(self.BuyInformation[1]) > 5:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=90):  
                        self.ResetInfromation()
                        print("做多平倉 "+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                        self.InsertResult("做多平倉",NowPrice.__str__(),"0")
                        #self.exeSell()
                        #self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多平倉",NowPrice.__str__()))
                        #self.resultconnect.commit()
                    else:
                        pass 
                elif float(NowPrice) - float(self.BuyInformation[1]) < -3:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=90):  
                        self.ResetInfromation()
                        print("做多平倉虧損 "+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                        self.InsertResult("做多平倉",NowPrice.__str__(),"0")
                        #self.exeSell()
                        #self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多平倉",NowPrice.__str__()))
                        #self.resultconnect.commit()
                    else:
                        pass 
                    
            ######################### 空單 #########################        
            if self.BuyInformation[2]=="Negative":
                if float(NowPrice) - float(self.BuyInformation[1]) < -15:
                    self.ResetInfromation()
                    print("做空平倉大賺 "+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                    self.InsertResult("做空平倉",NowPrice.__str__(),"0")
                    #self.exeBuy()
                    #self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做空平倉",NowPrice.__str__()))
                    #self.resultconnect.commit()
                
                elif float(NowPrice) - float(self.BuyInformation[1]) > -15 and float(NowPrice) - float(self.BuyInformation[1]) < -5:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=210):  
                        self.ResetInfromation()
                        print("做空平倉 "+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                        self.InsertResult("做空平倉",NowPrice.__str__(),"0")
                        #self.exeBuy()
                     #   self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做空平倉",NowPrice.__str__()))
                     #   self.resultconnect.commit()
                    else:
                        pass 
                elif float(NowPrice) - float(self.BuyInformation[1]) > 3:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=90):  
                        self.ResetInfromation()
                        print("做空平倉虧損"+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                        self.InsertResult("做空平倉",NowPrice.__str__(),"0")
                        #self.exeBuy()
                        #self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做空平倉",NowPrice.__str__()))
                        #self.resultconnect.commit()
                    else:
                        pass 
                    
    def Strategy(self,NowPrice):
        self.BuyOrSell(NowPrice)
        self.Process(NowPrice)
        
class Futures(DataBase):
    
    def __init__(self):
        super().__init__()
        self.GetInfo()
    
    def TestCase(self):
        wb = load_workbook('20160429Detail.xlsx')
        ws = wb.active
        x=0
        for row in ws.rows:
            if x==0:
                x=x+1
                continue
            else:
                self.Strategy(row[3].value)
                self.dbcommand.execute("INSERT INTO Futures VALUES (?,?,?,?,?)",("20160429", row[0].value.__str__(), row[3].value.__str__() ,"8500" , "8300"))
                x=x+1 
                  
    def GetInfo(self):
        x=0
        while True :
            try:
                self.url="http://mis.twse.com.tw/stock/data/futures_side.txt"   
                self.Response = requests.get(self.url)
                self.Futures=json.loads(self.Response.text)
                self.dbcommand.execute("INSERT INTO Futures VALUES (?,?,?,?,?)",(self.Futures['msgArray'][0]['d'],self.Futures['msgArray'][0]['t'],float(self.Futures['msgArray'][0]['z']),self.Futures['msgArray'][0]['h'],self.Futures['msgArray'][0]['l']))
                self.connection.commit()
                x = x+1
                self.Strategy(float(self.Futures['msgArray'][0]['z']))
                sleep(1)
                
            except requests.exceptions:
                print("Have connection error")
                pass

#b=DataBase()
a = Futures()



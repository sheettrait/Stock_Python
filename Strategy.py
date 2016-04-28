# coding=Big5
import json
import requests
import sqlite3
import os.path
import datetime
from time import sleep

class DataBase():
    
    def __init__(self):
        self.CreateDataBase()
        self.BuyInformation=[0,0,0,0] # [0] = flag, [1] = price ,[2] postitve or negative
        self.Record=[]
        
    def CreateDataBase(self):
        if(os.path.isfile('Futures.db')==False):
            self.connection = sqlite3.connect('Futures.db')
            self.dbcommand = self.connection.cursor()
            self.dbcommand.execute("CREATE TABLE Futures(Date , Time , Close , High , Low)")
            self.connection.commit()      
        else:
            self.connection = sqlite3.connect('Futures.db')
            self.dbcommand = self.connection.cursor()  
    #        self.dbcommand.execute("INSERT INTO Futures VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    
    def ResetInfromation(self):
        for x in range(0,4,1):
            self.BuyInformation[x]=0
    
    def BuyOrSell(self,NowPrice,row):
        NowTime = datetime.datetime.now()
        ######################### if the point less or more 4points than previous data 
        if NowPrice - float(row[2]) > 4:   #### should be bottom 
            if self.BuyInformation[0]==0:
                print("做多新倉")
                self.BuyInformation[0] = 1
                self.BuyInformation[1] = NowPrice
                self.BuyInformation[2] = "Positive"
                self.BuyInformation[3] = NowTime
                self.Record.append("做多新倉")
                self.Record.append(NowPrice)
        elif NowPrice - float(row[2]) < -4:
            if self.BuyInformation[0]==0:
                self.BuyInformation[0] = 1
                self.BuyInformation[1] = NowPrice
                self.BuyInformation[2] = "Negative"
                self.BuyInformation[3] = NowTime
                self.Record.append("做空新倉")
                self.Record.append(NowPrice)
        ################################################################################
    
    def Process(self,NowPrice):
        if self.BuyInformation[0]==1:
            ######################### 多單 #########################
            if self.BuyInformation[2]=="Positive":
                if float(NowPrice) - float(self.BuyInformation[1]) > 15:
                    self.Record.append("做多平倉")
                    self.Record.append(NowPrice)
                    self.ResetInfromation()
                    print("做多平倉")
                
                elif float(NowPrice) - float(self.BuyInformation[1]) < 15 and float(NowPrice) - float(self.BuyInformation[1]) > 5:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=210):  
                        self.Record.append("做多平倉")
                        self.Record.append(NowPrice)
                        self.ResetInfromation()
                        print("做多平倉")
                    else:
                        pass 
                elif float(NowPrice) - float(self.BuyInformation[1]) < 0:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=60):  
                        self.Record.append("做多平倉")
                        self.Record.append(NowPrice)
                        self.ResetInfromation()
                        print("做多平倉")
                    else:
                        pass 
                    
                    
            ######################### 空單 #########################        
            if self.BuyInformation[2]=="Negative":
                if float(NowPrice) - float(self.BuyInformation[1]) < -15:
                    self.Record.append("做空平倉")
                    self.Record.append(NowPrice)
                    self.ResetInfromation()
                    print("做空平倉")
                
                elif float(NowPrice) - float(self.BuyInformation[1]) > -15 and float(NowPrice) - float(self.BuyInformation[1]) < -5:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=210):  
                        self.Record.append("做空平倉")
                        self.Record.append(NowPrice)
                        self.ResetInfromation()
                        print("做空平倉")
                    else:
                        pass 
                elif float(NowPrice) - float(self.BuyInformation[1]) > 0:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=60):  
                        self.Record.append("做空平倉")
                        self.Record.append(NowPrice)
                        self.ResetInfromation()
                        print("做空平倉")
                    else:
                        pass 
                
    def Strategy(self,NowPrice):
        NowTime = datetime.datetime.now()
        for row in self.dbcommand.execute("SELECT * FROM Futures"):
            if float(row[2])>8580 and float(row[2])<8750:
            
                ####Timedata
                print(NowTime - datetime.datetime(int(row[0][0:4]),int(row[0][4:6]),int(row[0][6:8]),int(row[1][0:2]),int(row[1][3:5]),int(row[1][6:8])))
        
        self.BuyOrSell(NowPrice,row)
        self.Process(NowPrice)
        
        
        
        
class Futures(DataBase):
    def __init__(self):
   #     self.initdatabase()
        super().__init__()
        
        self.PowerStage=0
        self.PowerSatisfy=0
        self.MiddleStage=0
        self.WeakStage=0
        self.WeakSatisfy=0
   #     self.GetInfo()

    def GetInfo(self):
        x=0
        while x<=1:
            self.url="http://mis.twse.com.tw/stock/data/futures_side.txt"   
            self.Response = requests.get(self.url)
            self.Futures=json.loads(self.Response.text)
            print(self.Futures['msgArray'][0])
            difference = float(self.Futures['msgArray'][0]['h'])-float(self.Futures['msgArray'][0]['l'])
            self.MiddleStage = (float(self.Futures['msgArray'][0]['l'])+float(self.Futures['msgArray'][0]['h']))/2
            self.PowerStage = float(self.Futures['msgArray'][0]['l']) + difference*1.382
            self.PowerSatisfy = float(self.Futures['msgArray'][0]['l']) + difference*1.618
            self.WeakStage = float(self.Futures['msgArray'][0]['h']) - difference*1.382
            self.WeakSatisfy = float(self.Futures['msgArray'][0]['h']) - difference*1.618
            print("====================")
            print(self.PowerSatisfy)
            print(self.PowerStage)
            print(self.MiddleStage)
            print(self.WeakStage)
            print(self.WeakSatisfy)
            
         #   self.dbcommand.execute("INSERT INTO Futures VALUES (?,?,?,?,?)",(self.Futures['msgArray'][0]['d'],self.Futures['msgArray'][0]['t'],float(self.Futures['msgArray'][0]['z']),self.Futures['msgArray'][0]['h'],self.Futures['msgArray'][0]['l']))
        #    self.connection.commit()
            x = x+1
       #     sleep(1)
        
        for row in self.dbcommand.execute("SELECT Close FROM Futures"):
            if row[0]>8602:
                print(row)
     #   print(self.dbcommand.execute("SELECT * FROM Futures").fetchall().__len__())
        
    #    print(self.dbcommand.execute("SELECT * FROM Futures").fetchall()[5][3])
b=DataBase()  
b.Strategy(230)
#a = Futures()

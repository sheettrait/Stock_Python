# coding=Big5
import json
import requests
import sqlite3
import os.path
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
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
            self.resultconnect = sqlite3.connect('result.db')
            self.resultcommand = self.resultconnect.cursor()
            self.resultcommand.execute("CREATE TABLE Result(Action , Price)")
            self.resultconnect.commit()
        else:
            self.connection = sqlite3.connect('Futures.db')
            self.dbcommand = self.connection.cursor()
            
            self.resultconnect = sqlite3.connect('result.db')
            self.resultcommand = self.resultconnect.cursor()
    
    def ResetInfromation(self):
        for x in range(0,4,1):
            self.BuyInformation[x]=0
    
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
                    self.Record.append("做多新倉")
                    self.Record.append(NowPrice)
                    self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多新倉",NowPrice.__str__()))
                    
            elif NowPrice - float(row[2]) < -4:
                if self.BuyInformation[0]==0:
                    print("做空新倉 "+NowPrice.__str__()+" "+NowTime.__str__())
                    self.BuyInformation[0] = 1
                    self.BuyInformation[1] = NowPrice
                    self.BuyInformation[2] = "Negative"
                    self.BuyInformation[3] = NowTime
                    self.Record.append("做空新倉")
                    self.Record.append(NowPrice)
                    self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多新倉",NowPrice.__str__()))

        ################################################################################
    
    def Process(self,NowPrice):
        if self.BuyInformation[0]==1:
            ######################### 多單 #########################
            if self.BuyInformation[2]=="Positive":
                if float(NowPrice) - float(self.BuyInformation[1]) > 15:
                    self.Record.append("做多大賺平倉")
                    self.Record.append(NowPrice)
                    self.ResetInfromation()
                    print("做多大賺平倉" + NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                    self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多平倉",NowPrice.__str__()))
                
                elif float(NowPrice) - float(self.BuyInformation[1]) < 15 and float(NowPrice) - float(self.BuyInformation[1]) > 5:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=210):  
                        self.Record.append("做多平倉")
                        self.Record.append(NowPrice)
                        self.ResetInfromation()
                        print("做多平倉 "+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                        self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多平倉",NowPrice.__str__()))
                    else:
                        pass 
                elif float(NowPrice) - float(self.BuyInformation[1]) < 0:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=60):  
                        self.Record.append("做多平倉")
                        self.Record.append(NowPrice)
                        self.ResetInfromation()
                        print("做多平倉虧損 "+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                        self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做多平倉",NowPrice.__str__()))
                    else:
                        pass 
                    
            ######################### 空單 #########################        
            if self.BuyInformation[2]=="Negative":
                if float(NowPrice) - float(self.BuyInformation[1]) < -15:
                    self.Record.append("做空平倉")
                    self.Record.append(NowPrice)
                    self.ResetInfromation()
                    print("做空平倉大賺 "+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                    self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做空平倉",NowPrice.__str__()))
                
                elif float(NowPrice) - float(self.BuyInformation[1]) > -15 and float(NowPrice) - float(self.BuyInformation[1]) < -5:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=210):  
                        self.Record.append("做空平倉")
                        self.Record.append(NowPrice)
                        self.ResetInfromation()
                        print("做空平倉 "+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                        self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做空平倉",NowPrice.__str__()))
                    else:
                        pass 
                elif float(NowPrice) - float(self.BuyInformation[1]) > 0:
                    NowTime = datetime.datetime.now()
                    if NowTime - self.BuyInformation[3] > datetime.timedelta(seconds=60):  
                        self.Record.append("做空平倉")
                        self.Record.append(NowPrice)
                        self.ResetInfromation()
                        print("做空平倉虧損"+ NowPrice.__str__()+" "+self.BuyInformation[3].__str__())
                        self.resultcommand.execute("INSERT INTO Result VALUES (?,?)",("做空平倉",NowPrice.__str__()))
                    else:
                        pass 
                    
    def Strategy(self,NowPrice):
        self.BuyOrSell(NowPrice)
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
      #  self.TestCase()
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
        #        print(row[3].value)
        
    def GetInfo(self):
        x=0
        while True :
            self.url="http://mis.twse.com.tw/stock/data/futures_side.txt"   
            self.Response = requests.get(self.url)
            self.Futures=json.loads(self.Response.text)
         #   print(self.Futures['msgArray'][0])
            difference = float(self.Futures['msgArray'][0]['h'])-float(self.Futures['msgArray'][0]['l'])
            self.MiddleStage = (float(self.Futures['msgArray'][0]['l'])+float(self.Futures['msgArray'][0]['h']))/2
            self.PowerStage = float(self.Futures['msgArray'][0]['l']) + difference*1.382
            self.PowerSatisfy = float(self.Futures['msgArray'][0]['l']) + difference*1.618
            self.WeakStage = float(self.Futures['msgArray'][0]['h']) - difference*1.382
            self.WeakSatisfy = float(self.Futures['msgArray'][0]['h']) - difference*1.618
     #       print("====================")
     #       print(self.PowerSatisfy)
     #       print(self.PowerStage)
     #       print(self.MiddleStage)
     #       print(self.WeakStage)
     #       print(self.WeakSatisfy)
     
            self.dbcommand.execute("INSERT INTO Futures VALUES (?,?,?,?,?)",(self.Futures['msgArray'][0]['d'],self.Futures['msgArray'][0]['t'],float(self.Futures['msgArray'][0]['z']),self.Futures['msgArray'][0]['h'],self.Futures['msgArray'][0]['l']))
            self.connection.commit()
            x = x+1
            self.Strategy(float(self.Futures['msgArray'][0]['z']))
            sleep(1)
      #  for row in self.dbcommand.execute("SELECT Close FROM Futures"):
      #      if row[0]>8300:
      #          print(row)
     #   print(self.dbcommand.execute("SELECT * FROM Futures").fetchall().__len__())
        
    #    print(self.dbcommand.execute("SELECT * FROM Futures").fetchall()[5][3])
#b=DataBase()
a = Futures()

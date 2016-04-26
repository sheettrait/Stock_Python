import json
import requests
import sqlite3
import os.path
from time import sleep

class DataBase():
    
    def __init__(self):
        self.CreateDataBase()
        
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

            
class Futures(DataBase):
    def __init__(self):
   #     self.initdatabase()
        super().__init__()
        
        self.PowerStage=0
        self.PowerSatisfy=0
        self.MiddleStage=0
        self.WeakStage=0
        self.WeakSatisfy=0
        self.GetInfo()

    def GetInfo(self):
        x=22
        while x<=40:
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
            
            self.dbcommand.execute("INSERT INTO Futures VALUES (?,?,?,?,?)",(self.Futures['msgArray'][0]['d'],self.Futures['msgArray'][0]['t'],float(self.Futures['msgArray'][0]['z'])+x,self.Futures['msgArray'][0]['h'],self.Futures['msgArray'][0]['l']))
            self.connection.commit()
            x = x+1
            sleep(0.5)
        
        for row in self.dbcommand.execute("SELECT Close FROM Futures"):
            if row[0]>8602:
                print(row)
     #   print(self.dbcommand.execute("SELECT * FROM Futures").fetchall().__len__())
        
    #    print(self.dbcommand.execute("SELECT * FROM Futures").fetchall()[5][3])
#b=DataBase()  
a = Futures()

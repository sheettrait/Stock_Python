# coding=utf-8
import csv
import io
import urllib
import requests
import sys
import urllib.request
import tkinter

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
                   # elif QueryPrice.get_earnings_share()==None:
                    #    print(self.soup.select('.basic2')[x-2].text)
                    #    print("hi"+QueryPrice.get_earnings_share())
                    #    self.AllData.append("None")
                        
        
        
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
#b.getihi()
#a = GetData()
#a.SearchPERatio()
#print(a.AllData)
#print("sss")
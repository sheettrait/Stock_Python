import sqlite3
import datetime
  
data  = datetime.datetime.date(datetime.datetime.now()).__str__()+"-Data.db" 
connect2 = sqlite3.connect(data)
command = connect2.cursor()
#for line in command.execute("SELECT * FROM Futures WHERE Close > 8134 ORDER BY Time ASC LIMIT 30"):
for line in command.execute("SELECT * FROM Futures"):
    print(line)
    
print("===============================")
  
data  = datetime.datetime.date(datetime.datetime.now()).__str__()+"-Result.db" 
connect2 = sqlite3.connect(data)
command = connect2.cursor()
count = 0

for line in command.execute("SELECT * FROM Result"):
    print(line)

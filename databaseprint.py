import sqlite3
import datetime
  
print(datetime.datetime.date(datetime.datetime.now()).__str__()+"123")
connect2 = sqlite3.connect('Futures.db')
command = connect2.cursor()
for line in command.execute("SELECT * FROM Futures WHERE Close > 8134 ORDER BY Time ASC LIMIT 30"):
    print(line)
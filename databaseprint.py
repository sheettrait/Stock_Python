import sqlite3


  
connect2 = sqlite3.connect('Futures.db')
command = connect2.cursor()
for line in command.execute("SELECT * FROM Futures"):
    print(line)
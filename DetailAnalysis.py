import openpyxl
import csv 
import datetime
from openpyxl import Workbook



wb = Workbook()
ws = wb.active
reader = csv.reader(open('Daily_2016_06_21.csv'))

a = 1
row_counter = 1

for row in reader:
    try:
        if "TX" in row[1] and "MTX" not in row[1]:
        #    print(row[3][0:2]) 
        #    print(row)
        #    print(datetime.date(2002,1,2).isoformat())
            ws.cell(row = row_counter , column = 1, value = row[4])
            row_counter = row_counter + 1
    except:
        pass

wb.save("DetailPrice.xlsx")
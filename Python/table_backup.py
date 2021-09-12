import sys
import json
import requests
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="airdata",
  passwd="AESl0uis!",
  database="airdata"
)

mycursor = mydb.cursor()

#Find the current month and create a name for backup table
current_date = datetime.today()
current_month = current_date.month
current_year = current_date.year
new_table = "monitor_data" + str(current_year) + '_' + str(current_month)

print('Table to create is', new_table)

#Creates New Table with month attached and copies current data into this table
sql = 'CREATE TABLE ' + new_table + ' LIKE monitor_data;'
sql2 = 'INSERT INTO ' + new_table + ' SELECT * FROM monitor_data;'


#determine date to start erasing data
if current_month  < 11:
    delete_before = str(current_year) + '-0' + str(current_month - 1) + '-01 11:30:00'
else:
    delete_before = str(current_year) + '-' + str(current_month - 1) + '-01 11:30:00'

#Delete Extra Data from active table
sql3 = "DELETE FROM monitor_data WHERE lastModified < '" + delete_before + "';" 

#Update Main Backup Table
sql4 = "INSERT INTO historical_data SELECT * FROM monitor_data;"

print('Executing:\n', sql, sql2, sql3, sql4)

#Execute SQL queries
mycursor.execute(sql4)
mydb.commit()
mycursor.execute(sql3)
mydb.commit()
mycursor.execute(sql)
mydb.commit()
mycursor.execute(sql2)
mydb.commit()
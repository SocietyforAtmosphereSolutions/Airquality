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

#Create a View using my stupid complicated query
sql = "SELECT table2.*, max(table2.PM2_5Value) AS MAX, min(table2.PM2_5Value) AS MIN, avg(table2.PM2_5Value) AS AVG FROM (SELECT *, max(lastModified) AS max_date FROM monitor_data GROUP BY ID) AS aggregated_table INNER JOIN monitor_data AS table2 ON aggregated_table.max_date=table2.lastModified GROUP BY table2.lastModified ORDER BY table2.ID"
sql2 = "CREATE OR REPLACE VIEW Working_Data AS " + sql

#sql3 = "DROP TABLE IF EXISTS Current_Data"
sql4 = "CREATE TABLE Current_Data AS SELECT * FROM Working_Data"
#sql3 = "REPLACE INTO Current_Data SELECT * FROM Working_Data"

#Execute SQL queries
mycursor.execute(sql2)
mydb.commit()
mycursor.execute(sql4)
mydb.commit()
#mycursor.execute(sql4)
#mydb.commit()

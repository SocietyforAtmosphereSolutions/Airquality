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

def dropSensors():

  # opens JSON file as a readable string and assigns the
  # region list to a variable
  monitor_list = open("/var/www/html/scairquality.ca/public_html/Python/monitor_list.json", "r")
  region_list = json.loads(monitor_list.read())
  ID_list = region_list["Regions"]
  total_ids = []

  # Closes monitor list JSON to avoid memory leaks
  monitor_list.close()

  # concatenates all monitor ids from the region list into one variable
  for i in ID_list:
      # for every ID in each region add another ID equal to the original
      # ID plus 1 (This is the B channel for each monitor)
      for x in i["Stations"]:
          total_ids.append(x)
  print(total_ids)

  for tableid in total_ids:
    sql_del = "DROP TABLE IF EXISTS sensor" + str(tableid) + ";"
    mycursor.execute(sql_del)
    mydb.commit()

def clearTable(table):
  sql_del = "DELETE FROM " + table
  mycursor.execute(sql_del)
  mydb.commit()

def dropTable(table):
  sql_del = "DROP TABLE IF EXISTS " + table
  print(sql_del)
  mycursor.execute(sql_del)
  mydb.commit()

TABLE_NAME = ""

if len(sys.argv) != 2:
    print("Invalid number of arguments!")
    print("  USAGE: script.py table_name")
    exit()
else:
    TABLE_NAME = sys.argv[1]

if (TABLE_NAME == "sensors"):
  dropSensors()
else:
  clearTable(TABLE_NAME)




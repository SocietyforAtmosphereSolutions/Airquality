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

def dropTable(table):
  sql_del = "DROP TABLE IF EXISTS " + table
  print(sql_del)
  mycursor.execute(sql_del)
  mydb.commit()

if len(sys.argv) == 2:
    sensor_list = []
    sensor_list.append(sys.argv[1])
    print("updating single table " + sys.argv[1])
else:
    # opens JSON file as a readable string and assigns the
    # region list to a variable
    monitor_list = open("/var/www/html/scairquality.ca/public_html/Python/monitor_list.json", "r")
    region_list = json.loads(monitor_list.read())
    ID_list = region_list["Regions"]
    sensor_list = []

    # Closes monitor list JSON to avoid memory leaks
    monitor_list.close()

    # concatenates all monitor ids from the region list into one variable
    for i in ID_list:
        # for every ID in each region add another ID equal to the original
        # ID plus 1 (This is the B channel for each monitor)
        for x in i["Stations"]:
            sensor_list.append(x)
    print("updating all tables")
            


for tableid in sensor_list:

  sensor_table = f"sensor{str(tableid)}_daily"

  sql = f"SELECT ROUND(AVG(AChannel), 2) AS AverageA, ROUND(AVG(BChannel), 2) AS AverageB, lastModified FROM hist_monitor_readings WHERE id = {str(tableid)} GROUP BY id, YEAR(LastModified), MONTH(LastModified), DAY(LastModified) ORDER BY LastModified;"
      
  mycursor.execute(sql)

  desc = mycursor.description
  column_names = [col[0] for col in desc]
  data = [dict(zip(column_names, row))
          for row in mycursor.fetchall()]
  output_data = []

  print(f"Completed SELECT query for sensor #{str(tableid)}")

  for a in range(0, len(data)):
    i = data[a]
    x = {}
    x["AChannel"] = i["AverageA"]
    x["BChannel"] = i["AverageB"]
    x["lastModified"] = i["lastModified"]
    print("Appending: ", x)
    output_data.append(x)
  
  print(f"Completed data collection for sensor #{str(tableid)}")

  dropTable(sensor_table)

  sql2 = f"CREATE TABLE {sensor_table} (AChannel float, BChannel float, lastModified datetime)"
  mycursor.execute(sql2)
  mydb.commit()

  for monitor in output_data:
    sql3 = "INSERT INTO " + sensor_table + " (AChannel, BChannel, lastModified) VALUES (%s, %s, %s)"
    val = (str(monitor.get("AChannel", -1)), str(monitor.get("BChannel", -1)), str(monitor.get("lastModified", "null")))

    mycursor.execute(sql3, val)
    mydb.commit()
  print(f"Completed adding data to individual sensor table for sensor #{str(tableid)}")


for tableid in sensor_list:

  sensor_table = f"sensor{str(tableid)}_hourly"

  sql = f"SELECT AChannel, BChannel, lastModified FROM hist_monitor_readings WHERE id = {str(tableid)} ORDER BY LastModified"
      
  mycursor.execute(sql)

  desc = mycursor.description
  column_names = [col[0] for col in desc]
  data = [dict(zip(column_names, row))
          for row in mycursor.fetchall()]
  output_data = []

  print(f"Completed SELECT query for sensor #{str(tableid)}")

  for a in range(0, len(data)):
    i = data[a]
    x = {}
    x["AChannel"] = i["AChannel"]
    x["BChannel"] = i["BChannel"]
    x["lastModified"] = i["lastModified"]
    print("Appending: ", x)
    output_data.append(x)
  
  print(f"Completed data collection for sensor #{str(tableid)}")

  dropTable(sensor_table)

  sql2 = f"CREATE TABLE {sensor_table} (AChannel float, BChannel float, lastModified datetime)"
  mycursor.execute(sql2)
  mydb.commit()

  for monitor in output_data:
    sql3 = "INSERT INTO " + sensor_table + " (AChannel, BChannel, lastModified) VALUES (%s, %s, %s)"
    val = (str(monitor.get("AChannel", -1)), str(monitor.get("BChannel", -1)), str(monitor.get("lastModified", "null")))

    mycursor.execute(sql3, val)
    mydb.commit()
  print(f"Completed adding data to individual sensor table for sensor #{str(tableid)}")
    

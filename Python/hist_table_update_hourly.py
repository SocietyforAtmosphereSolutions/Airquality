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

# opens JSON file as a readable string and assigns the
# region list to a variable
monitor_list = open("/home/legal-server/python_code/monitor_list.json", "r")
region_list = json.loads(monitor_list.read())
ID_list = region_list["Regions"]
total_ids = []
test = [1314]

if len(sys.argv) == 3:
  arg_one = str(sys.argv[1])
  arg_two = str(sys.argv[2])
elif len(sys.argv) == 2:
  arg_one = str(sys.argv[1])
  arg_two = 'null'
else:
  arg_one = 'null'
  arg_two = 'null'
#print(arg_one)

if arg_one == 'test':
  sensor_list = test
  print("Running in test mode, will only affect station #1314")
elif arg_one == 'single':
  sensor_list = [arg_two]
  print("Running in single station mode, will only affect station #" + arg_two)
else:
  print("Running in normal mode, will affect all stations")
  sensor_list = total_ids

# concatenates all monitor ids from the region list into one variable
for i in ID_list:
    # for every ID in each region add another ID equal to the original
    # ID plus 1 (This is the B channel for each monitor)
    for x in i["Stations"]:
        total_ids.append(x)
#print(total_ids)

for tableid in sensor_list:

  #sql = "SELECT * FROM monitor_data WHERE ID = " + str(tableid) + " OR ParentID =" + str(tableid) + ";"

  sql = "SELECT ID, ParentID, Label, ROUND(AVG(PM2_5Value), 2) AS Average, ROUND(MAX(PM2_5Value), 2) AS Maximum, lastModified FROM historical_data WHERE id =" + str(tableid) + " OR ParentID = " + str(tableid) + " GROUP BY id, YEAR(LastModified), MONTH(LastModified), DAY(LastModified), HOUR(LastModified) ORDER BY LastModified"
      
  mycursor.execute(sql)

  desc = mycursor.description
  column_names = [col[0] for col in desc]
  data = [dict(zip(column_names, row))
          for row in mycursor.fetchall()]
  output_data = []

  print("Completed SELECT query for sensor #" + str(tableid))

  for a in range(0, len(data)):
    i = data[a]
    x = {}
    if int(i["ID"]) == int(tableid):
      x["AChannel"] = i["Average"]
      x["lastModified"] = i["lastModified"]
    else:
      continue

    for c in range(a+1, len(data)):
      b = data[c]
      #print("Timestamp comparison:", b["lastModified"], x["lastModified"], b["lastModified"] - x["lastModified"])
      if b["lastModified"] == x["lastModified"] and str(b["ParentID"]) == str(tableid):
        x["BChannel"] = b["Average"]
      break

    #print("Appending: ", x)
    output_data.append(x)

  print("Completed data collection for sensor #" + str(tableid))

  sql_del = "DROP TABLE IF EXISTS sensor" + str(tableid) + "_hourly;"
  sql2 = "CREATE TABLE sensor" + str(tableid) + "_hourly (AChannel float, BChannel float, lastModified datetime)"
  mycursor.execute(sql_del)
  mycursor.execute(sql2)

  for monitor in output_data:
    sql3 = "INSERT INTO sensor" + str(tableid) + "_hourly (AChannel, BChannel, lastModified) VALUES (%s, %s, %s)"
    val = (str(monitor.get("AChannel", 0)), str(monitor.get("BChannel", 0)), str(monitor.get("lastModified", "null")))

    mycursor.execute(sql3, val)
    mydb.commit()

  print("Completed adding data to individual sensor table for sensor #" + str(tableid))
    
#print(output_data)
#print(len(data) / 2)
#print(len(output_data))
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
monitor_list = open("/var/www/html/scairquality.ca/public_html/Python/monitor_list.json", "r")
region_list = json.loads(monitor_list.read())
ID_list = region_list["Regions"]
total_ids = []


# concatenates all monitor ids from the region list into one variable
for i in ID_list:
    # for every ID in each region add another ID equal to the original
    # ID plus 1 (This is the B channel for each monitor)
    for x in i["Stations"]:
        total_ids.append(x)
print(total_ids)

for tableid in total_ids:

  sql = "SELECT * FROM monitor_data WHERE ID = " + str(tableid) + " OR ParentID =" + str(tableid) + ";"

  mycursor.execute(sql)

  desc = mycursor.description
  column_names = [col[0] for col in desc]
  data = [dict(zip(column_names, row))
          for row in mycursor.fetchall()]
  output_data = []

  for a in range(0, len(data)):
    i = data[a]
    x = {}
    if int(i["ID"]) == int(tableid):
      x["AChannel"] = i["PM2_5Value"]
      x["lastModified"] = i["lastModified"]
    else:
      continue

    for c in range(a+1, len(data)):
      b = data[c]
      #print("Timestamp comparison:", b["lastModified"], x["lastModified"], b["lastModified"] - x["lastModified"])
      if b["lastModified"] == x["lastModified"] and str(b["ParentID"]) == str(tableid):
        x["BChannel"] = b["PM2_5Value"]
      break

    #print("Appending: ", x)
    output_data.append(x)

  sql_del = "DROP TABLE IF EXISTS sensor" + str(tableid) + ";"
  sql2 = "CREATE TABLE sensor" + str(tableid) + "(AChannel float, BChannel float, lastModified datetime)"
  mycursor.execute(sql_del)
  mycursor.execute(sql2)

  for monitor in output_data:
    sql3 = "INSERT INTO sensor" + str(tableid) + " (AChannel, BChannel, lastModified) VALUES (%s, %s, %s)"
    val = (str(monitor.get("AChannel", 0)), str(monitor.get("BChannel", 0)), str(monitor.get("lastModified", "null")))

    mycursor.execute(sql3, val)
    mydb.commit()
    
#print(output_data)
#print(len(data) / 2)
#print(len(output_data))

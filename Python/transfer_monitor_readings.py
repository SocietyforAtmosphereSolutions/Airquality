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


##########################################################################
#
# Read the command line argument and ensure it is valid.
#  - As a reminder from the description above, this selects which
#    database to store the current purple air data to.
#
##########################################################################
TABLE_NAME = "hist_monitor_readings"

SOURCE_NAME = ""

if len(sys.argv) != 2:
    print("Invalid number of arguments!")
    print("  USAGE: script.py table_name")
    exit()
else:
    SOURCE_NAME = sys.argv[1]

# Check if the table already exists.
mycursor.execute("SHOW TABLES")
table_exists = False
for table_name in mycursor:
    if table_name[0] == TABLE_NAME:
        table_exists = True


MYSQL = "CREATE TABLE " + TABLE_NAME + " ("
MYSQL = MYSQL + "ID INT" + ", "
MYSQL = MYSQL + "AChannel FLOAT" + ", "
MYSQL = MYSQL + "BChannel FLOAT" + ", "
MYSQL = MYSQL + "AGE INT" + ", "
MYSQL = MYSQL + "lastModified DATETIME" + ", "
MYSQL = MYSQL + "UNIQUE KEY `ID` (`ID`,`lastModified`));"

#ALTER = "ALTER TABLE " + TABLE_NAME + " ADD UNIQUE INDEX(ID, lastModified);"

# Create the table in the database using the mysql command from above.
if not table_exists:
    mycursor.execute(MYSQL)
    print("Create Table: ", TABLE_NAME)

# opens JSON file as a readable string and assigns the
# region list to a variable
monitor_list = open("/var/www/html/scairquality.ca/public_html/Python/monitor_list.json", "r")
region_list = json.loads(monitor_list.read())
ID_list = region_list["Regions"]
sensor_list = []


# concatenates all monitor ids from the region list into one variable
for i in ID_list:
    # for every ID in each region add another ID equal to the original
    # ID plus 1 (This is the B channel for each monitor)
    for x in i["Stations"]:
        sensor_list.append(x)

#print(sensor_list)

for tableid in sensor_list:

  #sql = "SELECT * FROM monitor_data WHERE ID = " + str(tableid) + " OR ParentID =" + str(tableid) + ";"

  sql = "SELECT ID, ParentID, ROUND(AVG(PM2_5Value), 2) AS Average, ROUND(MAX(PM2_5Value), 2) AS Maximum, lastModified, AGE FROM " + SOURCE_NAME + " WHERE id =" + str(tableid) + " OR ParentID = " + str(tableid) + " GROUP BY YEAR(LastModified), MONTH(LastModified), DAY(LastModified), HOUR(LastModified), ID ORDER BY LastModified"
      
  mycursor.execute(sql)

  desc = mycursor.description
  column_names = [col[0] for col in desc]
  data = [dict(zip(column_names, row))
          for row in mycursor.fetchall()]
  output_data = []

  print("Completed SELECT query for sensor #" + str(tableid))

  for a in range(0, (len(data) - 1)):
    i = data[a]
    b = data[a + 1]
    print(i, b)
    x = {}
    if int(i["ID"]) == int(tableid):
      x["ID"] = i["ID"]
      x["AGE"] = i["AGE"]
      x["AChannel"] = i["Average"]
      x["BChannel"] = b["Average"]
      x["lastModified"] = i["lastModified"]
      print("Appending: ", x)
      output_data.append(x)
    

  print("Completed data collection for sensor #" + str(tableid))

  for monitor in output_data:
    sql2 = "INSERT IGNORE INTO " + TABLE_NAME + " (ID, AChannel, BChannel, AGE, lastModified) VALUES (%s, %s, %s, %s, %s)"
    val = (
      str(monitor.get("ID", "0")),
      str(monitor.get("AChannel", 0)), 
      str(monitor.get("BChannel", 0)),
      str(monitor.get("AGE", 0)), 
      str(monitor.get("lastModified", "null")))

    mycursor.execute(sql2, val)
    mydb.commit()

  print("Completed adding data to individual sensor table for sensor #" + str(tableid))

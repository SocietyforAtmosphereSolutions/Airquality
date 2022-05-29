import sys
import json
from xmlrpc.client import boolean
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


##########################################################################
#
# Read the command line argument and ensure it is valid.
#  - As a reminder from the description above, this selects which
#    database to store the current purple air data to.
#
##########################################################################
TABLE_NAME = "averaged_readings"

SOURCE_NAME = "current_readings"


if len(sys.argv) == 3:
  SOURCE_NAME = sys.argv[1]
  TABLE_NAME = sys.argv[2]
elif len(sys.argv) > 3:
  print("Invalid number of arguments!")
  print("  USAGE: script.py source_table dest_table")
  exit()

dropTable(TABLE_NAME)


# Check if the table already exists.
mycursor.execute("SHOW TABLES")
table_exists = False
for table_name in mycursor:
    if table_name[0] == TABLE_NAME:
        table_exists = True


MYSQL = "CREATE TABLE " + TABLE_NAME + " ("
MYSQL = MYSQL + "ID INT" + ", "
MYSQL = MYSQL + "Region VARCHAR(128)" + ", "
MYSQL = MYSQL + "Label VARCHAR(128)" + ", "
MYSQL = MYSQL + "Lat FLOAT" + ", "
MYSQL = MYSQL + "Lon FLOAT" + ", "
MYSQL = MYSQL + "PM2_5Value FLOAT" + ", "
MYSQL = MYSQL + "AGE INT" + ", "
MYSQL = MYSQL + "lastModified DATETIME" + ", "
MYSQL = MYSQL + "UNIQUE (ID));"

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

# Closes monitor list JSON to avoid memory leaks
monitor_list.close()


# concatenates all monitor ids from the region list into one variable
for i in ID_list:
    # for every ID in each region add another ID equal to the original
    # ID plus 1 (This is the B channel for each monitor)
    for x in i["Stations"]:
        sensor_list.append(x)

#print(sensor_list)

for tableid in sensor_list:

  sql = f"SELECT const_data.ID,  const_data.Label, const_data.Region, {SOURCE_NAME}.PM2_5Value, const_data.Lat, const_data.Lon, {SOURCE_NAME}.lastModified, {SOURCE_NAME}.AGE FROM {SOURCE_NAME} INNER JOIN const_data ON {SOURCE_NAME}.ID = const_data.ID WHERE {SOURCE_NAME}.ID = {str(tableid)} OR {SOURCE_NAME}.ParentID = {str(tableid)} ORDER BY LastModified DESC;"

  mycursor.execute(sql)

  desc = mycursor.description
  column_names = [col[0] for col in desc]
  data = [dict(zip(column_names, row))
          for row in mycursor.fetchall()]
  output_data = []

  print(f"Completed SELECT query for sensor #{str(tableid)}")

  for a in range(0, (len(data) - 1)):
    i = data[a]
    b = data[a + 1]
    #print(i)
    x = {}
    if int(i["ID"]) == int(tableid):
      x["ID"] = i["ID"]
      x["Label"] = i["Label"]
      x["Region"] = i["Region"]
      x["Lat"] = i["Lat"]
      x["Lon"] = i["Lon"]
      x["AGE"] = i["AGE"]

      if ((i["PM2_5Value"] - b["PM2_5Value"]) > 50):
        print("channel discrepancy")
        x["PM2_5Value"] = b["PM2_5Value"]
      elif ((b["PM2_5Value"] - i["PM2_5Value"]) > 50):
        print("channel discrepancy")
        x["PM2_5Value"] = i["PM2_5Value"]
      else:
        x["PM2_5Value"] = ((i["PM2_5Value"] + b["PM2_5Value"]) / 2) 
      x["lastModified"] = i["lastModified"]
      #print("Appending: ", x)
      output_data.append(x)
    

  print(f"Completed data collection for sensor #{str(tableid)}")

  for monitor in output_data:
    sql2 = "INSERT IGNORE INTO " + TABLE_NAME + " (ID, Label, Region, PM2_5Value, Lat, Lon, lastModified, AGE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (
      str(monitor.get("ID", 0)),
      str(monitor.get("Label", "null")),
      str(monitor.get("Region", "null")),
      str(monitor.get("PM2_5Value", -1)), 
      str(monitor.get("Lat", 0)),
      str(monitor.get("Lon", 0)),
      str(monitor.get("lastModified", "null")),
      str(monitor.get("AGE", 0)))

    mycursor.execute(sql2, val)
    mydb.commit()

  print(f"Completed adding sensor #{str(tableid)} data to averaged data table")
  


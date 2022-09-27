##########################################################################
#
#  The script takes in a db table name as a command line parameter.
#  It validates that the name is one of two tables:
#    - monitor_data - Data that is retrieved every 5 minutes
#    - nightly_monitor_data - Data that is retrieved once a day
#  The script then creates the database table if it doesn't already
#  exists.  This table uses the purple air json file tags as
#  it column names.  Here is the definition of the column names
#  with unused columns noted:
#    - ID - PurpleAir Sensor ID
#    - ParentID - The PurpleAir Sensor Id of the "parent" entr for the B Channel
#    - Label - The "name" that appears on the map for this sensor
#    - DEVICE_LOCATIONTYPE - <NOT USED>
#    - THINGSPEAK_PRIMARY_ID - Thingspeak Channel ID for Primary Data
#    - THINGSPEAK_PRIMARY_ID_READ_KEY - Thingspeak Read Key for Primary Data
#    - THINGSPEAK_SECONDARY_ID - Thingspeak Channel ID for Secondary Data
#    - THINGSPEAK_SECONDARY_ID_READ_KEY - Thingspeak Read Key for Secondary Data
#    - Lat - Latitude Position Info
#    - Lon - Longitude Position Info
#    - PM2_5Value - Current PM2.5 Value
#    - LastSeen - <NOT USED>
#    - State - <NOT USED>
#    - Type - Sensor Type (PMS5003, PMS1003, BME280, etc.)
#    - Hidden - Hide from public view on map: true/false
#    - Flag - Data flagged for unusally high readings
#    - DEVICE_BRIGHTNESS - <NOT USED>
#    - DEVICE_HARDWAREDISCOVERED - <NOT USED>
#    - DEVICE_FIRMWAREVERSION - <NOT USED>
#    - Version - <NOT USED>
#    - LastUpdateCheck - <NOT USED>
#    - Uptime - <NOT USED>
#    - RSSI - <NOT USED>
#    - isOwner - Currently logged in user is the sensor owner
#    - A_H - True if sensor output is downgraded or marked for hardware issues
#    - temp_f - Current temperature in F
#    - humidity - Current humidity in %
#    - pressure - Current pressure in Millibars
#    - AGE - Sensor data age (when data was last received) in minutes
#    - Stats - Secondary json blob containing the following data:
#      - v - Real time or current PM2.5 value
#      - v1 - Short term (10 minute average)
#      - v2 - 30 minute average
#      - v3 - 1 hour average
#      - v4 - 6 hour average
#      - v5 - 24 hour average
#      - v6 - One week average
#      - pm - Real time or current PM2.5 Value
#      - lastModified - Last modified time stamp for averages
#      - timeSinceModified - Time between last two readings in milliseconds
# The script then populate the database table with data retrieved for a list of
# stations hard-coded into this script.
#
##########################################################################

##########################################################################
#
# Python imports - Equivalent to includes in c.
#
##########################################################################
import sys
import json
import requests
import mysql.connector
from datetime import datetime

##########################################################################
#
# Read the command line argument and ensure it is valid.
#  - As a reminder from the description above, this selects which
#    database to store the current purple air data to.
#
##########################################################################
TABLE_NAME = ""

if len(sys.argv) != 2:
    print("Invalid number of arguments!")
    print("  USAGE: script.py table_name")
    exit()
else:
    TABLE_NAME = sys.argv[1]



##########################################################################
#
# Get a list of all the monitor ids that we want data from.
#
##########################################################################
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
    for x in i["Stations"]:
        a_channel = x
        total_ids.append(a_channel)

MONITOR_IDS = total_ids


##########################################################################
#
# For Each Monitor ID, Get data the latest data from purpleair.com
#
##########################################################################
PURPLE_AIR_WEBSITE = 'https://www.purpleair.com/json'



import requests

import json

 

# Sort method for the monitor list by id.

def sortParam(elem):

    return elem[0]

 

# List all the sensor fields that we want to retrieve from Purple Air.

Sensor_Fields = [

    "last_seen",        # AGE (last time the sensor updated data)

    "pm2.5_a",            # pm - Real time or current PM2.5 Value

    "pm2.5_b"

]

 

# List all the fields in url format in a single string.

field_list_string = "last_modified"

for field in Sensor_Fields:

    field_list_string += "%2C" + field

 

url = 'https://api.purpleair.com/v1/sensors' + '?fields=' + field_list_string + '&nwlng=-139.06&nwlat=60&selng=-114.03&selat=48.3'

headers = {'content-type': 'application/json', 'X-API-Key': '5901141D-E28E-11EC-8561-42010A800005'}

 

req = requests.Request('Get',url,headers=headers,data='')

prepared = req.prepare()

 

s = requests.Session()

response = s.send(prepared)

 

monitor_list = []

monitor_array = []

 

if response.status_code != 200:

    print('Request Failed: ' + response.status_code)

    print(response.reason)

else:

    json_data = json.loads(response.text)

    raw_monitor_data = json_data['data']

    raw_monitor_data.sort(key=sortParam)

    for monitor in raw_monitor_data:
        i = 0

        print("*******************************\n")

        for x in monitor :
            print(f"Item: #{i}, Value: {x} \n")
            i += 1
        
        print("*******************************\n")
        print(monitor)


    for monitor in raw_monitor_data:

        monitor_list.append(monitor[0])

        monitor_dict_a = {}
        monitor_dict_b = {}

        monitor_dict_a['ID'] = monitor[0]
        monitor_dict_a['ParentID'] = "null"
        monitor_dict_a["PM2_5Value"] = monitor[3]
        monitor_dict_a["AGE"] = 0

        monitor_dict_b['ID'] = (monitor[0] + 1)
        monitor_dict_b['ParentID'] = monitor[0]
        monitor_dict_b["PM2_5Value"] = monitor[4]
        monitor_dict_b["AGE"] = 0



        monitor_array.append(monitor_dict_a)
        monitor_array.append(monitor_dict_b)


##########################################################################
#
# Connect to the MYSQL database on this machine, check to see if the selected
# table exists.  If it does not exist, create it.
#
##########################################################################
# Connect to the mysql database.
mydb = mysql.connector.connect(
    host="localhost",
    user="airdata",
    passwd="AESl0uis!",
    database="airdata"
)
mycursor = mydb.cursor()

def dropTable(table):
  sql_del = f"DROP TABLE IF EXISTS {table}"
  print(sql_del)
  mycursor.execute(sql_del)
  mydb.commit()

# Check if the purpleair table has been created.
mycursor.execute("SHOW TABLES")
table_exists = False
for table_name in mycursor:
    if table_name[0] == TABLE_NAME:
        table_exists = True

# Create a string to is the MYSQL command to create the desired table.
MYSQL = "CREATE TABLE " + TABLE_NAME + " ("
MYSQL = MYSQL + "ID INT" + ", "
MYSQL = MYSQL + "ParentID VARCHAR(10)" + ", "
MYSQL = MYSQL + "PM2_5Value FLOAT" + ", "
MYSQL = MYSQL + "AGE INT" + ", "
MYSQL = MYSQL + "lastModified DATETIME" + ") "

# Create the table in the database using the mysql command from above.
if not table_exists:
    mycursor.execute(MYSQL)
    print("Create Table: ", TABLE_NAME)


#Create Current Readings Table

dropTable("current_readings")

# Create a string to is the MYSQL command to create the desired table.
MYSQL = "CREATE TABLE current_readings ("
MYSQL = MYSQL + "ID INT" + ", "
MYSQL = MYSQL + "ParentID VARCHAR(10)" + ", "
MYSQL = MYSQL + "PM2_5Value FLOAT" + ", "
MYSQL = MYSQL + "AGE INT" + ", "
MYSQL = MYSQL + "lastModified DATETIME" + ", "
MYSQL = MYSQL + "UNIQUE (ID));"

mycursor.execute(MYSQL)
print("Create Table: ", TABLE_NAME)


##########################################################################
#
# Insert data from each monitor into the SQL database.
#
##########################################################################

for monitor in monitor_array:
    # Get the timestamp from the monitor data and convert to SQL date format.
    dt = datetime.fromtimestamp(monitor["lastModified"] / 1000)

    # Initialize two variables for assigning region
    id_val = monitor["ID"]
    # This Value will be used for B channel Monitors
    channel_val = (id_val - 1)
    # Default region
    monitor_region = 'none'

    # Assign the region to the variable 'monitor_region'
    # based on which region the ID falls under
    for i in ID_list:
        if id_val in i["Stations"]:
            monitor_region = i["Name"]
        elif channel_val in i["Stations"]:
            monitor_region = i["Name"] + ' B'

    print("MONITOR REGION IS:", monitor_region)

    # Create SQL string to insert a row into the database table.
    sql = "INSERT INTO " + TABLE_NAME + " (ID, ParentID, PM2_5Value, AGE, lastModified) VALUES (%s, %s, %s, %s, %s)"
    sql2 = "INSERT INTO current_readings (ID, ParentID, PM2_5Value, AGE, lastModified) VALUES (%s, %s, %s, %s, %s)"
    
    # Create a list of the data we are going to insert into the table.
    val = (
            str(monitor.get("ID", 0)), 
            str(monitor.get("ParentID", "null")),
            str(monitor.get("PM2_5Value", -1)),
            str(monitor.get("AGE", 0)), 
            dt)

    # Insert the data into the table.
    print("**********************INSERTING DATA**********************\n", sql, val)
    mycursor.execute(sql, val)
    mydb.commit()

    # Insert the data into the table.
    print("**********************INSERTING DATA**********************\n", sql2, val)
    mycursor.execute(sql2, val)
    mydb.commit()

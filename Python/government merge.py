import requests
import csv
import json
import sys
import mysql.connector
from datetime import datetime

##########################################################################
#
# Get raw csv data from BC Government website.  This script should be
# run once per hour as that is the frequency that the csv is updated.
#
##########################################################################
BC_GOVERNMENT_WEBSITE = 'http://www.env.gov.bc.ca/epd/bcairquality/aqo/csv/bc_air_monitoring_stations.csv'
response = requests.get(BC_GOVERNMENT_WEBSITE)
raw_data = response.text


##########################################################################
#
# Define all the components of the header row.  We hard-code this so
# that we can verify that the csv data does not change.   If it has
# changed we will output an error message.
#
##########################################################################
header_row = ['SERIAL_CODE', 'EMS_ID', 'STATION_NAME', 'LOCATION', 'CITY', 'CATEGORY', 'STATION_ENVIRONMENT', 'STATION_OWNER', 'DATE_ESTABLISHED', 'NOTES', 'LATITUDE', 'LONGITUDE', 'HEIGHT(m)', 'STATUS', 'URL', 'URL2', 'PM25_INSTRUMENT', 'PM25', 'PM25_UNIT', 'NO', 'NO_UNIT', 'NO2', 'NO2_UNIT', 'NOX', 'NOX_UNIT', 'O3', 'O3_UNIT', 'PM10', 'PM10_UNIT', 'SO2', 'SO2_UNIT', 'TRS', 'TRS_UNIT', 'H2S', 'H2S_UNIT', 'WDIR_VEC', 'WDIR_UNIT', 'WSPD_VEC', 'WSPD_UNIT', 'TEMP', 'TEMP_UNIT', 'HUMIDITY', 'HUMIDITY_UNIT', 'PRECIPITATION', 'PRECIPITATION_UNIT', 'BAR_PRESSURE', 'PRESSURE_UNIT', 'SNOWDEPTH', 'SNOWDEPTH_UNIT', 'CO', 'CO_UNIT', 'PM25_24', 'NO_24', 'NO2_24', 'NOX_24', 'O3_8', 'PM10_24', 'SO2_24', 'TRS_24', 'H2S_24', 'DATE', 'DATE_PST', 'URL_Station']


##########################################################################
#
# Use the csv module to load the raw_data into a dictionary.
#
##########################################################################
reader = csv.reader(raw_data.splitlines())
row_count = 0
aq_stations = []
for row in reader:
    if (row_count == 0):
        if header_row != row:
            print("The BC government air quality csv file has changed!  No data read!")
            break
    else:
        station_dict = dict(zip(header_row,row))
        aq_stations.append(station_dict)

    row_count = row_count + 1


##########################################################################
#
# Parse the AQ Stations and create a new list where stations actually
# have data.   i.e. remove stations with blank p26 values.
#
##########################################################################
valid_aq_stations = []
for station in aq_stations:
    if station['PM25']:
       valid_aq_stations.append(station)

# Sort the monitor list by ID.
def sortParam(elem):
    return int(elem['SERIAL_CODE'])
valid_aq_stations.sort(key=sortParam)

# Print-out stations and exit as a test.
#for station in valid_aq_stations:
#    print(station['SERIAL_CODE'] + ' ' + station['STATION_NAME'] + ' ' + station['PM25'])
#exit()


##########################################################################
#
# Create the SQL Table to store the Government air quality data.
#
##########################################################################
TABLE_NAME = 'monitor_data'

# Connect to the mysql database.
mydb = mysql.connector.connect(
    host="localhost",
    user="airdata",
    passwd="AESl0uis!",
    database="airdata"
)
mycursor = mydb.cursor()

# Check if the database table has been created or not.
mycursor.execute("SHOW TABLES")
table_exists = False
for table_name in mycursor:
    if table_name[0] == TABLE_NAME:
        table_exists = True

# Create a string to is the MYSQL command to create the desired table.
# I will do this one table column at a time so that it is easy to
# follow.   In the end the create table command should look something
# like: "CREATE TABLE monitor_data (ID INT, PM2_5 FLOAT, lastModified DATETIME)"
# but with more fields of course.
MYSQL = "CREATE TABLE " + TABLE_NAME + " ("
MYSQL = MYSQL + "ID INT" + ", "
MYSQL = MYSQL + "Region VARCHAR(128)" + ", "
MYSQL = MYSQL + "ParentID VARCHAR(10)" + ", "
MYSQL = MYSQL + "Label VARCHAR(128)" + ", "
#    - DEVICE_LOCATIONTYPE - <NOT USED> - maybe VARCHAR(20)
MYSQL = MYSQL + "THINGSPEAK_PRIMARY_ID INT" + ", "
MYSQL = MYSQL + "THINGSPEAK_PRIMARY_ID_READ_KEY VARCHAR(20)" + ", "
MYSQL = MYSQL + "THINGSPEAK_SECONDARY_ID INT" + ", "
MYSQL = MYSQL + "THINGSPEAK_SECONDARY_ID_READ_KEY VARCHAR(20)" + ", "
MYSQL = MYSQL + "Lat FLOAT" + ", "
MYSQL = MYSQL + "Lon FLOAT" + ", "
MYSQL = MYSQL + "PM2_5Value FLOAT" + ", "
#MYSQL = MYSQL + "LastSeen DATETIME" + ", "
#    - State - <NOT USED> - maybe VARCHAR(20)
MYSQL = MYSQL + "Type VARCHAR(64)" + ", "
MYSQL = MYSQL + "Hidden VARCHAR(10)" + ", "
MYSQL = MYSQL + "Flag VARCHAR(10)" + ", "
#    - DEVICE_BRIGHTNESS - <NOT USED> - maybe VARCHAR(20)
#    - DEVICE_HARDWAREDISCOVERED - <NOT USED> - maybe VARCHAR(128)
#    - DEVICE_FIRMWAREVERSION - <NOT USED> - maybe VARCHAR(20)
#    - Version - <NOT USED> - maybe VARCHAR(10)
#    - LastUpdateCheck - <NOT USED> - maybe VARCHAR(20)
#    - Uptime - <NOT USED> - maybe INT
#    - RSSI - <NOT USED> - maybe INT
MYSQL = MYSQL + "isOwner INT" + ", "
MYSQL = MYSQL + "A_H VARCHAR(10)" + ", "
MYSQL = MYSQL + "temp_f FLOAT" + ", "
MYSQL = MYSQL + "humidity FLOAT" + ", "
MYSQL = MYSQL + "pressure FLOAT" + ", "
MYSQL = MYSQL + "AGE INT" + ", "
MYSQL = MYSQL + "v FLOAT" + ", "  # - Current Value
MYSQL = MYSQL + "v1 FLOAT" + ", "  # - 10 Min Avg
MYSQL = MYSQL + "v2 FLOAT" + ", "  # - 30 Min Avg
MYSQL = MYSQL + "v3 FLOAT" + ", "  # - 1 Hr Avg
MYSQL = MYSQL + "v4 FLOAT" + ", "  # - 6 Hr Avg
MYSQL = MYSQL + "v5 FLOAT" + ", "  # - 24 Hr Avg
MYSQL = MYSQL + "v6 FLOAT" + ", "  # - 1 Wk Avg
MYSQL = MYSQL + "pm FLOAT" + ", "  # - Current Value
MYSQL = MYSQL + "lastModified DATETIME" + ", "
MYSQL = MYSQL + "timeSinceModified BIGINT" + ")"


# Create the table in the database using the mysql command from above.
if not table_exists:
    mycursor.execute(MYSQL)
    print("Create Table: ", TABLE_NAME)


##########################################################################
#
# Insert data from each monitor into the SQL database.
#
##########################################################################
for station in valid_aq_stations:
    # Get the region data for the station
    id_val = station['SERIAL_CODE']
    monitor_region = 'Gov'

    # Create SQL string to insert a row into the database table.
    sql = "INSERT INTO " + TABLE_NAME + " (ID, Label, Region, Lat, Lon, PM2_5Value, v, lastModified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    sql_cur = "INSERT INTO current_data (ID, Label, Region, Lat, Lon, PM2_5Value, v, lastModified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ID=VALUES(ID)"

    # Create a list of the data we are going to insert into the table.
    val = ( 
            str(station.get("SERIAL_CODE", 0)),
            str(station.get("STATION_NAME", "null")),
            monitor_region,
            str(station.get("LATITUDE", 0.0)),
            str(station.get("LONGITUDE", 0.0)),
            str(station.get("PM25", 0.0)),
            str(station.get("PM25_24", 0.0)),
            str(station.get("DATE_PST", "null"))
          )

    # Insert the data into the table.
    print("**********************INSERTING DATA**********************\n", sql, val)
    mycursor.execute(sql, val)
    mycursor.execute(sql_cur, val)
    mydb.commit()

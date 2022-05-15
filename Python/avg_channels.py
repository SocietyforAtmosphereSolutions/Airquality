import sys
import json
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="airdata",
    passwd="AESl0uis!",
    database="airdata"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM current_data")

desc = mycursor.description
column_names = [col[0] for col in desc]
data = [dict(zip(column_names, row))
        for row in mycursor.fetchall()]
avg_data = []

for b in data:
    if b["Region"] == "Gov":
        print("adding " + str(b["ID"]))
        avg_data.append(x)
    elif b["ParentID"] == "null":
        print("skipping " + str(b["ID"]))
        continue
    else:
        print("adding " + str(b["ID"]))
        for a in data:
            if float(a["ID"]) == float(b["ParentID"]):
                print("matched " + str(a["ID"]))
                x = a
                if (float(a["PM2_5Value"]) - float(b["PM2_5Value"])) >= 10:
                    print(str(a["PM2_5Value"]) +
                          "is bigger than " +
                          str(b["PM2_5Value"]) +
                          " picking " +
                          str(b["PM2_5Value"]))
                    x["PM2_5Value"] = b["PM2_5Value"]
                    x["v"] = b["v"]
                    x["v1"] = b["v1"]
                    x["v2"] = b["v2"]
                    x["v3"] = b["v3"]
                    x["v4"] = b["v4"]
                    x["v5"] = b["v5"]
                    x["v6"] = b["v6"]
                elif (float(a["PM2_5Value"]) - float(b["PM2_5Value"])) <= -10:
                    # print(str(b["PM2_5Value"]) +
                    #       "is bigger than " +
                    #       str(a["PM2_5Value"]) +
                    #       " picking " +
                    #       str(a["PM2_5Value"]))
                    x["PM2_5Value"] = a["PM2_5Value"]
                    x["v"] = a["v"]
                    x["v1"] = a["v1"]
                    x["v2"] = a["v2"]
                    x["v3"] = a["v3"]
                    x["v4"] = a["v4"]
                    x["v5"] = a["v5"]
                    x["v6"] = a["v6"]
                else:
                    # print("Averaging")
                    x["PM2_5Value"] = (
                        (float(a["PM2_5Value"]) + float(b["PM2_5Value"])) / 2)
                    x["v"] = round(((float(a["v"]) + float(b["v"])) / 2), 1)
                    x["v1"] = round(((float(a["v1"]) + float(b["v1"])) / 2), 1)
                    x["v2"] = round(((float(a["v2"]) + float(b["v2"])) / 2), 1)
                    x["v3"] = round(((float(a["v3"]) + float(b["v3"])) / 2), 1)
                    x["v4"] = round(((float(a["v4"]) + float(b["v4"])) / 2), 1)
                    x["v5"] = round(((float(a["v5"]) + float(b["v5"])) / 2), 1)
                    x["v6"] = round(((float(a["v6"]) + float(b["v6"])) / 2), 1)
                # print(a, b, x)
                avg_data.append(x)
                # print(avg_data)
del_current = 'DELETE FROM cur_avg_data;'
print('Wiping cur_avg_data')
mycursor.execute(del_current)
mydb.commit()
for monitor in avg_data:
    sql = "INSERT INTO cur_avg_data (ID, ParentID, Label, THINGSPEAK_PRIMARY_ID, THINGSPEAK_PRIMARY_ID_READ_KEY, THINGSPEAK_SECONDARY_ID, THINGSPEAK_SECONDARY_ID_READ_KEY, Lat, Lon, PM2_5Value, Type, Hidden, Flag, isOwner, A_H, temp_f, humidity, pressure, AGE, v, v1, v2, v3, v4, v5, v6, pm, lastModified, timeSinceModified, Region) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (
        str(
            monitor.get(
                "ID", 0)), str(
            monitor.get(
                "ParentID", "null")), str(
            monitor.get(
                "Label", "null")), str(
            monitor.get(
                "THINGSPEAK_PRIMARY_ID", 0)), str(
            monitor.get(
                "THINGSPEAK_PRIMARY_ID_READ_KEY", "null")), str(
            monitor.get(
                "THINGSPEAK_SECONDARY_ID", 0)), str(
            monitor.get(
                "THINGSPEAK_SECONDARY_ID_READ_KEY", "null")), str(
            monitor.get(
                "Lat", 0)), str(
            monitor.get(
                "Lon", 0)), str(
            monitor.get(
                "PM2_5Value", 0)),  str(
            monitor.get(
                "Type", "null")), str(
            monitor.get(
                "Hidden", "null")), str(
            monitor.get(
                "Flag", "null")), str(
            monitor.get(
                "isOwner", 0)), str(
            monitor.get(
                "A_H", "null")), str(
            monitor.get(
                "temp_f", 0)), str(
            monitor.get(
                "humidity", 0)), str(
            monitor.get(
                "pressure", 0)), str(
            monitor.get(
                "AGE", 0)), str(
            monitor.get(
                "v", 0)), str(
            monitor.get(
                "v1", 0)), str(
            monitor.get(
                "v2", 0)), str(
            monitor.get(
                "v3", 0)), str(
            monitor.get(
                "v4", 0)), str(
            monitor.get(
                "v5", 0)), str(
            monitor.get(
                "v6", 0)), str(
            monitor.get(
                "pm", 0)), str(
            monitor.get(
                "lastModified", "null")), str(
            monitor.get(
                "timeSinceModified", "null")), str(
            monitor.get(
                "Region", "null")))

    #print("**********************INSERTING DATA**********************\n", sql, val)
    mycursor.execute(sql, val)
    mydb.commit()

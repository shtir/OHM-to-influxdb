#!/usr/bin/env python
import datetime
import psutil
from influxdb import InfluxDBClient
import json
import requests

# influx configuration - edit these
ifuser = "grafana"
ifpass = "grafana"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "system_data"

# get data.json from PC 
url = "http://192.168.88.12:8085/data.json"

try:
    file = requests.get(url)
except requests.exceptions.RequestException as e:  # This is the correct syntax
    raise SystemExit(e)
data = json.loads(file.content)

def checkData(data,Text, Children):
    try:
        for data in data['Children']:
            if (data['Text']==Text):
                for data in data['Children']:
                    if (data['Text']==Children):
                        return (data['Value'])
            else:
                result = (checkData(data, Text, Children))
                if (result):
                    return(result)
    except NameError:
        print("well, it WASN'T defined after all!")



# take a timestamp for this measurement
time = datetime.datetime.utcnow()

# format the data as a single measurement for influx
body = [
    {
        "measurement": measurement_name,
        "time": time,
        "fields": {
            "CPU Temperatures": float(checkData(data,"Temperatures", "CPU Package").split('°C')[0]),
            "GPU Temperatures": float(checkData(data,"Temperatures", "GPU Core").split('°C')[0]),
            "CPU Load": float(checkData(data,"Load", "CPU Total").split('%')[0]),
            "GPU Load": float(checkData(data,"Load", "GPU Core").split('%')[0]),

        }
    }
]

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
ifclient.write_points(body)



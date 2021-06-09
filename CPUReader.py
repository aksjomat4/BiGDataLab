#!/usr/bin/env python3

import psutil  #library for retrieving information on running processes and system utilization
import requests
import sched, time

# Simple psutil test
# for x in range(3):
#   print("CPU usage:", psutil.cpu_percent(interval=1))
#   print("Cores number:", psutil.cpu_count())
#   print("CPU load:", psutil.getloadavg())

# Create scheduler to run every n seconds
s = sched.scheduler(time.time, time.sleep)
interval = 60


# Definition to read data and send it to ThingSpeak
def read_and_send(sc):
    # Using psutil module set the query string
    queries = {
        "api_key": "PE0X9V27HN8PX92U", #my write key
        "field1": psutil.cpu_percent(interval=1),
        "field2": psutil.getloadavg(),
    }
    # Send the request to ThingSpeak
    r = requests.get('https://api.thingspeak.com/update', params=queries)
    # Verify that ThingSpeak recived our data
    if r.status_code == requests.codes.ok:
        print("Data Recived!")
    else:
        print("Error Code: " + str(r.status_code))
    # Re-add this definition to run again in n seconds
    s.enter(interval, 1, read_and_send, (sc, ))


# Add read_and_send task to the scheduler and run it.
s.enter(interval, 1, read_and_send, (s, ))
s.run()
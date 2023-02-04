#!/usr/bin/env python3

import time
from  bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

import logging

import requests
import time
from datetime import datetime




logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp


# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up


#first temp is flakey. Skip some just in case
def getTemp():
    factor = 2.25
    cpu_temps = [get_cpu_temperature()] * 5
    counter = 5
    while counter > 0:
        counter = counter - 1
        cpu_temp = get_cpu_temperature()
        # Smooth out with some averaging to decrease jitter
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = bme280.get_temperature()
        comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor) - 5
        time.sleep(0.1)
    return comp_temp


api_url = "https://temperature-ugdebiz6jq-uc.a.run.app"
#api_url = "http://127.0.0.1:5001/bvik-370610/us-central1/temperature"

def try_post(url):
    reportTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report =  { "reporter":"bvik1", "datetime":reportTime, "temp":"{:05.2f}".format(getTemp())}
    print(report)
    try:
       response = requests.post(url, json=report)
    except requests.exceptions.RequestException as e:
       print("Cannot connect")
       print(e);
       # TODO: cancellation logic to return False
       return 5
    else:
       return 60*10

while True:
    timeout = try_post(api_url)
    time.sleep(timeout)


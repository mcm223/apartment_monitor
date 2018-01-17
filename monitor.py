###
# Environment Monitor
# Checks temp/humdity reports image
# for use in a local webserver.
# Script is autorun from /etc/xdg/lxsession/LXDE-pi/autostart
# sudo /usr/bin/python /home/pi/apartment_monitor/monitor.py
###

import Adafruit_DHT
import datetime
import time
import json
import picamera
import boto3
from array import array
from functools import reduce

# Global variables
sensor = Adafruit_DHT.AM2302
todaysHigh = None
todaysLow = None
avgTemp = 0.0
avgHum = 0.0
today = datetime.date.today()

# GPIO Input
# Really pin 7, but GPIO 4
pin = 4

# Initialize arrays
tempArr = array('f',[])
humArr = array('f',[])

# Initialize camera
c = picamera.PiCamera()
c.hflip = True
c.vflip = True

# Initialize S3 Session
# Credentials stored as env variables locally
s3 = boto3.resource('s3')
bucket = 'apt-monitor'

def averageArray(input):
    sum = reduce((lambda x, y: x + y), input)
    avg = sum / len(input)
    return avg   

def uploadFileToS3(path,contentType):
    data = open(path,'rb')
    s3.Bucket(bucket).put_object(Key=path, Body=data, ContentType=contentType, ACL='public-read')

# Continuously get readings and keep five values in array for averaging to smooth outliers
for x in range(0,5):
    # Check if day has turned over or need to initialize high/low values
    if todaysHigh is None or todaysLow is None or today < datetime.date.today():
        prevHumidity, prevTemperature = Adafruit_DHT.read_retry(sensor, pin)
        prevTemperature = ((prevTemperature * (9.0/5.0))+32.0)
        todaysHigh = prevTemperature
        todaysLow = prevTemperature
        today = datetime.date.today()

    # Get new reading
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Sensor may occasionally reject read
    if humidity is not None and temperature is not None:

        # Convert to fahrenheit
        temperature = ((temperature * (9.0/5.0))+32.0)

        # Compare values to keep a running high and low for the day
        if temperature > todaysHigh:
            todaysHigh = temperature
        if temperature < todaysLow:
            todaysLow = temperature

        # Process temperature
        if len(tempArr) == 5:
            tempArr.pop(0)
        tempArr.append(temperature)
        avgTemp = averageArray(tempArr)

        # Process humidity
        if len(humArr) == 5:
            humArr.pop(0)
        humArr.append(humidity)
        avgHum = averageArray(humArr)
    else:
        print('Failed to get reading.')
    #print('The current date is: ' + str(today))
    #print('The current temp is {0:0.1f}*. The current humidity is {1:0.1f}%.'.format(temperature, humidity))
    #print('Todays High is {0:0.1f}*. Todays Low is {1:0.1f}*.'.format(todaysHigh, todaysLow))

    # Write JSON to file
    with open('/var/www/html/js/output.json','w') as outfile:
        json.dump({'currentTemp': avgTemp,
                   'currentHumidity': avgHum,
                   'today': str(today),
                   'todaysHigh': todaysHigh,
                   'todaysLow': todaysLow}, outfile)

    # Snap a pic
    c.annotate_text = str(datetime.datetime.now())
    c.capture('/var/www/html/images/latestPic.jpg', resize=(960,540))

    # Upload to S3
    uploadFileToS3('/var/www/html/js/output.json','application/json')
    uploadFileToS3('/var/www/html/images/latestPic.jpg','image/jpeg')

    # Capture once a minute
    time.sleep(10)




import Adafruit_DHT
import datetime
import time
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

def averageArray(input):
    sum = reduce((lambda x, y: x + y), input)
    avg = sum / len(input)
    return avg   

# Continuously get readings and keep five values in array for averaging to smooth outliers
for x in range(0,5):
    # Check if day has turned over or need to initialize high/low values
    if todaysHigh is None or todaysLow is None or today < datetime.date.today():
        print('Resetting values!')
        prevHumidity, prevTemperature = Adafruit_DHT.read_retry(sensor, pin)
        prevTemperature = ((prevTemperature * (9.0/5.0))+32.0)
        todaysHigh = prevTemperature
        print(todaysHigh)
        todaysLow = prevTemperature
        print(todaysLow)
        today = datetime.date.today()

    # Get new reading
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Sensor may occasionally reject read
    if humidity is not None and temperature is not None:

        # Convert to fahrenheit
        temperature = ((temperature * (9.0/5.0))+32.0)

        # Compare values to keep a running high and low
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
    print('The current date is: ' + str(today))
    print('The current temp is {0:0.1f}*. The current humidity is {1:0.1f}%.'.format(temperature, humidity))
    print('Todays High is {0:0.1f}*. Todays Low is {1:0.1f}*.'.format(todaysHigh, todaysLow))
    time.sleep(5)




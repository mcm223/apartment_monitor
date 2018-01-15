import Adafruit_DHT
import time
from array import array
from functools import reduce

# Global variables
sensor = Adafruit_DHT.AM2302
todaysHigh = 0.0
todaysLow = 0.0
avgTemp = 0.0
avgHum = 0.0

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

# Get baseline temp for comparing today's high and low
prevHumidity, prevTemperature = Adafruit_DHT.read_retry(sensor, pin)
prevTemperature = ((prevTemperature * (9.0/5.0))+32.0)
todaysHigh = prevTemperature
todaysLow = prevTemperature

# Continuously get readings and keep five values in array for averaging to smooth outliers
for x in range(0,10):
    # Get reading
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
    print('The current temp is {0:0.1f}*. The current humidity is {1:0.1f}%.'.format(temperature, humidity))
    print('Todays High is {0:0.1f}*. Todays Low is {1:0.1f}*.'.format(todaysHigh, todaysLow))
    time.sleep(5)




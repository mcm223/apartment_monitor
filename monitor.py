import Adafruit_DHT
import time
from array import array

# Adafruit variables
sensor = Adafruit_DHT.AM2302

# GPIO Input
# Really pin 7, but GPIO 4
pin = 4

# Initialize arrays
tempArr = array('f',[])
humArr = array('f',[])

for x in range(0,10):
    # Get reading
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Convert temp to Fahrenheit
    if humidity is not None and temperature is not None:
        temperature = ((temperature * (9.0/5.0))+32.0)
        if len(tempArr) == 5:
            tempArr.pop(0)
        tempArr.append(temperature)
        if len(humArr) == 5:
            humArr.pop(0)
        humArr.append(humidity)
        print(tempArr)
        # print(humArr)
    else:
        print('Failed to get reading.')
    time.sleep(5)


# print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))


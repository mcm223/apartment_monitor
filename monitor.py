import Adafruit_DHT

# Adafruit variables
sensor = Adafruit_DHT.AM2302

# GPIO Input
# Really pin 7, but GPIO 4
pin = 4

# Get reading
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Convert temp to Fahrenheit
if humidity is not None and temperature is not None:
    temperature = ((temperature * (9.0/5.0))+32.0)
else:
    print('Failed to get reading.')
    continue


print(humidity)
print(temperature)


import Adafruit_DHT, urllib2, os, urllib

server   = os.getenv('TWOX_LOG_SERVER')
location = os.getenv('TWOX_LOG_DHT11_LOCATION')
sensor	 = Adafruit_DHT.DHT11
gpio	 = int(os.getenv('TWOX_DHT11_PIN'))

# Do a number of readings, and store the result
hs = []
ts = []
# Retrieve 
for i in range(10) :
    h, t = Adafruit_DHT.read_retry(sensor, gpio)
    print("Warming up!")
for i in range(20) :
    h, t = Adafruit_DHT.read_retry(sensor, gpio)
    print('Humidity ' + str(h) + '%, Temperature ' + str(t) + 'C') 
    hs.append(h)
    ts.append(t)

# Calculate the average from our set of readings
humidity    = reduce(lambda x, y: x + y, hs) / len(hs) 
temperature = reduce(lambda x, y: x + y, ts) / len(ts)

# Log the values
args = {'location': location, 'event': 'temperature', 'value': temperature}
response = urllib2.urlopen('http://' + server + '/log/?' + urllib.urlencode(args))
args = {'location': location, 'event': 'humidity', 'value': humidity}
response = urllib2.urlopen('http://' + server + '/log/?' + urllib.urlencode(args))



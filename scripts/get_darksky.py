#!/usr/local/bin/python

import datetime, json, time, urllib, pytz, os

# These are the Darksky credentials and location, set in .bashrc
key = os.environ.get('DARKSKY_KEY')
lat = os.environ.get('DARKSKY_LATITUDE')
lon = os.environ.get('DARKSKY_LONGITUDE')
lim = float(os.environ.get('DARKSKY_PRECIPITATION_LIMIT'))

# Request data from darksky.net
url = 'https://api.darksky.net/forecast/' + key + '/' + lat + ',' + lon + '?units=si'
response = urllib.urlopen(url)
data = json.loads(response.read())

# Save the data so that we can access it locally
filename = '/var/www/html/darksky/index.html'
with open(filename, 'w') as outfile:
    json.dump(data, outfile)

# Extract the sunrise and sunset - if sunset/sunrise has happend, show the next one. 
sunset = data['daily']['data'][0]['sunsetTime']
if (time.time() - sunset > 0): sunset = data['daily']['data'][1]['sunsetTime']
sunrise = data['daily']['data'][0]['sunriseTime']
if (time.time() - sunrise > 0): sunrise = data['daily']['data'][1]['sunriseTime']

# Convert to a usable format
london  = pytz.timezone("Etc/Greenwich")
dt_rise = london.localize(datetime.datetime.fromtimestamp(int(sunrise)))
dt_set  = london.localize(datetime.datetime.fromtimestamp(int(sunset)))

sunrise = str(dt_rise.strftime('%H:%M'))
sunset = str(dt_set.strftime('%H:%M'))

#print(sunrise + ' ' + sunset)
#hourly = []
#for key, value in data['daily']['data'][0].items():
#	hourly.append(value['apparentTemperature'])
#	print(key)

hourly_temperature = []
hourly_time = []
hourly_datetime = []
hourly_precip = []
for value in data['hourly']['data']:
	hourly_temperature.append(value['apparentTemperature'])
	timez = datetime.datetime.fromtimestamp(int(value['time'])) #.strftime('%H:%M')	
	hourly_datetime.append(timez)
	hourly_time.append(value['time'])
	hourly_precip.append(value['precipProbability'])

rainindex = -1
index = 0
for value in hourly_precip:
	if ((value > lim) and (rainindex == -1)): rainindex = index
	index += 1

td = (hourly_time[rainindex] - time.time())/(3600.0)
td = round(td, 1)
nextrain = 'T-' + str(td) + 'h'
if (rainindex == -1) : nextrain = 'DRY'
if (abs(td) < 1) : nextrain = 'NOW'

scroll = nextrain + '     ' + sunrise + '     ' + sunset + '     '
print(scroll)
file = open('/var/www/html/darksky/scroll/index.html', 'w')
file.write(scroll)
file.close()

file = open('/var/www/html/darksky/sunrise/index.html', 'w')
file.write(sunrise)
file.close()

file = open('/var/www/html/darksky/sunset/index.html', 'w')
file.write(sunset)
file.close()

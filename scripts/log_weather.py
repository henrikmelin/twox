#!/usr/bin/python
import urllib2, urllib

# Get the stored sunrise time and log it
response = urllib2.urlopen('http://piserver/darksky/sunrise/')
args = {'location': 'weather', 'event': 'sunrise', 'value': response.read()}
response = urllib2.urlopen('http://piserver/log/?' + urllib.urlencode(args))

print(response)

# Get the stored sunrise time and log it
response = urllib2.urlopen('http://piserver/darksky/sunset/')
args = {'location': 'weather', 'event': 'sunset', 'value': response.read()}
response = urllib2.urlopen('http://piserver/log/?' + urllib.urlencode(args))



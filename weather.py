import urllib
import json
import os
import argparse

# get the Dark Sky API key in a cool safe way
apikey = os.environ['DARKSKY_API_KEY']

# To start, let's grab whatever arguments were passed in.
# First, we make a parser with argparse:
parser = argparse.ArgumentParser(description = 'Specify optional preferences.')
# Next, we'll define what options we'd like to, um, define
parser.add_argument('-location', '-l', help = 'specify a particular location')

# Put all those arguments into something we can use!
args = parser.parse_args()


# Let's define several locations that we may care about
locations = {'recursecenter': {'lat': '40.72078', 'lon': '-74.001119'},
             'portland_home': {'lat': '45.55902', 'lon': '-122.630664'},
             'parents':       {'lat': '47.29085', 'lon': '-122.40482'}}

# define the base URL for API calls
url = 'https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE'
# put in the details we actually need to get real information
s = url.replace('APIKEY', apikey).replace('LATITUDE', recursecenter['lat']).replace('LONGITUDE', recursecenter['lon'])

# let's keep this thing in a file-like object from the internet
f = urllib.urlopen(s)
# actually get the information out of the file-like object
data = f.read()
# turn this into a dictionary, by the power of JSON
d = json.loads(data)

minutely = d['minutely']
print 'Imminently: {0}'.format(minutely['summary'])
hourly = d['hourly']
print 'Coming up: {0}'.format(hourly['summary'])


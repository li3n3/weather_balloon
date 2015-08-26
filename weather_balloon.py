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
parser.add_argument('-location', '-l', help = 'Specify a particular location')
parser.add_argument('-timeframe', '-t', help = 'What timeframe to print out',
                    choices = ['currently', 'minutely', 'hourly', 'daily'])

# Put all those arguments into something we can use!
args = parser.parse_args()

# Let's define several locations that we may care about, but with
# slightly blurred coordinates:
locations = {'recursecenter': {'lat': '40.72078', 'lon': '-74.001119'},
             'portland_home': {'lat': '45.55902', 'lon': '-122.630664'},
             'parents':       {'lat': '47.29085', 'lon': '-122.40482'}}

# If a valid location was specified with the location flag, set that
if args.location in locations:
    target_location = args.location
# Otherwise, set a sensible default:
else:
    target_location = 'recursecenter'

# If a timeframe was specified, set that
if args.timeframe:
    target_timeframe = args.timeframe
# Otherwise, let's just get the current weather:
else:
    target_timeframe = 'currently'


# Make the location-specific URL!
def make_url(location_key):
    """ Takes a dictionary key (string) naming a location; returns a URL for the
    Dark Sky API call. Key's value should be in the `locations` dict. """
    # base URL
    url = 'https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE'
    # ooh, gross long line. TODO: learn how to de-awful this
    location_url = url.replace('APIKEY', apikey).replace('LATITUDE', locations[location_key]['lat']).replace('LONGITUDE', locations[location_key]['lon'])

    return location_url

# call make_url, get results, & put it in a file-like object
f = urllib.urlopen(make_url(target_location))
# actually get the information out of the file-like object
data = f.read()
# turn this into a dictionary, by the power of JSON
d = json.loads(data)

def print_weather():
    """oh man I just want a function that takes something and returns weather
    results like what I'm currently printing manually"""

minutely = d['minutely']
print 'Imminently: {0}'.format(minutely['summary'])
hourly = d['hourly']
print 'Coming up: {0}'.format(hourly['summary'])


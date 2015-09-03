# -*- coding: utf-8 -*-

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
parser.add_argument('--location', '-l', help = 'Specify a particular location')
parser.add_argument('--timeframe', '-t', help = 'What timeframe to print out',
                    choices = ['currently', 'minutely', 'hourly', 'daily'])

# Put all those arguments into something we can use!
args = parser.parse_args()

# Let's define several locations that we may care about, but with
# slightly blurred coordinates and a more human-friendly description:
locations = {'recursecenter': {'lat': '40.72078', 'lon': '-74.001119',
                               'longname': 'at the Recurse Center'},
             'portland_home': {'lat': '45.55902', 'lon': '-122.630664',
                               'longname': 'at home (in Portland)'},
             'parents':       {'lat': '47.29085', 'lon': '-122.40482',
                               'longname': "at your parents' house"}}
# Also! What would happen if we could search for NEW locations?!

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
    location_url = url.replace('APIKEY', apikey).\
                   replace('LATITUDE', locations[location_key]['lat']).\
                   replace('LONGITUDE', locations[location_key]['lon'])

    return location_url


# call make_url, get results, & put it in a file-like object
f = urllib.urlopen(make_url(target_location))
# actually get the information out of the file-like object
data = f.read()
# turn this into a dictionary, by the power of JSON, because we'll need it
d = json.loads(data)


def find_weather_emoji(weather_icon):
    """ Given the `icon` description, finds a suitable emoji to represent weather
    conditions, and returns it. Currently accepted values (more may be defined in
    the future): clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy,
    partly-cloudy-day, partly-cloudy-night."""

    weatherdict = {'clear-day': '🌞', 'clear-night': '🌠 🌃', 'rain': '☔️ 💦',
                   'snow': '❄️ ⛄️', 'sleet': '💧 ❄️', 'wind': '💨 🍃', 'fog': '🌁',
                   'cloudy': '☁️', 'partly-cloudy-day': '⛅️',
                   'partly-cloudy-night': '☁️ ⭐️ ☁️'}

    # grab the emoji for that weather. Conditions not found? Return cool '?'
    return weatherdict.get(weather_icon, '❔')

def alerts_info(alert_object):
    """ Takes a Dark Sky alert object (a list of dicts, one for each alert), and
    prints out the summary information with an option to display a much
    longer description. More on alert objects:
    https://developer.forecast.io/docs/v2#alerts """
    # current alerts? print each (there might be more than one)
    print "\nHey, potentially interesting news: there's at least one active " + \
          "weather alert right now.", '\n' + \
          "Info below!", '\n' + \
          "🚫 🔥 🚫 🌊 🚫 💔 🚫 🚨 🚫 🚩 🚫 ♨️ 🚫 🙅🏻 🚫 😬 🚫 "
    for alert in range(len(alert_object)):
        # print the summary
        print alert_object[alert]['title']
        # TODO: ask the user if they'd like more information instead of just
        # assuming
        print alert_object[alert]['description']

def print_weather(level_of_detail = target_timeframe):
    """ Given whatever the desired level of detail is, put together something
    kinda nice to describe the weather, then print it out. """
    if level_of_detail == 'currently':
        timeframe_word = 'current'
    elif level_of_detail == 'minutely' or level_of_detail == 'hourly':
        timeframe_word = "upcoming"
    elif level_of_detail == 'daily':
        timeframe_word = "next week's"
    else: # noooooooo
        print "Rats. Something went wrong."

    # just the summary for the requested timeframe:
    print u"In a nutshell, the {} weather {} is this: {}".format(
            timeframe_word, locations[target_location]['longname'],
            d[level_of_detail]['summary'])

    print "You know how that makes me feel? Like this: {}".format(
           find_weather_emoji(d[level_of_detail]['icon']))

    if 'alerts' in d:
        alerts_info(d['alerts'])


# and now we invoke it all!
print_weather()

import urllib
import json
import os

apikey = os.environ['DARKSKY_API_KEY']
recursecenter = {'lat': '40.72078', 'lon': '-74.001119'}
# defint the base URL for API calls
url = 'https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE'
# put in the details we actually need to get real information
s = url.replace('APIKEY', apikey).replace('LATITUDE', recursecenter['lat']).replace('LONGITUDE', recursecenter['lon'])

# let's keep this thing in a file-like object from the internet
f = urllib.urlopen(s)
# actually get the information out of the file-like object
data = f.read()
# turn this into a dictionary, by the power of JSON
d = json.loads(data)

hourly = d['hourly']
print hourly['summary']


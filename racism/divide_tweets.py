from urllib2 import urlopen
import json
import csv
from geopy.geocoders import Nominatim
from time import sleep

from itertools import islice

def getplace(lat, lon):
    url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyCo9EVZIj04To5_pTuAqP09ZwVJwS-kgps&"
    url += "latlng=%s,%s&sensor=false" % (lat, lon)
    v = urlopen(url).read()
    # sleep(1)
    j = json.loads(v)
    print j
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    return town, country


def getlatlong(place):
    # sleep(2)
    geolocator = Nominatim()
    location = geolocator.geocode(place, timeout=10)
    try:
        return location.latitude, location.longitude
    except:
        return 0, 0  

with open('racism_tweets.txt') as f:
    line = f.readline()
    while True:
        if line.startswith('Tweet number'):
            loc_line = f.next()       
            location = loc_line.partition(',')[-1].rpartition(')')[0]
            lat, lon = getlatlong(location)
            if lat != 0 :
                country = getplace(lat, lon)[1]
                file_name = country + ".txt"
                file = open(file_name, 'a')
            # print location
            tweet=''
            temp_line = f.next()
            while(not temp_line.startswith('Tweet number')):
                tweet = tweet + temp_line
                temp_line = f.next()
            # f.previous() 
            if lat != 0 :
                file.write(tweet)   
            print tweet    
from urllib2 import urlopen
import json
import csv
from geopy.geocoders import Nominatim
from time import sleep

def getplace(lat, lon):
    url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyAy5ZDFBKh9vW8-viy4z-9QeH8dWCY9OiQ&"
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
dict1={}
num=1
with open('loc_count_racism.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print num
        num=num+1
        print dict1
        place = row['loaction']
        lat, lon = getlatlong(place)
        if lat != 0 :
            country = getplace(lat, lon)[1]
            if country in dict1:
                dict1[country]=dict1[country]+int(row['count'])
            else:
                dict1[country]=int(row['count']) 

# print(getplace(51.1, 0.1))[1]
# # print(getplace(51.2, 0.1))
# print(getplace(51.3, 0.1))[1]
# print(getplace(33.7490987, -84.3901849))[1]
# print(getplace(39.7837304, -100.4458825))[1]

print dict1
"""
Emulate a Mike Wallace related biscuit consumption incident in the Bristol area. 

"""
import random
import httplib2
import json
import time
from Biscuits.BiscuitDB import randomBiscuit

#
# location of Bristol University Physics dept used as gaussian mean
# width either side of mean set to 2.5 km, implying 2.35 sigma should be around 2500 m
# 1 degree of latitude = 111256.87 m 5K = 0.044941045 degrees lat.
# 1 degree of longitude at ~51 lat = 69514.35 m  5K = 0.071927595 degrees long. 
# Assuming Mike never really goes more than 5K from the University in search of Biscuits
# 
uniLatitude, uniLongitude = (51.451379,-2.583502)
latSigma = 0.009561924468085107
longSigma = 0.015303743617021276


def realAddress(lat, long):
    """
    _realAddress_
    
    Use google maps API reverse geocoding to convert lat/long into real address
    http://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&sensor=true_or_false
    
    Pull out the full street address, if notm return something appropriately rural. 
    
    """
    h = httplib2.Http(".cache")
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=true" % (lat, long)
    resp, content = h.request(url, "GET")
    result = "a remote field somewhere near Bristol"
    if resp['status'] == '200':
        data = json.loads(content.decode())
        for d in data['results']:
            if 'street_address' in d['types']:
                result = d['formatted_address']
    return result
    
    


def biscuitIncident():
    """
    _biscuitIncident_
    
    Genarate a Biscuit incident. 
    Between 0 & six biscuits of a randomly selected type will be consumed at a location in or around the Bristol Area
    
    """
    biscuitType = randomBiscuit() 
    biscuitCount = random.randint(0, 6)
    randomLat = random.gauss(uniLatitude, latSigma)
    randomLong = random.gauss(uniLongitude, longSigma)
    return { "Biscuit" : biscuitType, "Consumed" : biscuitCount, "Location": (randomLat, randomLong) }
    
    
def formattedBiscuitIncident():
    """
    _formattedBiscuitIncident_
    
    Convert raw biscuit incident data into something fit for human consumption
    
    """
    biscuit = biscuitIncident()
    addr = realAddress(*biscuit['Location'])
    if biscuit['Consumed'] == 0:
         msg = "Metson has eaten all of Mikes {0} biscuits at {1}".format(biscuit['Biscuit'], addr)
    else:
         msg = "Mike just ate {0} {1}  biscuits at {2}".format(biscuit['Consumed'], biscuit['Biscuit'], addr) 
    return msg                                             
         







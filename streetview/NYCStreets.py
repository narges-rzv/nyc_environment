import googlemaps
from datetime import datetime
import urllib.request
import urllib.parse


def query_api(keyfile='streetview_key.secret', addresslist=['227 east 30st, NY', '220 east 30th street, NYC 10016']):
    try:
        keystr = open(keyfile).readline().strip()
    except:
        print ('create a file named streetview_key.secret, and write your API key in it.')
        return

    gmaps = googlemaps.Client(key=keystr)

    # Geocoding an address
    geocode_result = gmaps.geocode(addresslist[0])
    # print(geocode_result[0]['types'])

    return geocode_result
    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.922958, -73.994938))
    #north-west: 40.922958, -73.994938
    #south-east: 40.532201, -73.545335
    #every 0.0005 is ok. 0.0001 is better!
    print(reverse_geocode_result)

    # Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions(addresslist[0], addresslist[1], mode="walking", departure_time=now)
    # print(directions_result)


def street_view_save(address='227 east 30st, NY 10016', gmaps = None, keystr1 = None):
    if gmaps == None or keystr1 == None:
        try:
            keystr1 = open(streetview_key.secret).readline().strip()
        except:
            print ('create a file named streetview_key.secret, and write your API key in it.')
            return
        gmaps = googlemaps.Client(key=keystr1)

    geocode_result = gmaps.geocode(address)
    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="+urllib.parse.quote_plus(address)+"&key="
    MyUrl = base + keystr1
    fname = str(lat)+str(lon)+'.jpg'    
    urllib.request.urlretrieve(MyUrl, fname)
    print(fname, MyUrl)

def crowl_and_save(toplat=40.9229, toplon=-73.9949, botlat=40.5322, botlon=-73.5453, step=0.0005, keyfile1='streetview_key.secret'):
    try:
        keystr1 = open(keyfile1).readline().strip()
    except:
        print ('create a file named streetview_key.secret, and write your API key in it.')
        return
    gmaps = googlemaps.Client(key=keystr1)
    l1, l2 = toplat, toplon
    i = 0

    while l1 >= botlat:
        l1 -= step
        while l2 <= botlon:
            l2 += step
            try:
                reverse_geocode_result = gmaps.reverse_geocode((l1, l2))
                address = reverse_geocode_result[0]['formatted_address']
                print(address)
                street_view_save(address, gmaps, keystr1)                
                i += 1
                print(i)
            except:
                continue
    

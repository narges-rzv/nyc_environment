import googlemaps
from datetime import datetime
import urllib.request
import urllib.parse
from multiprocessing import Pool
import os.path
import pickle


class NYCStreetViewer(object):

    def __init__(self, keyfile='../private/streetview_key.secret'):
        try:
            self.keystr = open(keyfile).readline().strip()
        except:
            print ('create a file named streetview_key.secret, and write your API key in it.')
            return

        self.gmaps = googlemaps.Client(key=self.keystr)


    def query_api(self, addresslist=['227 east 30st, NY', '220 east 30th street, NYC 10016']):
        # try:
        #     keystr = open(keyfile).readline().strip()
        # except:
        #     print ('create a file named streetview_key.secret, and write your API key in it.')
        #     return

        # gmaps = googlemaps.Client(key=keystr)

        # Geocoding an address
        geocode_result = self.gmaps.geocode(addresslist[0])
        # print(geocode_result[0]['types'])

        return geocode_result
        # Look up an address with reverse geocoding
        reverse_geocode_result = self.gmaps.reverse_geocode((40.922958, -73.994938))
        #north-west: 40.922958, -73.994938
        #south-east: 40.532201, -73.545335
        #every 0.0005 is ok. 0.0001 is better!
        print(reverse_geocode_result)

        # Request directions via public transit
        now = datetime.now()
        directions_result = self.gmaps.directions(addresslist[0], addresslist[1], mode="walking", departure_time=now)
        # print(directions_result)


    def street_view_save(self, address='227 east 30st, NY 10016'):
        # if gmaps == None or keystr1 == None:
        #     try:
        #         keystr1 = open(streetview_key.secret).readline().strip()
        #     except:
        #         print ('create a file named streetview_key.secret, and write your API key in it.')
        #         return
        #     gmaps = googlemaps.Client(key=keystr1)

        geocode_result = self.gmaps.geocode(address)
        try:
            lat = geocode_result[0]['geometry']['location']['lat']
            lon = geocode_result[0]['geometry']['location']['lng']
        except:
            print('error with streetview:', address )
            return
        base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="+urllib.parse.quote_plus(address)+"&key="
        MyUrl = base + self.keystr
        fname = str(lat)+str(lon)+'.jpg'
        urllib.request.urlretrieve(MyUrl, fname)
        print(fname, MyUrl)


    def crowl_and_save_list(self, latlonlist=None):
        # try:
        #     keystr1 = open(keyfile1).readline().strip()
        # except:
        #     print ('create a file named streetview_key.secret, and write your API key in it.')
        #     return

        # gmaps = googlemaps.Client(key=keystr1)
        if latlonlist == None:
            y = NYCStreets.create_lat_lon_list(step=0.005, listlocs=y)

        i = 0
        for (l1, l2) in latlon:
            crowl_and_save_single( (l1, l2) )
            i += 1
            if i % 100 == 0:
                print(i, ' addresses collected.')

    def crowl_and_save_single(self, latlonitem=None):
        if self.gmaps == None or self.keystr == None:
            print('error with gmapsAPI object :( aborting.')
            return
        (l1, l2) = latlonitem
        if os.path.isfile(str(l1)+str(l2)+'.txt') :
            print (latlonitem, ' already exists.')
            return
        try:
            reverse_geocode_result = self.gmaps.reverse_geocode((l1, l2))
            address = reverse_geocode_result[0]['formatted_address']
            outfile = open(str(l1)+str(l2)+'.txt', 'w')
            outfile.write(address)
            outfile.flush(); outfile.close();
            pickle.dump(file=open(str(l1)+str(l2)+'.pkl', 'wb'), obj=reverse_geocode_result, protocol=-1)
            self.street_view_save(address)
        except:
            print('error with item:', latlonitem)


    def parallel_crowl(self, latlonlist):
        # try:
        #     keystr1 = open(keyfile1).readline().strip()
        # except:
        #     print ('create a file named streetview_key.secret, and write your API key in it.')
        #     return
        # gmaps = googlemaps.Client(key=keystr1)

        p = Pool(17)
        p.map(self.crowl_and_save_single, latlonlist)


    def create_lat_lon_list(self, toplat=40.922, toplon=-74.042, botlat=40.532, botlon=-73.545, step=0.003, listlocs = None):
        if listlocs == None:
            listlocs = []

        l1, l2 = toplat, toplon
        while l1 >= botlat:
            l1 -= step
            l2 = toplon
            while l2 <= botlon:
                l2 += step 
                if (l1, l2) not in listlocs:
                    listlocs.append((l1,l2))        
        return listlocs
    

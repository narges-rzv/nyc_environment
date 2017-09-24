import googlemaps
from datetime import datetime
import urllib.request
import urllib.parse
from multiprocessing import Pool
import os.path
import pickle
import json

class NYCStreetViewer(object):
    def __init__(self, keyfile='../private/streetview_key.secret'):
        try:
            with open(keyfile) as kf:
                self.keystr = kf.readline().strip()
        except:
            print('create a file named streetview_key.secret, and write your API key in it.')
            raise

    def street_view_save(self, latlonitem, dir_target):
        ((l1, l2), dindex) = latlonitem
        latlonStr = "{0},{1}".format(l1, l2)
        for heading in [0, 90, 180, 270]:
            parameterStr = "size=1200x800&location={0}&heading={1}&key={2}".format(latlonStr, heading, self.keystr)
            SVurl = "https://maps.googleapis.com/maps/api/streetview?"+parameterStr
            metaUrl = "https://maps.googleapis.com/maps/api/streetview/metadata?"+parameterStr
            fname = os.path.join(dir_target, "{0:09}_{1:03}.stview.jpg".format(dindex, heading))
            if os.path.exists(fname):
                print(fname, 'already exists')
            else:
                outMeta = json.loads(urllib.request.urlopen(metaUrl).read().decode('utf-8'))
                if outMeta["status"] == "OK":
                    urllib.request.urlretrieve(SVurl, fname)
                    print('finished', metaUrl)
                else:
                    print('no streetview for', metaUrl, outMeta)


    def crowl_and_save_single(self, latlonitem=None, dir_target='../dumps/'):
        if self.keystr == None:
            raise ValueError('error with gmapsAPI object :( aborting.')
        ((l1, l2), dindex) = latlonitem
        folder_a = "{0:02}".format(int(dindex) % 100)
        folder_b = "{0:02}".format(int(dindex / 100) % 100)
        dirname = os.path.join(os.path.join(str(dir_target), folder_a), folder_b)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        filename = os.path.join(dirname, "{0:09}.latlon.json".format(dindex))
        if os.path.exists(filename):
            print(filename, ' already exists.')
        else:
            try:
                with open(filename, 'w') as outfile:
                    json.dump({
                        "lat": l1,
                        "lon": l2,
                    }, outfile)
                    self.street_view_save(latlonitem, dirname)
            except:
                print('error with item:', latlonitem)
                raise

    def parallel_crowl(self, listlocs):
        p = Pool()
        p.map(self.crowl_and_save_single, listlocs)

    def load_lat_lon_list(self, picklefile='../private/lat_lon_to_sample.pkl'):
        with open(picklefile, 'rb') as pf:
            listlocs = pickle.load(pf)
            listlocs = listlocs[:10]
            return listlocs



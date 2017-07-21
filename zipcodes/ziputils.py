import csv
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def read_ascii_boundary(filestem, polygon_data={}):
    '''
    Reads polygon data from an ASCII boundary file.
    Returns a dictionary with polygon IDs for keys. The value for each
    key is another dictionary with three keys:
    'name' - the name of the polygon
    'polygon' - list of (longitude, latitude) pairs defining the main 
    polygon boundary 
    'exclusions' - list of lists of (lon, lat) pairs for any exclusions in
    the main polygon
    '''
    metadata_file = filestem + 'a.dat'
    data_file = filestem + '.dat'
    # Read metadata
    lines = [line.strip().strip('"') for line in open(metadata_file)]
    polygon_ids = lines[::6]
    polygon_names = lines[2::6]
    
    for polygon_id, polygon_name in zip(polygon_ids, polygon_names):
        # Initialize entry with name of polygon.
        # In this case the polygon_name will be the 5-digit ZIP code.
        polygon_data[polygon_id] = {'name': polygon_name}
    del polygon_data['0']
    # Read lon and lat.
    f = open(data_file)
    for line in f:
        fields = line.split()
        if len(fields) == 3:
            # Initialize new polygon
            polygon_id = fields[0]
            polygon_data[polygon_id]['polygon'] = []
            polygon_data[polygon_id]['exclusions'] = []
        elif len(fields) == 1:
            # -99999 denotes the start of a new sub-polygon
            if fields[0] == '-99999':
                polygon_data[polygon_id]['exclusions'].append([])
        else:
            # Add lon/lat pair to main polygon or exclusion
            lon = float(fields[0])
            lat = float(fields[1])
            if polygon_data[polygon_id]['exclusions']:
                polygon_data[polygon_id]['exclusions'][-1].append((lon, lat))
            else:
                polygon_data[polygon_id]['polygon'].append((lon, lat))
    return polygon_data

def load_csv_zip(filename):
    res = {}
    #implement later. return a hashtable with key=zip (string) and value=some float num

def run(zipcode_data, d, label_x='Plot number of patients', filename='tmp'):
    
    fig1 = plt.figure()
    min_x = 10000; max_x = -10000; min_y = 10000; max_y=-10000
    max_val = max(zipcode_data.values())
    min_val = min(zipcode_data.values())
    for polygon_id in d:
        polygon_data = array(d[polygon_id]['polygon'])
        zipcode = d[polygon_id]['name']
        zip_val = zipcode_data[zipcode] if zipcode in zipcode_data else 0
        patch = Polygon(array(polygon_data))
        if zipcode in zipcode_data:
            min_x = min(array(polygon_data).min(axis=0)[0], min_x)
            max_x = max(array(polygon_data).max(axis=0)[0], max_x)
            min_y = min(array(polygon_data).min(axis=0)[1], min_y)
            max_y = max(array(polygon_data).max(axis=0)[1], max_y)

    ax1 = fig1.add_subplot(1,1,1)
    #zipcode_data = load_csv(filename)
    
    cmap = cm.Blues
    # norm = colors.SymLogNorm(vmin=0, vmax=max_val, linthresh=0.03, linscale=0.03) #PowerNorm(gamma=3,
    norm = colors.Normalize(vmin=min_val, vmax=max_val)
    for polygon_id in d:
        polygon_data = array(d[polygon_id]['polygon'])
        zipcode = d[polygon_id]['name']
        zip_val = zipcode_data[zipcode] if zipcode in zipcode_data else 0
        # print(zipcode, zip_val)
        # if zip_val < 1:
        #     continue
        fc = cmap(norm(zip_val))
        #print num_births, max_births, fc
        if zipcode in zipcode_data:
            patch = Polygon(array(polygon_data), facecolor=fc, edgecolor=(.3, .3, .3, 1), linewidth=.2)
            plt1 = ax1.add_patch(patch)

    ax1.set_xlim(min_x,max_x)
    ax1.set_ylim(min_y,max_y)
    ax1.set_title(label_x)
    ax1.axis('off')

    cax = fig1.add_axes([0.93, 0.1, 0.03, 0.8])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cb1 = fig1.colorbar(sm, cax=cax, label=label_x)
    cb1.ax.tick_params(labelsize=7)
    from matplotlib import ticker
    tick_locator = ticker.MaxNLocator(nbins=10)
    cb1.locator = tick_locator
    cb1.update_ticks()

    plt.subplots_adjust(left=0.01, right=0.9, top=0.9, bottom=0.1)
    plt.show()
    plt.savefig('tmp.png')

if __name__=='__main__':
    d = read_ascii_boundary('zip_boundaries/zt36_d00')
    zipcode_data = load_csv_zip(filename)
    run(zipcode_data,d)

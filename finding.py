# -*- coding: utf-8 -*-
'''
© 2012-2013 eBay Software Foundation
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
from optparse import OptionParser

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError


def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")
    parser.add_option("-y", "--yaml",
                      dest="yaml", default='ebay.yaml',
                      help="Specifies the name of the YAML defaults file. [default: %default]")
    parser.add_option("-a", "--appid",
                      dest="appid", default=None,
                      help="Specifies the eBay application id to use.")
    parser.add_option("-n", "--domain",
                      dest="domain", default='svcs.ebay.com',
                      help="Specifies the eBay domain to use (e.g. svcs.sandbox.ebay.com).")

    (opts, args) = parser.parse_args()
    return opts, args

def get_category(category_id):
    try:
        api = finding(debug=opts.debug, appid=opts.appid, domain=opts.domain,
                      config_file=opts.yaml, warnings=True)

        api_request = {
            'categoryId': str(category_id),
            'affiliate': {'trackingId': 1},
            'sortOrder': 'CountryDescending',
        }

        response = api.execute('findItemsAdvanced', api_request)
        rep = response.dict()["searchResult"]["item"]            
        print(str(category_id))
        return rep

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        return {}

def merge_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z = z.update(y)    # modifies z with y's keys and values & returns None
    return z

def get_categories(cat_arr):
    z = []
    for i in range(0,len(cat_arr)):
        z = z + get_category(cat_arr[i])
    return z


# example usage, should be deleted if this is used  as a library
if __name__ == "__main__":
    print("Finding samples for SDK version %s" % ebaysdk.get_version())
    (opts, args) = init_options()
    print("RUN:")    
    #run(opts)
    categories = [162969, 37936, 162976, 171171]
    yeet = get_categories(categories)
    print(yeet)
    
    
    
    
    
    
    
    
    
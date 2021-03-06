# -*- coding: utf-8 -*-
'''
© 2012-2013 eBay Software Foundation
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
import random
from .predict import generate_IDs
from optparse import OptionParser
import sys

# sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

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

def get_category(category_id, opts):
    try:
        api = finding(debug=opts.debug, appid=opts.appid, domain=opts.domain,
                      config_file=opts.yaml, warnings=True)

        api_request = {
            'categoryId': str(category_id),
            'affiliate': {'trackingId': 1},
            'sortOrder': 'CountryDescending',
        }

        response = api.execute('findItemsAdvanced', api_request)
        rep = None
        try:
            rep = response.dict()["searchResult"]["item"]
        except:
            pass

        return rep

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        return {}

def merge_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z = z.update(y)    # modifies z with y's keys and values & returns None
    return z

def get_categories(cat_arr,opts):
    z = []
    for i in range(0,len(cat_arr)):
        c = get_category(cat_arr[i],opts)
        if (c is not None):
            z = z + c
    return z


# example usage, should be deleted if this is used  as a library
def use_machine_learning(token, budget):
    print("Finding samples for SDK version %s" % ebaysdk.get_version())
    (opts, args) = init_options()
    #run(opts)
    #categories = [[162922],[91101]]
    #yeet = get_categories(categories)

    categories = generate_IDs(token)
    arr = []
    for item in categories:
        if len(item)>2:
            item = random.sample(item,2)
        yeet = get_categories(item, opts)
        arr.append(yeet)

    viable_option = []
    iterator = [1] * len(arr)
    while (True):
        iterator[len(iterator)-1] += 1
        carryOver = False
        b = False
        for i in range(len(iterator)-1, -1, -1):
            if (carryOver):
                iterator[i] += 1
            if iterator[i] >= len(arr[i]):
                iterator[i] = 0
                carryOver = True
                if i==0:
                    b = True
                    break
        if (b):
            break
        sum = 0
        for e in range(len(iterator)):
            sum += float(arr[e][iterator[e]]['sellingStatus']['currentPrice']['value'])
        if sum <= budget:
            viable_option.append(tuple(iterator+[sum]))
    output = []
    if len(viable_option)==0:
        return output
    picked_choice = random.choice(viable_option)
    print(picked_choice)
    for it in range(len(picked_choice)-1):
        output.append((arr[it][picked_choice[it]]['title'],arr[it][picked_choice[it]]['galleryURL'],
                      arr[it][picked_choice[it]]['sellingStatus']['currentPrice']['value']))
    output.append(picked_choice[len(picked_choice)-1])
    return output


    #EAAH3Vm6c8K4BAIhH5J2psYBl00I0xqEDWPtwMUNBbWhm8bQ9InZCZAc8ZB88ZAkL8OnO6A3BVGO8MXqkXrV9oK1iNzXg4ZA002bvinUWcbwdLJeN6CZC6ZAAnLyun4gc4uzaPoXHeMRwH8qi5R9tvhwgh4t2qZAc6sXaay47q0BZBynpiaFxtJcU7ZCr32iBLbMX2kstjuKf0QoAZDZD
    
    
    
    
    
    
    
    
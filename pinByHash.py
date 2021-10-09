import sys
import os
from os import path
from common.PinataKeyClass import PinataKey

sys.stdout.reconfigure(encoding='utf-8')

# construct the Pinata key object
keylist=PinataKey('pinataApiKey.csv')

endpoint = keylist.fetchEndpoint('pinByHash')

headers={}
hashToPin=''
pinataMetadata={'name':'','keyvalues':{}}

#pinByHash.py hash free/paid

# Parsing Parameter
if(len(sys.argv) != 4):
    print("usage: python pinByHash.py hash name free/paid")
    raise SystemExit

mode = sys.argv[3]

if (mode != 'free' and mode != 'paid'):
    print("usage: either free or paid header")    
    raise SystemExit

hashToPin = sys.argv[1]
name = sys.argv[2]
mode = sys.argv[3]
print('hashToPin={}, name={}, mode={}'.format(hashToPin,name,mode))

headers=keylist.fetchKey(mode)


import requests

# Construct the json dict for the pinataMetadata.  Only name will be processed
pinataMetadata['name']=name


resp = requests.post(endpoint, headers=headers, json={'hashToPin':hashToPin,'pinataMetadata':pinataMetadata})

print(str(resp))

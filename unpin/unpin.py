import sys
import os
from os import path
from PinataKeyClass import PinataKey

sys.stdout.reconfigure(encoding='utf-8')

# construct the Pinata key object
keylist=PinataKey('pinata_api_key.csv')

endpoint = keylist.fetchEndpoint('unpin')

headers={}

# Parsing Parameter
if(len(sys.argv) != 3):
    print("usage: python unpin.py ipfshash free/paid")
    raise SystemExit

ipfshash = sys.argv[1]
mode = sys.argv[2]

if (mode != 'free' and mode != 'paid'):
    print("usage: either free or paid header")    
    raise SystemExit

headers=keylist.fetchKey(mode)

print('header got:')
print(headers)

print('Unpinning hash {} from {} endpoint'.format(ipfshash,mode))

import requests

#resp = requests.delete(endpoint, headers=headers,requestid=ipfshash)
print(endpoint+"/"+ipfshash)
resp = requests.delete(endpoint+"/"+ipfshash, headers=headers)

print("Return code: "+str(resp.status_code))

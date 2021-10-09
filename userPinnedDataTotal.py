import sys
import os
from os import path
from common.PinataKeyClass import PinataKey

sys.stdout.reconfigure(encoding='utf-8')


#Globals
gb=1024*1024*1024
mb=1024*1024
headers={}
endpoint =''

# construct the Pinata key object
keylist=PinataKey('pinataApiKey.csv')
endpoint = keylist.fetchEndpoint('userPinnedDataTotal')


# Parsing Parameter
if(len(sys.argv) != 2):
    print("usage: python userPinnedDataTotal.py free/paid")
    raise SystemExit

mode = sys.argv[1]

if (mode != 'free' and mode != 'paid'):
    print("usage: either free or paid header")    
    raise SystemExit

headers=keylist.fetchKey(mode)

print('Checking print quota for the {} endpoint...'.format(mode))

import requests

resp = requests.get(endpoint, headers=headers)

resdict = resp.json()

for data in resdict:
    if(data == 'pin_size_total' or data == 'pin_size_with_replications_total'):
        inbytes = int(resdict[data])
        if(inbytes > gb):
            print("{}:{:.2f} GB".format(data,inbytes/gb))
        else:
            print("{}:{:.2f} MB".format(data,inbytes/mb))
    else:
        print(data,resdict[data])
    
costpermonth=int(resdict['pin_size_with_replications_total'])*0.15/(1024*1024*1024)
print('Monthly cost: USD {:.2f}'.format(costpermonth))
print('Yearly cost: USD {:.2f}'.format(costpermonth*12))

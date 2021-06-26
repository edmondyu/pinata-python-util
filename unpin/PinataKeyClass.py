# pinata utility class
#
# Requests format
# authentication keys in headers
# unpin:    DELETE endpoint+"/"+ipfshash
# pinFileToIPFS: POST endpoint files=file_to_be_pinned
# userPinnedDataTotal: GET endpoint


import os
from os import path
import csv

class PinataKey:
    csv_filename=''
    endpoint = "https://api.pinata.cloud/"

    def __init__(self,csv_filename):
    # Constructor read a filename parameter
    # fetch all rows from csv
    # contruct a list of dicts, each dict has 3 key-value pairs: lable, api_key, secret_api_key
        self.allKeyList=[]
        self.returnKey={}
        if path.isfile(csv_filename):
            # Read the CSV and update our listed dictionary
            with open(csv_filename, mode='r', encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.allKeyList.append(row)
 
            print('Inititialized by {}'.format(csv_filename))
            print('Total number of elements:{}'.format(len(self.allKeyList)))

    def fetchKey(self,label):
        # input: a label of the api_key
        # return: a dict of api_key and secret_api_key
        keyItem={}

        for keyItem in self.allKeyList:
            if(keyItem['label'] == label):
                self.returnKey['pinata_api_key']=keyItem['pinata_api_key']
                self.returnKey['pinata_secret_api_key']=keyItem['pinata_secret_api_key']
                break
        return(self.returnKey)

    def fetchEndpoint(self,operation):
        # return the proper endpoint format
        if(operation == 'unpin' or operation == 'pinByHash' or operation == 'pinFileToIPFS'):
            self.endpoint += 'pinning/'+operation
        elif(operation == 'userPinnedDataTotal'):
            self.endpoint += 'data/'+operation
        return(self.endpoint)

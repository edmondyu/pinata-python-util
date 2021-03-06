# pinFileInCSV.py
# Pin files specified in CSV to IPFS using Pinata.cloud, write the returned hash to a new column
# secret keys are stored in the working directory as plain text file
# Must have the field "filename" in the inputCSV.csv file
#
# usage : python pinFileInCSV.py inputCSV.csv keyTag


import sys
import os
import csv
import requests
import time #for sleep
from os import path
from common.PinataKeyClass import PinataKey

sys.stdout.reconfigure(encoding='utf-8')

#Global variable
totalRecords =0 #total number of records to be uploaded
listedDict1 =[]
uploadPath = 'upload'

# Copy your Pinata API Key and Secret here
headers={}
endpoint =''


# construct the Pinata key object
keylist=PinataKey('pinataApiKey.csv')
endpoint = keylist.fetchEndpoint('pinFileToIPFS')

def pinFile(thisFilePath):
    if path.isfile(thisFilePath):
        print('Uploading {} of {}'.format(i,totalRecords), thisFilePath, '...... ', end = '', flush= True)
        files = {"file":open(thisFilePath, 'rb')}

        # Retry for 3 times if failed
        retry=0
        print("attempt {}...".format(retry+1),end='',flush=True)
        resp = requests.post(endpoint, headers=headers, files=files)
        while(resp.status_code != 200 and retry < 3):
            retry +=1
            print("attempt {}...".format(retry+1),end='',flush=True)
            time.sleep(15)
            resp = requests.post(endpoint, headers=headers, files=files)
            
        if(resp.status_code == 200):
            print("Upload success")
            # return ipfsHash
            return resp.json()["IpfsHash"]
        else:
            print("Upload failed.  Error:"+str(resp.status_code))
            return False
    else:
        print("File ", filename," is missing.")
        return False

# Parsing Parameter
if(len(sys.argv) != 3):
    print("usage: python pinFileInCSV.py csvFile keyTag")
    raise SystemExit

inputFile = sys.argv[1]
mode = sys.argv[2]
outputFile = 'out_'+inputFile

if (mode != 'free' and mode != 'paid'):
    print("usage: either free or paid header")    
    raise SystemExit

headers=keylist.fetchKey(mode)

with open(inputFile, mode='r', encoding="utf-8") as inputFileh:
    reader1 = csv.DictReader(inputFileh)
    # put new file entries in a list
    for row1 in reader1: 
        listedDict1.append(row1)
        #[{'publisedDate':2020-01-01,'publisher':'MingPao',....},{'publisedDate':2020-01-02,'publisher':'MingPao',....}]
totalRecords=len(listedDict1)
# CSV fields.  
# original fields should be read from the input CSV file
# hash field should be fixed as "ipfsHash"

newItem=listedDict1[0]
fieldnames = newItem.keys()
relatedIpfsHashes=[]

if('ipfsHash' not in fieldnames):
    newItem['ipfsHash']=''
    fieldnames = newItem.keys()
if('relatedIpfsHashes' not in fieldnames):
    newItem['relatedIpfsHashes']=''
    fieldnames = newItem.keys()


filewriter= open(outputFile,'w', encoding="utf-8")

dict_writer = csv.DictWriter(filewriter,fieldnames)
dict_writer.writeheader()

for i,item1 in enumerate(listedDict1):

    if('ipfsHash' not in item1.keys()):
        ipfsHash=''
        item1['ipfsHash']=ipfsHash
    else:
        ipfsHash = item1['ipfsHash']

    if(ipfsHash):
        # already pinned.  skip
        dict_writer.writerow(item1)
        print(f'Already pinned: {ipfsHash}')
        continue
    else:
        # filename -> ipfsHash
        # relatedFiles -> otherIpfsHash
        # try to pin the file
        filename = item1['filename']
        filepath = os.path.join(uploadPath,filename)
        print(f"filepath={filepath}")

        # call a function to get the hash
        ipfsHash=pinFile(filepath)

        if(ipfsHash):
                item1['ipfsHash'] = ipfsHash

        #### deal with relatedFiles
        relatedFilesStr=item1['relatedFiles'][1:-1].replace('\'','')
        relatedFilesStr=relatedFilesStr.replace(' ','')
        if(relatedFilesStr):
            relatedFiles=relatedFilesStr.split(',')
        else:
            relatedFiles=[]

        if(relatedFiles):
            print('Pinning related files')
            for filename in relatedFiles:
                filepath = os.path.join(uploadPath,filename)
                print(f"filepath={filepath}")
                # call a function to get the hash
                relatedIpfsHash=pinFile(filepath)
                if(relatedIpfsHash):
                    relatedIpfsHashes.append(relatedIpfsHash)
            item1['relatedIpfsHashes'] = relatedIpfsHashes
        
        dict_writer.writerow(item1)



filewriter.close()
import sys
import os
from os import path
import requests
import csv
import time
from common.PinataKeyClass import PinataKey

filePath = 'toUpload'
txtFileList=[]
item={}

print(f"Current working directory: {os.getcwd()}")

headers={}
endpoint =''
# construct the Pinata key object
keylist=PinataKey('pinataApiKey.csv')
endpoint = keylist.fetchEndpoint('pinFileToIPFS') # choose the pinata endpoint and the corresponding header format

mode='likerland' # the mode label is defined in the file pinata_api_key.csv.  
headers=keylist.fetchKey(mode)

fileCounter=0
for file in os.listdir(filePath):
    # Check whether file is in text format or not.  If yes, put into the txtFileList
    
    if file.endswith(".txt"):
        fileCounter+=1
        txtFileList.append(file)

txtFileList = sorted(txtFileList)

print(f'Number of text file to be uploaded:{fileCounter}')

# Upload to Pinata, output to csv for record if successfully

fieldnames=['filename','ipfsHash']
fileWriter= open('uploadedTxt.csv','w', encoding="utf-8")

dictWriter = csv.DictWriter(fileWriter,fieldnames)
dictWriter.writeheader()

for file in txtFileList:
    item['filename']=file
    fullPath=f"{filePath}/{file}"
    
    files = {"file":open(fullPath, 'rb')}
       
    resp = requests.post(endpoint, headers=headers, files=files)
    retry=0
    while(resp.status_code != 200 and retry < 3):
        retry +=1
        print("attempt {}...".format(retry+1),end='',flush=True)
        time.sleep(15)
        resp = requests.post(endpoint, headers=headers, files=fullPath)    

    if(resp.status_code == 200):
        print(f"{fullPath} upload successful")
        item['ipfsHash'] = resp.json()["IpfsHash"]

    dictWriter.writerow(item)


fileWriter.close()

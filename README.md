# Pinata toolkit in Python
This toolkit is for Pinata users who use Python. 

## Installation
- git clone https://github.com/edmondyu/pinata-python-util.git
- edit the file [pinata_api_key.csv](https://github.com/edmondyu/pinata-python-util/blob/main/pinata_api_key.csv "pinata_api_key.csv") to include your Pinata API key.  You can assign any label to your key, and supply the label as a parameter to instruct the script to use that key.

## Using [pinFileInCSV.py](https://github.com/edmondyu/pinata-python-util/blob/main/pinFileInCSV.py "pinFileInCSV.py")

- this script is for batch uploading and pinning files to Pinata.
- prepare data in a CSV file, one row one file, filename specified in the "filename" field, with any metadata. 
- copy the CSV file to the program directory
- copy all the files to be uploaded to the "/upload" directory
- run the command

```python3 pinFileInCsv.py csvFile.csv keyLabel```

- the script will pin the files specified in the CSV row by row.  If pinning successful, the returned hash will be written in the output file "out_[inputFilename]". The field will be left blank if pinning failed.
- the input file does not need to have the "ipfsHash" field prepared in advance, the script will add this field automatically.  
- If the input file has the ipfsHash field in advance, however, the script will skip those records which already have hash value filled.

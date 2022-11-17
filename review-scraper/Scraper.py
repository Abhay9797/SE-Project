from dateutil import parser as dateparser
from encodings.utf_8 import encode
from selectorlib import Extractor
from time import sleep
import pandas as pd
import requests 
import json 
import csv

extractor = Extractor.from_yaml_file('selectors.yml')

def scrape(url):    
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page with the requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)

    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None

    # Pass the HTML of the page and create 
    return extractor.extract(r.text)

# product_data = []
with open("urls.txt",'r', encoding='utf-8') as urllist, open('data.csv','w',encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["title","content","product"],quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for url in urllist.readlines():
        data = scrape(url) 
        if data:
            for r in data['reviews']:
                r["product"] = data["product_title"]
                writer.writerow(r)
            sleep(5)

#removes empty spaces in the previous CSV file
dt = pd.read_csv('data.csv')
#checking the number of empty rows in th csv file
print (dt.isnull().sum())
#Droping the empty rows
modifiedDF = dt.dropna()
#Saving it to the csv file 
modifiedDF.to_csv('nospace.csv',index=False,quoting=csv.QUOTE_ALL) 



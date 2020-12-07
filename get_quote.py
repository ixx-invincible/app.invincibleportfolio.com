import os
from datetime import datetime
import time
import requests
import json 
import pandas as pd


last_rebalancing = {
    'rebalance_date': '2020-09-30',
    'index': 415.1941708,
    'spy': 334.8900146,
    'gld': 162.7501068,
    'tlt': 177.1199951,
}


api_url = 'https://cloud.iexapis.com/stable'
endpoint = '/stock/market/quote'
token = 'pk_1dafd28f39414e6fa735c9350a508a47'


while 1:
    now = datetime.now()
    if now.hour <= 6 or now.hour >= 9:
        try:
            r = requests.get(api_url + endpoint + '?token=' + token + '&symbols=gld,spy,tlt&filter=symbol,open,latestPrice,latestUpdate,previousClose')

            quotes = json.loads(r.text)

            gld = {}
            spy = {}
            tlt = {}
            index = {'symbol': 'GST'}
            latestUpdate = 0

            for quote in quotes:
                if quote['latestUpdate'] > latestUpdate:
                    latestUpdate = quote['latestUpdate']

                if quote['symbol'] == 'GLD':
                    gld = quote

                if quote['symbol'] == 'SPY':
                    spy = quote

                if quote['symbol'] == 'TLT':
                    tlt = quote


            index['previousClose'] = last_rebalancing['index'] * ((gld['previousClose']/last_rebalancing['gld'] + spy['previousClose']/last_rebalancing['spy'] + tlt['previousClose']/last_rebalancing['tlt']) / 3)
            index['open'] = last_rebalancing['index'] * ((gld['open']/last_rebalancing['gld'] + spy['open']/last_rebalancing['spy'] + tlt['open']/last_rebalancing['tlt']) / 3)
            index['latestPrice'] = last_rebalancing['index'] * ((gld['latestPrice']/last_rebalancing['gld'] + spy['latestPrice']/last_rebalancing['spy'] + tlt['latestPrice']/last_rebalancing['tlt']) / 3)
            index['latestUpdate'] = latestUpdate

            quotes.append(index)



            today = datetime.today().strftime('%Y-%m-%d')

            # Writing to today.txt 
            with open(os.getcwd() + "/quote/" + today + ".log", "a") as outfile: 
                outfile.write("\n")
                outfile.write(json.dumps(quotes)) 


            # Serializing json  
            json_object = json.dumps(quotes, indent = 4) 

            # Writing to quote.json 
            with open(os.getcwd() + "/quote/latest.json", "w") as outfile: 
                outfile.write(json_object) 
        except:
            pass

    time.sleep(2)
import os
from datetime import datetime
import time
import requests
import json 
import pandas as pd


api_url = 'https://cloud.iexapis.com/stable'
endpoint = '/stock/market/quote'
token = 'pk_1dafd28f39414e6fa735c9350a508a47'


while 1:
    now = datetime.now()
    if now.hour <= 6 or now.hour >= 21:
        try:
            r = requests.get(api_url + endpoint + '?token=' + token + '&symbols=gld,spy,tlt&filter=symbol,open,latestPrice,latestUpdate')

            quotes = json.loads(r.text)

            gld = {}
            spy = {}
            tlt = {}
            gst = {'symbol': 'GST'}
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


            with open('quote/invincible_portfolio_latest.json') as f:
                data = json.load(f)
                gld['previousClose'] = data[0]['gld']
                spy['previousClose'] = data[0]['spy']
                tlt['previousClose'] = data[0]['tlt']

                gst['previousClose'] = data[0]['portfolio']
                gst['previousDate'] = datetime.fromtimestamp(data[0]['Date']/1000).strftime("%Y-%m-%d")


                if gld['open'] != None and spy['open'] != None and tlt['open'] != None:
                    gst['open'] = data[0]['portfolio_rb'] * ((gld['open']/data[0]['gld_rb'] + spy['open']/data[0]['spy_rb'] + tlt['open']/data[0]['tlt_rb']) / 3)
                
                if gld['latestPrice'] != None and spy['latestPrice'] != None and tlt['latestPrice'] != None:
                    gst['latestPrice'] = data[0]['portfolio_rb'] * ((gld['latestPrice']/data[0]['gld_rb'] + spy['latestPrice']/data[0]['spy_rb'] + tlt['latestPrice']/data[0]['tlt_rb']) / 3)
            
                gst['latestUpdate'] = latestUpdate

            quotes.append(gst)

            # Writing to quote.json 
            with open("quote/latest.json", "w") as outfile: 
                outfile.write(json.dumps(quotes, indent = 4)) 


            # Writing to today.log 
            today = datetime.today().strftime('%Y-%m-%d')
            quotes_latest = {
                'latestUpdate': latestUpdate,
                'spy': spy['latestPrice'],
                'gld': gld['latestPrice'],
                'tlt': tlt['latestPrice'],
                'gst': gst['latestPrice']
            }

            with open("quote/" + today + ".log", "a") as outfile: 
                outfile.write("\n")
                outfile.write(json.dumps(quotes_latest)) 
        except:
            pass

    time.sleep(2)
import os
from datetime import datetime
import time
import json 

from yahoo_fin import stock_info as si

 
while 1:
    now = datetime.now()
    if now.hour <= 6 or now.hour >= 12:
        try:
            # r = requests.get(api_url + endpoint + '?token=' + token + '&symbols=gld,spy,tlt&filter=symbol,open,latestPrice,latestUpdate,isUSMarketOpen')
            # quotes = json.loads(r.text)

            gst = {'symbol': 'GST'}
            # latestUpdate = 0

            quote = si.get_quote_table("SPY")
            quote = si.get_quote_table("GLD")
            gld = {
                "symbol": "GLD",
                "open": quote['Open'],
                "previousClose": quote['Previous Close'],
                "latestPrice": quote['Quote Price'],
                "latestUpdate": time.time(),
            }

            spy = {
                "symbol": "SPY",
                "open": quote['Open'],
                "previousClose": quote['Previous Close'],
                "latestPrice": quote['Quote Price'],
                "latestUpdate": time.time(),
            }

            quote = si.get_quote_table("TLT")
            tlt = {
                "symbol": "TLT",
                "open": quote['Open'],
                "previousClose": quote['Previous Close'],
                "latestPrice": quote['Quote Price'],
                "latestUpdate": time.time(),
            }

            
            with open('quote/invincible_portfolio_latest.json') as f:
                data = json.load(f)

                if spy['isUSMarketOpen']:
                    data = data[1]
                else:
                    data = data[0]

                gld['previousClose'] = data['gld']
                spy['previousClose'] = data['spy']
                tlt['previousClose'] = data['tlt']

                gst['previousClose'] = data['portfolio']
                gst['previousDate'] = datetime.fromtimestamp(data['Date']/1000).strftime("%Y-%m-%d")


                if gld['open'] != None and spy['open'] != None and tlt['open'] != None:
                    gst['open'] = data['portfolio_rb'] * ((gld['open']/data['gld_rb'] + spy['open']/data['spy_rb'] + tlt['open']/data['tlt_rb']) / 3)
                
                if gld['latestPrice'] != None and spy['latestPrice'] != None and tlt['latestPrice'] != None:
                    gst['latestPrice'] = data['portfolio_rb'] * ((gld['latestPrice']/data['gld_rb'] + spy['latestPrice']/data['spy_rb'] + tlt['latestPrice']/data['tlt_rb']) / 3)
            
                gst['latestUpdate'] = latestUpdate
            
            quotes.append(gst)


            # Writing to quote.json 
            # with open("quote/latest.json", "w") as outfile: 
            #     outfile.write(json.dumps(quotes, indent = 4)) 


            # Writing to today.log 
            # today = datetime.today().strftime('%Y-%m-%d')
            # quotes_latest = {
            #     'latestUpdate': latestUpdate,
            #     'spy': spy['latestPrice'],
            #     'gld': gld['latestPrice'],
            #     'tlt': tlt['latestPrice'],
            #     'gst': gst['latestPrice']
            # }

            # with open("quote/" + today + ".log", "a") as outfile: 
            #     outfile.write("\n")
            #     outfile.write(json.dumps(quotes_latest)) 
        except:
            pass

    time.sleep(2)
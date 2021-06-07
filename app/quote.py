import requests
import json 
from datetime import datetime


api_url = 'https://cloud.iexapis.com/stable'
endpoint = '/stock/market/quote'
token = 'pk_1dafd28f39414e6fa735c9350a508a47'

# https://cloud.iexapis.com/stable/stock/market/quote?token=pk_1dafd28f39414e6fa735c9350a508a47&symbols=gld,spy,tlt

"""
[
    {
        "symbol":"GLD",
        "companyName":"SSgA Active Trust - SPDR Gold Shares ETF",
        "primaryExchange":"NYSE ARCA",
        "calculationPrice":"close",
        "open":176.63,
        "openTime":1622813400310,
        "openSource":"official",
        "close":177.16,
        "closeTime":1622836800149,
        "closeSource":"official",
        "high":177.57,
        "highTime":1622836799997,
        "highSource":"15 minute delayed price",
        "low":176.61,
        "lowTime":1622813403686,
        "lowSource":"15 minute delayed price",
        "latestPrice":177.16,
        "latestSource":"Close",
        "latestTime":"June 4, 2021",
        "latestUpdate":1622836800149,
        "latestVolume":8375264,
        "iexRealtimePrice":null,
        "iexRealtimeSize":null,
        "iexLastUpdated":null,
        "delayedPrice":177.17,
        "delayedPriceTime":1622836799997,
        "oddLotDelayedPrice":177.17,
        "oddLotDelayedPriceTime":1622836799921,
        "extendedPrice":177.16,
        "extendedChange":0,
        "extendedChangePercent":0,
        "extendedPriceTime":1622851200017,
        "previousClose":175.27,
        "previousVolume":10153899,
        "change":1.89,
        "changePercent":0.01078,
        "volume":8375264,
        "iexMarketPercent":null,
        "iexVolume":null,
        "avgTotalVolume":9463921,
        "iexBidPrice":null,
        "iexBidSize":null,
        "iexAskPrice":null,
        "iexAskSize":null,
        "iexOpen":177.17,
        "iexOpenTime":1622836794034,
        "iexClose":177.17,
        "iexCloseTime":1622836794034,
        "marketCap":63352416000,
        "peRatio":null,
        "week52High":194.45,
        "week52Low":157.13,
        "ytdChange":0.004052034088360511,
        "lastTradeTime":1622836799997,
        "isUSMarketOpen":false
    }
]
"""

def get_iex_quotes():
    try:
        r = requests.get(api_url + endpoint + '?token=' + token + '&symbols=gld,spy,tlt&filter=symbol,previousClose,open,latestPrice,latestUpdate,isUSMarketOpen,week52High,week52Low,ytdChange')

        quotes = json.loads(r.text)

        return quotes
    except:
        return []

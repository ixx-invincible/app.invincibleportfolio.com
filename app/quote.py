import requests
import json 
from datetime import datetime
from yahoo_fin import stock_info as si


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
    """
    [
        {"symbol":"GLD","previousClose":167.67,"open":167.58,"latestPrice":170.19,"latestUpdate":1630094400166,"isUSMarketOpen":false,"week52High":186.99,"week52Low":157.13,"ytdChange":-0.03077623458174482},
        {"symbol":"SPY","previousClose":446.26,"open":447.1,"latestPrice":450.25,"latestUpdate":1630094400237,"isUSMarketOpen":false,"week52High":450.65,"week52Low":316.37,"ytdChange":0.2210992291286507},
        {"symbol":"TLT","previousClose":148.45,"open":148.59,"latestPrice":149.46,"latestUpdate":1630094400655,"isUSMarketOpen":false,"week52High":165.27,"week52Low":132.48,"ytdChange":-0.03830056600121004}
    ]
    """

    try:
        r = requests.get(api_url + endpoint + '?token=' + token + '&symbols=gld,spy,tlt&filter=symbol,previousClose,open,latestPrice,latestUpdate,isUSMarketOpen,week52High,week52Low,ytdChange')

        quotes = json.loads(r.text)

        return quotes
    except:
        return []




def get_yahoo_quotes():
    """
    [
        {'52 Week Range': '157.13 - 186.99', 'Ask': '0.00 x 4000', 'Avg. Volume': 8064500.0, 'Beta (5Y Monthly)': 0.09, 'Bid': '0.00 x 1300', "Day's Range": '166.90 - 170.19', 'Expense Ratio (net)': '0.40%', 'Inception Date': '2004-11-18', 'NAV': 166.84, 'Net Assets': '59.26B', 'Open': 167.58, 'PE Ratio (TTM)': 28.63, 'Previous Close': 167.67, 'Quote Price': 170.19000244140625, 'Volume': 10036431.0, 'YTD Daily Total Return': '-6.43%', 'Yield': '0.00%'},
        {'52 Week Range': '319.80 - 450.65', 'Ask': '0.00 x 1200', 'Avg. Volume': 61116292.0, 'Beta (5Y Monthly)': 1.0, 'Bid': '0.00 x 3100', "Day's Range": '447.07 - 450.65', 'Expense Ratio (net)': '0.09%', 'Inception Date': '1993-01-22', 'NAV': 439.23, 'Net Assets': '374.03B', 'Open': 447.12, 'PE Ratio (TTM)': 3.12, 'Previous Close': 446.26, 'Quote Price': 450.25, 'Volume': 77235113.0, 'YTD Daily Total Return': '19.94%', 'Yield': '1.30%'},
        {'52 Week Range': '133.19 - 167.24', 'Ask': '0.00 x 1100', 'Avg. Volume': 15720817.0, 'Beta (5Y Monthly)': 3.36, 'Bid': '0.00 x 2200', "Day's Range": '148.34 - 149.48', 'Expense Ratio (net)': '0.15%', 'Inception Date': '2002-07-22', 'NAV': 149.23, 'Net Assets': '15.15B', 'Open': 148.57, 'PE Ratio (TTM)': nan, 'Previous Close': 148.45, 'Quote Price': 149.4600067138672, 'Volume': 15384740.0, 'YTD Daily Total Return': '-5.12%', 'Yield': '1.50%'}
    ]
    """

    try:
        quotes = []
        for quote in ['gld', 'spy', 'tlt', 'tqqq', 'upro', 'tmf']:
            quotes.append(
                {
                    "symbol": quote,
                    "previousClose": si.get_quote_table(quote).get('Previous Close'),
                    "open": si.get_quote_table(quote).get('Open'),
                    "latestPrice": si.get_quote_table(quote).get('Quote Price'),
                    "week52Low": float(si.get_quote_table(quote).get('52 Week Range').split(" - ")[0]),
                    "week52High": float(si.get_quote_table(quote).get('52 Week Range').split(" - ")[1]),
                    "ytdChange": si.get_quote_table(quote).get('YTD Daily Total Return'),
                }
            )

        with open('static/quote.json', 'w') as fp:
            json.dump(quotes, fp, sort_keys=True, indent=4)
    except:
        return


def get_live_quote():
    try:
        quotes = []
        for quote in ['gld', 'spy', 'tlt', 'tqqq', 'upro', 'tmf']:
            quotes.append(
                    {
                        "symbol": quote,
                        "livePrice": si.get_live_price(quote)
                    }
                )

        
        return quotes
    except:
        return []



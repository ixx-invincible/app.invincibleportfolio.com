# import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si
import json

# get live price of Apple
# print(si.get_live_price("spy"))

 
# or Amazon
# print(si.get_quote_table('gld'))
# print(si.get_quote_table('spy'))
# print(si.get_quote_table('tlt'))
 
quotes = []
# quotes.append(si.get_quote_table('gld'))
# quotes.append(si.get_quote_table('spy'))
# quotes.append(si.get_quote_table('tlt'))

quotes = []
for quote in ['gld', 'spy', 'tlt']:
    quotes.append(
        {
            "symbol": "GLD",
            "previousClose": si.get_quote_table(quote).get('Previous Close'),
            "open": si.get_quote_table(quote).get('Open'),
            "latestPrice": si.get_quote_table(quote).get('Quote Price'),
            "week52Low": float(si.get_quote_table(quote).get('52 Week Range').split(" - ")[0]),
            "week52High": float(si.get_quote_table(quote).get('52 Week Range').split(" - ")[1]),
            "ytdChange": si.get_quote_table(quote).get('YTD Daily Total Return'),
        }
    )

    """
    [
        {"symbol":"GLD","previousClose":167.67,"open":167.58,"latestPrice":170.19,"latestUpdate":1630094400166,"isUSMarketOpen":false,"week52High":186.99,"week52Low":157.13,"ytdChange":-0.03077623458174482},
        {"symbol":"SPY","previousClose":446.26,"open":447.1,"latestPrice":450.25,"latestUpdate":1630094400237,"isUSMarketOpen":false,"week52High":450.65,"week52Low":316.37,"ytdChange":0.2210992291286507},
        {"symbol":"TLT","previousClose":148.45,"open":148.59,"latestPrice":149.46,"latestUpdate":1630094400655,"isUSMarketOpen":false,"week52High":165.27,"week52Low":132.48,"ytdChange":-0.03830056600121004}
    ]
    """

    """
    [
        {'52 Week Range': '157.13 - 186.99', 'Ask': '0.00 x 4000', 'Avg. Volume': 8064500.0, 'Beta (5Y Monthly)': 0.09, 'Bid': '0.00 x 1300', "Day's Range": '166.90 - 170.19', 'Expense Ratio (net)': '0.40%', 'Inception Date': '2004-11-18', 'NAV': 166.84, 'Net Assets': '59.26B', 'Open': 167.58, 'PE Ratio (TTM)': 28.63, 'Previous Close': 167.67, 'Quote Price': 170.19000244140625, 'Volume': 10036431.0, 'YTD Daily Total Return': '-6.43%', 'Yield': '0.00%'},
        {'52 Week Range': '319.80 - 450.65', 'Ask': '0.00 x 1200', 'Avg. Volume': 61116292.0, 'Beta (5Y Monthly)': 1.0, 'Bid': '0.00 x 3100', "Day's Range": '447.07 - 450.65', 'Expense Ratio (net)': '0.09%', 'Inception Date': '1993-01-22', 'NAV': 439.23, 'Net Assets': '374.03B', 'Open': 447.12, 'PE Ratio (TTM)': 3.12, 'Previous Close': 446.26, 'Quote Price': 450.25, 'Volume': 77235113.0, 'YTD Daily Total Return': '19.94%', 'Yield': '1.30%'},
        {'52 Week Range': '133.19 - 167.24', 'Ask': '0.00 x 1100', 'Avg. Volume': 15720817.0, 'Beta (5Y Monthly)': 3.36, 'Bid': '0.00 x 2200', "Day's Range": '148.34 - 149.48', 'Expense Ratio (net)': '0.15%', 'Inception Date': '2002-07-22', 'NAV': 149.23, 'Net Assets': '15.15B', 'Open': 148.57, 'PE Ratio (TTM)': nan, 'Previous Close': 148.45, 'Quote Price': 149.4600067138672, 'Volume': 15384740.0, 'YTD Daily Total Return': '-5.12%', 'Yield': '1.50%'}
    ]
    """

print(quotes)
with open('static/quote.json', 'w') as fp:
    json.dump(quotes, fp, sort_keys=True, indent=4)


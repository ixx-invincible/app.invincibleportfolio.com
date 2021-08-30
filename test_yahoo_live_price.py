from yahoo_fin import stock_info as si
import json


for quote in ['gld', 'spy', 'tlt']:
    print(si.get_live_price(quote))

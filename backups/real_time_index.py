import json

from datetime import datetime
import time
from yahoo_fin import stock_info as si


weighting = {
    'rebalance_date': '2020-09-30',
    'spy_weight': 0.413264236,
    'gld_weight': 0.781380249,
    'tlt_weight': 0.849505351,
}

spy = si.get_quote_table("spy")
gld = si.get_quote_table("gld")
tlt = si.get_quote_table("tlt")


pp_previous_close = spy['Previous Close'] * weighting['spy_weight'] + gld['Previous Close'] * weighting['gld_weight'] + tlt['Previous Close'] * weighting['tlt_weight']

pp_live_price = spy['Quote Price'] * weighting['spy_weight'] + gld['Quote Price'] * weighting['gld_weight'] + tlt['Quote Price'] * weighting['tlt_weight']



dictionary ={ 
    "now" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
    "pp_previous_close" : pp_previous_close, 
    "spy_previous_close" : spy['Previous Close'],
    "gld_previous_close" : gld['Previous Close'],
    "tlt_previous_close" : tlt['Previous Close'],
    "pp_live_price" : pp_live_price,
    "spy_quote_price" : spy['Quote Price'],
    "gld_quote_price" : gld['Quote Price'],
    "tlt_quote_price" : tlt['Quote Price']
} 

# Serializing json  
json_object = json.dumps(dictionary, indent = 4) 

# Writing to sample.json 
with open("./real_time_index.json", "w") as outfile: 
    outfile.write(json_object) 

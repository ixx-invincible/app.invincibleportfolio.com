import json

from datetime import datetime
import time
from yahoo_fin import stock_info as si


weighting = {
    'rebalance_date': '2020-09-30',
    'spy_pp_weight': 0.413264236,
    'gld_pp_weight': 0.781380249,
    'tlt_pp_weight': 0.849505351,
    'spy_ip_weight': 0.500091562,
    'gld_ip_weight': 0.709161903,
    'tlt_ip_weight': 0.770990605
}

spy = si.get_quote_table("spy")
gld = si.get_quote_table("gld")
tlt = si.get_quote_table("tlt")


pp_previous_close = spy['Previous Close'] * weighting['spy_pp_weight'] + gld['Previous Close'] * weighting['gld_pp_weight'] + tlt['Previous Close'] * weighting['tlt_pp_weight']
ip_previous_close = spy['Previous Close'] * weighting['spy_ip_weight'] + gld['Previous Close'] * weighting['gld_ip_weight'] + tlt['Previous Close'] * weighting['tlt_ip_weight']

pp_live_price = spy['Quote Price'] * weighting['spy_pp_weight'] + gld['Quote Price'] * weighting['gld_pp_weight'] + tlt['Quote Price'] * weighting['tlt_pp_weight']
ip_live_price = spy['Quote Price'] * weighting['spy_ip_weight'] + gld['Quote Price'] * weighting['gld_ip_weight'] + tlt['Quote Price'] * weighting['tlt_ip_weight']



dictionary ={ 
    "now" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
    "pp_previous_close" : pp_previous_close, 
    "ip_previous_close" : ip_previous_close, 
    "spy_previous_close" : spy['Previous Close'],
    "gld_previous_close" : gld['Previous Close'],
    "tlt_previous_close" : tlt['Previous Close'],
    "pp_live_price" : pp_live_price,
    "ip_live_price" : ip_live_price,
    "spy_quote_price" : spy['Quote Price'],
    "gld_quote_price" : gld['Quote Price'],
    "tlt_quote_price" : tlt['Quote Price']
} 

# Serializing json  
json_object = json.dumps(dictionary, indent = 4) 

# Writing to sample.json 
with open("real_time_index.json", "w") as outfile: 
    outfile.write(json_object) 

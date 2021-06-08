
from datetime import datetime
import time
from yahoo_fin import stock_info as si


spy_quote_table = si.get_quote_table("spy")
gld_quote_table = si.get_quote_table("gld")
tlt_quote_table = si.get_quote_table("tlt")

previous_close = spy_quote_table['Previous Close'] * 0.413264236 + gld_quote_table['Previous Close'] * 0.781380249 + tlt_quote_table['Previous Close'] * 0.849505351
print('Previous Close: {}'.format(round(previous_close, 2)))


try:
    while 1:
        spy = si.get_live_price("spy")
        gld = si.get_live_price("gld")
        tlt = si.get_live_price("tlt")
 
        # 30/09/2020       
        # spy_shares	gld_shares	tlt_shares
        # 0.413264236	0.781380249	0.849505351

        live_price = spy*0.413264236 + gld*0.781380249 + tlt*0.849505351
        
        print('{} {} {}{}% [SPY:{} GLD:{} TLT:{}]'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                                            round(live_price, 2), 
                                                            ('+' if live_price > previous_close else ''),
                                                            round((live_price/previous_close-1)*100, 2),
                                                            round(spy, 2),
                                                            round(gld, 2),
                                                            round(tlt, 2)))
        
        time.sleep(10)

except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    pass

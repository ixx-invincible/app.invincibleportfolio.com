#import talib as ta
import math
import numpy as np
import pandas as pd
import pandas_datareader as pdr

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import seaborn as sns

import yfinance as yfin
yfin.pdr_override()

# from mplfinance import candlestick_ohlc
# import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc


faang = ['QQQ', 'AAPL', 'AMZN', 'MSFT', 'FB', 'GOOGL', 'GOOG']

#https://www.zacks.com/funds/etf/QQQ/holding
qqq = ['QQQ', 'AAPL', 'AMZN', 'MSFT', 'META', 'GOOGL', 'GOOG', 'TSLA', 'NVDA', 'ADBE', 'NFLX', 
       'PYPL', 'INTC', 'CMCSA', 'PEP', 'CSCO', 'COST', 'AMGN', 'TMUS', 'AVGO', 'TXN', 
       'QCOM', 'CHTR', 'AMD', 'SBUX', 'INTU','MDLZ', 'GILD', 'ISRG', 'BKNG', 'JD', 
       'VRTX', 'ATVI', 'REGN', 'MELI', 'ADP', 'AMAT', 'CSX', 'ADSK', 'ILMN', 
       'LRCX', 'MU', 'ZM', 'LULU', 'BIIB', 'ADI', 'MNST', 'KHC', 'EA', 'EBAY']
#https://www.zacks.com/funds/etf/SPY/holding
spy = ['SPY', 'AAPL', 'MSFT', 'AMZN', 'META', 'GOOGL', 'GOOG', 'JNJ', 'BRK-B', 'V', 'PG', 
       'JPM', 'UNH', 'HD', 'MA', 'NVDA', 'VZ', 'PYPL', 'PFE', 'NFLX', 'ADBE', 
       'T', 'DIS', 'INTC', 'MRK', 'CMCSA', 'CSCO', 'BAC', 'PEP', 'KO', 'WMT', 
       'ABT', 'XOM', 'CRM', 'ABBV', 'TMO', 'CVX', 'MCD', 'AMGN', 'COST', 'ACN', 
       'NEE', 'BMY', 'MDT', 'LLY', 'DHR', 'LIN', 'AVGO', 'PM', 'QCOM', 'NKE']

hs50 = ['2800.HK', '0700.HK', '9988.HK', '0941.HK', '0005.HK', '0939.HK', '3690.HK', '1299.HK', '0883.HK', '9999.HK', 
        '9618.HK', '9888.HK', '0388.HK', '2318.HK', '1810.HK', '1398.HK', '0016.HK', '2020.HK', '1211.HK', '1876.HK', 
        '2388.HK', '1109.HK', '0027.HK', '0267.HK', '3988.HK', '9633.HK', '1928.HK', '0066.HK', '9961.HK', '2269.HK', 
        '0011.HK', '0762.HK', '0688.HK', '0001.HK', '0291.HK', '1113.HK', '0002.HK', '0669.HK', '0981.HK', '3968.HK', 
        '6618.HK', '1929.HK', '6862.HK', '0857.HK', '2313.HK', '0003.HK', '0386.HK', '0012.HK', '0960.HK', '1997.HK', 
        '0992.HK', '2331.HK', '2319.HK', '0826.HK', '1038.HK', '0175.HK', '2688.HK', '2628.HK', '0006.HK', '0316.HK']




pp = ['SPY', 'GLD', 'TLT']
#etf = ['SPY', 'QQQ', 'IVV', 'IEFA', 'MTUM', 'GLD', 'IAU', 'SLV', 'TLT', 'AGG', 'IWM', 'IVW', 'XLV']

etf = ['SPY', 'QQQ', 'XLV', 'VNQ', 'GDX', 'XLF', 'XLY', 'XLC', 'XLE', 'XLI', 'XLU', 'XLP', 'VOX', 'GLD', 'TLT', 'AGG']

metal = ['GLD', 'PALL', 'SLV', 'CPER', 'PPTL']

us_equities = ['SPY', 'QQQ', 'MTUM']

indexes = [qqq, spy, hs50, metal, pp, us_equities]
#
indexes = [qqq]


for tickers in indexes:
    
    m = pd.DataFrame()
    
    for ticker in tickers:
        print(ticker)

        try:
            # df = pdr.get_data_yahoo(ticker, start="2010-01-01", interval='w')
            df = yfin.download(ticker, start='2010-01-01', interval='1wk')
            
            df.rename(columns={'Adj Close': ticker}, inplace=True)
            
            df['100ma'] = df['Close'].rolling(window=100).mean()
            df['ratio'] = (df['Close'] / df['100ma']) - 1
            df['pct_change'] = df[ticker].pct_change()
            
            df[ticker + '_twr'] = ((1 + df['pct_change']).cumprod() - 1).fillna(0)
            df[ticker + '_mdd'] = (1 + df[ticker + '_twr']) / np.maximum.accumulate(1 + df[ticker + '_twr']) - 1
            
                    
            df['pct_change_3m'] = df[ticker].pct_change(periods=13)
            df['pct_change_12m'] = df[ticker].pct_change(periods=52)
            df['std_3y'] = df['pct_change'].rolling(window=156).std() * math.sqrt(52)
            df['z-score_3m'] = df['pct_change_3m']/df['std_3y']
            df['z-score_12m'] = df['pct_change_12m']/df['std_3y']
            df['momentum'] = (df['z-score_3m']+df['z-score_12m'])/2
            
            df.to_excel('out/' + ticker +  '.xlsx', sheet_name=ticker)

            print('out/' + ticker +  '.xlsx')
            
            
            fig = plt.figure(constrained_layout=True, figsize=(20, 10))
            spec = fig.add_gridspec(ncols=1, nrows=4, height_ratios=[3, 1, 1, 1])
            
            ax1 = fig.add_subplot(spec[0, 0])
            ax1.plot(df['100ma'], label='100 SMA', linewidth=1)
            ax1.legend(loc='upper left')
            ax1.title.set_text(ticker + ' Momentum')
        
            candlestick_ohlc(ax1, zip(mdates.date2num(df.index.to_pydatetime()), df['Open'], df['High'], df['Low'], df['Close']), 
        		width=0.6, colorup='green', colordown='red', alpha=0.75)
        
            ax1.grid(True)
            
            ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
            ax2.plot(df['momentum'], label='Momentum Score')
            ax2.legend(loc='upper left')
            ax2.grid(True)
        	
            ax3 = fig.add_subplot(spec[2, 0], sharex=ax1)
            ax3.plot(df['ratio'], label='Close / 100ma')
            ax3.legend(loc='upper left')
            ax3.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
            ax3.grid(True)
        
            ax4 = fig.add_subplot(spec[3, 0], sharex=ax1)
            ax4.plot(df[ticker + '_mdd'], label='Drawdown')
            ax4.legend(loc='upper left')
            ax4.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
            ax4.grid(True)
    
            plt.savefig('out/' + ticker  + '.png')
            plt.close()
            
#            m[ticker] = df['momentum'].tail(52)
            m[ticker] = df['momentum'].tail(260)
            
            if df['momentum'].iloc[-1] > m[tickers[0]].iloc[-1]:
                print(ticker)
        except:
            raise

            
            
    m.to_excel('out/' + tickers[0] + '_momentum_matrix.xlsx')

    
    dates = m.tail(50).index.date.tolist()
    momentum = [[round(col-row[0], 1) for col in row] for row in m.tail(50).to_numpy()]
    
    
    plt.figure(figsize=(16, 16))
    rdgn = sns.diverging_palette(h_neg=220, h_pos=20, s=99, l=55, sep=3, as_cmap=True)

    
    ax = sns.heatmap(momentum, linewidth=0.5, cmap=rdgn, center=0.00, xticklabels=tickers, yticklabels=[date_obj.strftime('%Y%m%d') for date_obj in dates])
    plt.title(tickers[0] + ' Momentum')
#    plt.show()

    plt.savefig('out/' + tickers[0] + '_heatmap.png')
    plt.close()
        
    


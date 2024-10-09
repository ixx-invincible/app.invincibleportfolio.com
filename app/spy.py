# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:22:27 2020

@author: TerryLaw
"""

from datetime import datetime, timezone, timedelta

import ffn
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import yfinance as yfin
yfin.pdr_override()


def spy_analysis():
    start='2004-12-31'
    
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        start='2005-01-01'

    df_spy_daily = yfin.download('spy', start=start, end=datetime.today())
    df_spy_weekly = yfin.download('spy', start=start, end=datetime.today(), interval="1wk")

    df_spy_daily.dropna(axis = 0, how ='any').to_excel('static/etfs/spy_daily.xlsx')
    df_spy_weekly.dropna(axis = 0, how ='any').to_excel('static/etfs/spy_weekly.xlsx')


    df_vix_daily = yfin.download('^VIX', start=start, end=datetime.today())
    df_vix_weekly = yfin.download('^VIX', start=start, end=datetime.today(), interval="1wk")

    df_vix_daily.dropna(axis = 0, how ='any').to_excel('static/etfs/vix_daily.xlsx')
    df_vix_weekly.dropna(axis = 0, how ='any').to_excel('static/etfs/vix_weekly.xlsx')


    perf = df_spy_daily['Adj Close'].calc_stats()

    perf.stats.to_excel('static/etfs/spy_stats.xlsx')
    perf.return_table.to_excel('static/etfs/spy_monthly_returns.xlsx')

    fig = plt.figure(constrained_layout=True, figsize=(10, 5))
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

    ax1 = fig.add_subplot(spec[0, 0])
    ax1.plot(df_spy_daily['Adj Close'], label='SPY', linewidth=2)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax2 = fig.add_subplot(spec[1, 0])
    ax2.plot(perf.prices.to_drawdown_series(), label='Drawdown')
    ax2.legend(loc='lower left')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax2.grid(True)

    plt.savefig('static/etfs/spy.png')


    fig = plt.figure(constrained_layout=True, figsize=(10, 5))
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

    ax1 = fig.add_subplot(spec[0, 0])
    ax1.plot(df_spy_daily['Adj Close'].rebase(), label='SPY', linewidth=2)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax2 = fig.add_subplot(spec[1, 0])
    ax2.plot(perf.prices.to_drawdown_series(), label='Drawdown')
    ax2.legend(loc='lower left')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax2.grid(True)

    plt.savefig('static/etfs/spy_rebase.png')

    plt.close()


    ## merge spy and vix
    df_spy_vix = df_spy_daily.join(df_vix_daily['Close'], lsuffix='_spy', rsuffix='_vix')

    df_spy_vix['year'] = df_spy_vix.index.year

    ## calculate 20 days average of spy
    df_spy_vix['sma20'] = df_spy_vix['Adj Close'].rolling(20).mean()


    ## daily, 5 days, 10 days, 20 days rolling return
    df_spy_vix['daily_return'] = df_spy_vix['Adj Close'].pct_change()
    df_spy_vix['5d_return'] = df_spy_vix['Adj Close'].pct_change(5)
    df_spy_vix['10d_return'] = df_spy_vix['Adj Close'].pct_change(10)
    df_spy_vix['20d_return'] = df_spy_vix['Adj Close'].pct_change(20)

    ## calculate low pct_change
    df_spy_vix['1d_low_pct_change'] = df_spy_vix['Low'] / df_spy_vix['Close_spy'].shift(1) - 1
    df_spy_vix['5d_low_pct_change'] = df_spy_vix['Low'].rolling(5).min() / df_spy_vix['Close_spy'].shift(5) - 1
    df_spy_vix['10d_low_pct_change'] = df_spy_vix['Low'].rolling(10).min() / df_spy_vix['Close_spy'].shift(10) - 1
    df_spy_vix['20d_low_pct_change'] = df_spy_vix['Low'].rolling(20).min() / df_spy_vix['Close_spy'].shift(20) - 1
    
    # df_spy_vix.dropna(axis = 0, how ='any').to_excel('static/etfs/spy_vix_daily.xlsx')
    df_spy_vix.to_excel('static/etfs/spy_vix_daily.xlsx')


    ## merge spy_weekly and vix_weekly
    df_spy_vix_weekly = df_spy_weekly.join(df_vix_weekly['Close'], lsuffix='_spy', rsuffix='_vix')

    df_spy_vix_weekly = df_spy_vix_weekly.dropna(axis = 0, how ='any')

    df_spy_vix_weekly['year'] = df_spy_vix_weekly.index.year

    # ## calculate 100 weeks average of spy
    df_spy_vix_weekly['sma100'] = df_spy_vix_weekly['Adj Close'].rolling(100).mean()


    # ## daily, 5 days, 10 days, 20 days rolling return
    df_spy_vix_weekly['weekly_return'] = df_spy_vix_weekly['Adj Close'].pct_change()
    df_spy_vix_weekly['2w_return'] = df_spy_vix_weekly['Adj Close'].pct_change(2)
    df_spy_vix_weekly['4w_return'] = df_spy_vix_weekly['Adj Close'].pct_change(4)
    df_spy_vix_weekly['13w_return'] = df_spy_vix_weekly['Adj Close'].pct_change(13)

    # ## calculate low pct_change
    df_spy_vix_weekly['1w_low_pct_change'] = df_spy_vix_weekly['Low'] / df_spy_vix_weekly['Close_spy'].shift(1) - 1
    df_spy_vix_weekly['2w_low_pct_change'] = df_spy_vix_weekly['Low'].rolling(2).min() / df_spy_vix_weekly['Close_spy'].shift(2) - 1
    df_spy_vix_weekly['4w_low_pct_change'] = df_spy_vix_weekly['Low'].rolling(4).min() / df_spy_vix_weekly['Close_spy'].shift(4) - 1
    df_spy_vix_weekly['13w_low_pct_change'] = df_spy_vix_weekly['Low'].rolling(13).min() / df_spy_vix_weekly['Close_spy'].shift(13) - 1
    
    df_spy_vix_weekly.to_excel('static/etfs/spy_vix_weekly.xlsx')


            

spy_analysis()

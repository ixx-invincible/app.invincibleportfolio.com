# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:22:27 2020

@author: TerryLaw
"""
from datetime import datetime
import ffn
# import s3fs


# fs = s3fs.S3FileSystem(anon=False)

prices = ffn.get('GLD, SPY, TLT', provider='iex', start='2021-01-01')
weekday = datetime.today().weekday()

print(prices.tail())

# prices.to_csv('s3://app.invincibleportfolio.com/out/invincible_portfolio_' + str(weekday) + '.csv')

# prices.to_csv('out/invincible_portfolio_' + str(weekday) + '.csv')

# prices.to_csv('s3://experimental/playground/temp_csv/invincible_portfolio_' + str(weekday) + '.csv', index=False)

# prices.to_csv('quote/invincible_portfolio.csv')
# prices.to_json('quote/invincible_portfolio.json', orient='index')
# prices.tail(2).to_json('quote/invincible_portfolio_latest.json', orient='records')

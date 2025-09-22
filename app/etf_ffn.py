import ffn


import matplotlib.pyplot as plt

prices = ffn.get('SPY,SPMO,QQQ', start='2000-01-01', end='2024-12-31')

## group the prices by month and take the last price of each month
monthly_prices = prices.resample('M').last()
## store the price to a csv file
monthly_prices.to_csv('spy_spmo_qqq_monthly.csv')

stats = prices.calc_stats()

# Create a figure with two subplots: price and drawdown
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot rebased prices
prices.rebase().plot(ax=ax1)
ax1.set_title('SPY, SPMO & QQQ Price (Rebased)')
ax1.set_ylabel('Rebased Price')


# Calculate and plot drawdown series for each asset
stats.prices.to_drawdown_series().plot(ax=ax2)
ax2.set_title('Drawdown Series')
ax2.set_ylabel('Drawdown')

plt.tight_layout()
fig.savefig('spy_spmo_qqq_combined.png')

stats.display()

# stats['spy'].display_monthly_returns()
## store the monthly returns to a csv file
stats['spy'].monthly_returns.to_csv('spy_monthly_returns.csv')


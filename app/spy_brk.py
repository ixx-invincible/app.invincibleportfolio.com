import ffn


prices = ffn.get('QQQ,BRK-B', start='2015-01-01')

ax = prices.rebase().plot(figsize=(10, 5))

## store the plot to a file
ax.get_figure().savefig('qqq_brk.png')

stats = prices.calc_stats()
stats.display()
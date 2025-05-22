import ffn
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def download_stock_data(symbol='SPY', interval='daily', start_date='2000-01-01', end_date=None):
    """
    Download stock historical data from Yahoo Finance for specified interval
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Downloading {symbol} {interval} data from {start_date} to {end_date}")
    
    # Download data
    stock_data = ffn.get(symbol, start=start_date, end=end_date)
    
    # Resample to weekly if needed
    if interval.lower() == 'weekly':
        stock_data = stock_data.resample('W').last()
    
    # Standardize column names
    if len(stock_data.columns) == 1:
        stock_data.columns = [symbol]
    elif 'close' in [col.lower() for col in stock_data.columns]:
        stock_data = stock_data[['close']].rename(columns={'close': symbol})
    elif 'adj close' in [col.lower() for col in stock_data.columns]:
        stock_data = stock_data[['adj close']].rename(columns={'adj close': symbol})
    
    return stock_data

def calculate_indicators(data, symbol='SPY', window=14):
    """
    Calculate RSI and EMA indicators
    """
    if symbol not in data.columns:
        available_cols = ", ".join(data.columns)
        raise ValueError(f"Data must contain '{symbol}' column. Available columns: {available_cols}")
    
    # Calculate RSI
    delta = data[symbol].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(alpha=1/window, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1/window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # Calculate 100-period EMA
    ema_100 = data[symbol].ewm(span=100, adjust=False).mean()
    
    result = pd.DataFrame({
        'Date': data.index,
        'Price': data[symbol],
        'EMA_100': ema_100,
        'RSI': rsi
    }).set_index('Date')
    
    return result.dropna()

def save_to_excel(data, symbol='SPY', interval='daily', filename=None):
    """
    Save data to Excel file with a separate sheet for the calculation explanation
    """
    if filename is None:
        filename = f'{symbol.lower()}_{interval}_indicators.xlsx'
    
    try:
        # Create explanation of the calculations
        explanation = pd.DataFrame({
            'Indicator': ['RSI', 'EMA 100'],
            'Description': [
                'Relative Strength Index (14-period) using Wilder\'s smoothing',
                '100-period Exponential Moving Average of closing prices'
            ],
            'Calculation': [
                '100 - (100 / (1 + (Avg Gain / Avg Loss)))',
                'EMA = (Price * multiplier) + (Previous EMA * (1 - multiplier)) where multiplier = 2/(100+1)'
            ],
            'Trading Use': [
                'Overbought (>70), Oversold (<30)',
                'Trend direction, Support/Resistance'
            ]
        })
        
        with pd.ExcelWriter(filename) as writer:
            data.to_excel(writer, sheet_name=f'{symbol} {interval.capitalize()} Data')
            explanation.to_excel(writer, sheet_name='Indicators Guide', index=False)
        
        print(f"\nData successfully saved to {filename}")
        print("The Excel file contains two sheets:")
        print(f"1. '{symbol} {interval.capitalize()} Data' - Price and indicators")
        print("2. 'Indicators Guide' - Explanation of calculations")
        
    except Exception as e:
        print(f"\nError saving to Excel: {e}")

def plot_data(data, symbol='SPY', interval='daily'):
    """
    Plot stock price with EMA 100 and RSI
    """
    plt.style.use('ggplot')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    # Plot price and EMA
    ax1.plot(data.index, data['Price'], label=f'{symbol} Price', color='#1f77b4', linewidth=1.5)
    ax1.plot(data.index, data['EMA_100'], label='EMA 100', color='#ff7f0e', linewidth=2)
    ax1.set_ylabel('Price ($)', fontsize=12)
    ax1.set_title(f'{symbol} {interval.capitalize()} Price with Indicators', fontsize=14, pad=20)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(fontsize=12)
    
    # Plot RSI
    ax2.plot(data.index, data['RSI'], label='RSI(14)', color='#9467bd', linewidth=1.5)
    ax2.fill_between(data.index, data['RSI'], 70, where=(data['RSI']>=70), 
                    facecolor='red', alpha=0.2, interpolate=True)
    ax2.fill_between(data.index, data['RSI'], 30, where=(data['RSI']<=30), 
                    facecolor='green', alpha=0.2, interpolate=True)
    ax2.axhline(70, linestyle='--', color='red', alpha=0.7, linewidth=1)
    ax2.axhline(30, linestyle='--', color='green', alpha=0.7, linewidth=1)
    ax2.set_ylabel('RSI', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylim(0, 100)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend(fontsize=12)
    
    plt.tight_layout()
    plt.show()

def get_user_input():
    """Get user input for symbol, interval, and date range"""
    symbol = input("Enter stock symbol (e.g., SPY, AAPL, MSFT): ").strip().upper()
    
    # Interval selection with validation
    while True:
        interval = input("Enter data interval (daily/weekly, default daily): ").strip().lower()
        if not interval:
            interval = 'daily'
            break
        if interval in ['daily', 'weekly']:
            break
        print("Please enter either 'daily' or 'weekly'")
    
    # Date range input with validation
    while True:
        try:
            years = int(input("Enter number of years of data to fetch (default 5): ") or 5)
            if years <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer for years.")
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365*years)).strftime('%Y-%m-%d')
    
    return symbol, interval, start_date, end_date

def main():
    print("Stock Technical Indicator Analyzer")
    print("--------------------------------\n")
    
    symbol, interval, start_date, end_date = get_user_input()
    
    try:
        stock_data = download_stock_data(symbol, interval, start_date, end_date)
        
        print("\nFirst few rows of downloaded data:")
        print(stock_data.head())
        
        indicators_data = calculate_indicators(stock_data, symbol)
        
        print(f"\nLast 5 {interval} periods with indicators:")
        print(indicators_data.tail())
        
        # Save to Excel
        save_to_excel(indicators_data, symbol, interval)
        
        # Plot the data
        plot_data(indicators_data, symbol, interval)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
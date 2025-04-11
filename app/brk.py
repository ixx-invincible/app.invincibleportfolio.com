import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_brkb_yearly_returns():
    """
    Fetch BRK-B historical data and calculate yearly returns.
    Returns a DataFrame with yearly returns in percentage.
    """
    try:
        # Fetch BRK-B historical data
        brkb = yf.Ticker("BRK-B")
        hist_data = brkb.history(period="max")
        
        if hist_data.empty:
            print("No data available for BRK-B")
            return None
        
        # Resample to yearly and calculate returns
        yearly_data = hist_data['Close'].resample('Y').last()
        yearly_returns = yearly_data.pct_change() * 100
        
        # Format as DataFrame
        returns_df = pd.DataFrame({
            'Year': yearly_returns.index.year,
            'Return (%)': yearly_returns.values.round(2)
        }).dropna()
        
        returns_df = returns_df.set_index('Year')
        
        # Print yearly returns
        print("\nBRK-B Yearly Returns (%):")
        print(returns_df.to_string())
        
        # Plot yearly returns
        plt.figure(figsize=(12, 6))
        plt.bar(returns_df.index, returns_df['Return (%)'], color='steelblue')
        plt.title('BRK-B Yearly Returns')
        plt.ylabel('Return (%)')
        plt.xlabel('Year')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on top of bars
        for year, ret in zip(returns_df.index, returns_df['Return (%)']):
            plt.text(year, ret, f'{ret:.1f}%', 
                    ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.show()
        
        return returns_df
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    returns = get_brkb_yearly_returns()
    if returns is not None:
        # Optionally save to CSV
        returns.to_csv('brkb_yearly_returns.csv')
        print("\nData saved to 'brkb_yearly_returns.csv'")
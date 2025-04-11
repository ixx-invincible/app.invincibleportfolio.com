import ffn
import matplotlib.pyplot as plt
import numpy as np

def analyze_invincible_portfolio():
    """
    Analyze and visualize the Invincible Portfolio (GLD, SPY, TLT)
    with properly spaced charts
    """
    try:
        # Get historical prices
        print("Fetching historical data for GLD, SPY, TLT...")
        prices = ffn.get('GLD, SPY, TLT', start='2020-01-01')
        
        if prices.empty:
            print("No data returned - please check your tickers and date range")
            return None

        # Create figure with proper spacing
        plt.figure(figsize=(12, 12))
        
        # First subplot: Individual assets rebased
        plt.subplot(2, 1, 1)
        rebased = prices.rebase()
        for ticker in rebased.columns:
            plt.plot(rebased.index, rebased[ticker], label=ticker, linewidth=2)
        
        plt.title('Individual Asset Performance (Rebased to 100)', pad=20)
        plt.ylabel('Value (Rebased to 100)', labelpad=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='upper left')
        plt.ylim(50, 240)  # Set consistent y-axis limits
        
        # Calculate equal-weighted portfolio
        portfolio = prices.pct_change().dropna()
        portfolio['EqualWeight'] = portfolio.mean(axis=1)
        portfolio_value = (1 + portfolio['EqualWeight']).cumprod() * 100
        
        # Second subplot: Equal-weighted portfolio
        plt.subplot(2, 1, 2)
        plt.plot(portfolio_value.index, portfolio_value, 
                label='Equal-Weighted Portfolio', 
                linewidth=2, 
                color='purple')
        
        plt.title('Equal-Weighted Portfolio Performance (1/3 each in GLD, SPY, TLT)', pad=20)
        plt.ylabel('Portfolio Value (Starting at 100)', labelpad=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='upper left')
        plt.ylim(80, 160)  # Match y-axis with top chart
        
        # Add reference lines
        for level in [80, 100, 120, 140, 160]:
            plt.axhline(y=level, color='gray', linestyle=':', alpha=0.3)
        
        # Adjust layout with more padding
        plt.tight_layout(pad=3.0)
        plt.savefig('invincible_portfolio_analysis_fixed.png', 
                  dpi=300, 
                  bbox_inches='tight')
        print("\nSaved corrected analysis charts as: invincible_portfolio_analysis_fixed.png")
        
        # Show the plot
        plt.show()
        
        return prices, portfolio_value
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None

if __name__ == "__main__":
    analyze_invincible_portfolio()
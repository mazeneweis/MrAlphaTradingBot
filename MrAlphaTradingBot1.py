# This version of MrAlpha calculates the correlation between two securities, just enter the ticker of
# the two securities you wish to compare, and MrAlpha should give you a rating of how correlated the securities are
import yfinance as yf
import pandas as pd
import os

# Suppress yfinance progress output
yf.pdr_override()

# Function to get the correlation rating
def get_correlation_rating(correlation_coefficient):
    if 0.7 <= correlation_coefficient <= 1:
        return 'Highly Correlated'
    elif 0.3 <= correlation_coefficient < 0.7:
        return 'Somewhat Correlated'
    elif -0.3 <= correlation_coefficient < 0.3:
        return 'Not Correlated'
    elif -0.7 <= correlation_coefficient < -0.3:
        return 'Somewhat Negatively Correlated'
    else:
        return 'Negatively Correlated'

# Main function
def main():
    # Ask user for tickers
    ticker1 = input('Enter the ticker for Security 1: ').upper()
    ticker2 = input('Enter the ticker for Security 2: ').upper()

    # Suppress error messages by redirecting stderr
    with open(os.devnull, 'w') as fnull:
        original_stderr = os.dup(2)
        os.dup2(fnull.fileno(), 2)

        # Fetch data from Yahoo Finance for ticker1
        security1 = yf.download(ticker1, period='1y', progress=False)['Adj Close']
        if security1.empty:
            print(f"Ticker {ticker1} not found, please check your spelling")
            return

        # Fetch data from Yahoo Finance for ticker2
        security2 = yf.download(ticker2, period='1y', progress=False)['Adj Close']
        if security2.empty:
            print(f"Ticker {ticker2} not found, please check your spelling")
            return

        # Restore original stderr
        os.dup2(original_stderr, 2)

    # Calculate daily returns
    returns1 = security1.pct_change().dropna()
    returns2 = security2.pct_change().dropna()

    # Merge the returns data
    merged_returns = pd.concat([returns1, returns2], axis=1)
    merged_returns.columns = [ticker1, ticker2]

    # Calculate correlation
    correlation = merged_returns.corr().iloc[0, 1]

    # Print results
    print(f'Correlation between {ticker1} and {ticker2}: {correlation:.2f}')
    print(f'Rating: {get_correlation_rating(correlation)}')

if __name__ == '__main__':
    main()

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

chosen_stock = input("Chosen stocks for analysis: ", )
data_check = yf.download(chosen_stock, period="1y", interval="1d")

if data_check.empty:
    print(f"The stock ticker '{chosen_stock}' is invalid or has no data available.")
else:
    data_check['Close'].plot(title=f'Daily Closing Prices for {chosen_stock} Over the Past Year', figsize=(10, 6))

    # Going to start with tech stock, so my tickers will be the 15 majors stocks listed in NASDAQ
    tickers_15_NQ = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'META', 'AVGO', 'GOOGL', 'GOOG', 'TSLA', 'NFLX', 'PLTR', 'COST', 'AMD', 'ASML', 'CSCO']

    history_data = yf.download(tickers_15_NQ, period='1y', interval='1d', group_by='ticker')

    if isinstance(history_data.columns, pd.MultiIndex):
        close_prices = history_data.xs('Close', level=1, axis=1)
    else:
        close_prices = history_data['Close']

    returns = close_prices.dropna(how = 'all')

    # Analyze financial ratios for each stock in the top 15 NASDAQ tech stocks, and compare it with the chosen stock
    # Going to focus on Gross Margin, Operating Margin, Return on Assets, Return on Equity and Trailing P/E Ratio
    ratio = {}
    for i in tickers_15_NQ:
        stock = yf.Ticker(i)
        info = stock.info

        ratio[i] = {
            'Gross Margins': info.get('grossMargins'),
            'Operating Margins': info.get('operatingMargins'),
            'Return On Assets': info.get('returnOnAssets'),
            'Return On Equity': info.get('returnOnEquity'),
            'Trailing PE': info.get('trailingPE')
        }
        ratio_graph = pd.DataFrame(ratio).T

    ratio_chosen_stock = {}
    stock_chosen_ratio = yf.Ticker(chosen_stock)
    info_chosen = stock_chosen_ratio.info
    ratio_chosen_stock[chosen_stock] = {
        'Gross Margins': info_chosen.get('grossMargins'),
        'Operating Margins': info_chosen.get('operatingMargins'),
        'Return On Assets': info_chosen.get('returnOnAssets'),
        'Return On Equity': info_chosen.get('returnOnEquity'),
        'Trailing PE': info_chosen.get('trailingPE')
    }
    ratio_graph_chosen_stock = pd.DataFrame(ratio_chosen_stock).T

    print(ratio_graph)
    print(ratio_graph_chosen_stock)

    

    stock_graph = returns.plot(figsize=(14, 8), lw=1)
    stock_graph.set_title('Daily Charts of Major NASDAQ Tech Stocks Over the Past Year', fontsize=16)
    stock_graph.set_xlabel('Date', fontsize=14)
    stock_graph.set_ylabel('Price (USD)', fontsize=14)

    plt.show()





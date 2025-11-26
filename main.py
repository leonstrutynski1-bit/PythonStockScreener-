import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

chosen_stock = input("Chosen stocks for analysis: ", )
data_check = yf.download(chosen_stock, period="1y", interval="1d")

if data_check.empty:
    print(f"The stock ticker '{chosen_stock}' is invalid or has no data available.")
else:
    
    # Going to start with tech stock, so my tickers will be the 15 majors stocks listed in NASDAQ
    tickers_15_NQ = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'META', 'AVGO', 'GOOGL', 'GOOG', 'TSLA', 'NFLX', 'PLTR', 'COST', 'AMD', 'ASML', 'CSCO']

    history_data = yf.download(tickers_15_NQ, period='1y', interval='1d', group_by='ticker')

    if isinstance(history_data.columns, pd.MultiIndex):
        close_prices = history_data.xs('Close', level=1, axis=1)
    else:
        close_prices = history_data['Close']

    returns_nq100 = close_prices.dropna(how = 'all')

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

        mean_ratios = ratio_graph.mean()
        median_ratios = ratio_graph.median()

    print("Median Financial Ratios for Top 15 NASDAQ Tech Stocks:")
    print(median_ratios)
    print("\nMean Financial Ratios for Top 15 NASDAQ Tech Stocks:")
    print(mean_ratios)
    

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

    print(f"\nFinancial Ratios for Chosen Stock '{chosen_stock}':")
    print(ratio_graph_chosen_stock)
    print('')

    for ratio_name in mean_ratios.index:
        if ratio_graph_chosen_stock[ratio_name].values[0] is not None:
            if ratio_graph_chosen_stock[ratio_name].values[0] > mean_ratios[ratio_name]:
                print(f"{chosen_stock} has a higher {ratio_name} than the average of the top 15 NASDAQ tech stocks.")
            else:
                print(f"{chosen_stock} has a lower {ratio_name} than the average of the top 15 NASDAQ tech stocks.")
    
    

    graph_client = input("\nDo you want to see the stock price graph for the chosen stock? (yes/no): ", ).strip().lower()
    if graph_client == 'yes':
        data_check['Close'].plot(title=f'Daily Closing Prices for {chosen_stock} Over the Past Year', figsize=(10, 6))


        stock_graph = returns_nq100.plot(figsize=(14, 8), lw=1)
        stock_graph.set_title('Daily Charts of Major NASDAQ Tech Stocks Over the Past Year', fontsize=16)
        stock_graph.set_xlabel('Date', fontsize=14)
        stock_graph.set_ylabel('Price (USD)', fontsize=14)

        plt.show()





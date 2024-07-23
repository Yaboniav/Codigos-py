# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 08:22:46 2024

@author: Yaboniav
"""

import yfinance as yf
import pandas as pd
import numpy as np
import os
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD

# List of companies with their tickers
companies = {
    'Bancolombia': 'CIB',
    'ISA': 'ISA',
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Johnson & Johnson': 'JNJ',
    'Procter & Gamble': 'PG',
    'Coca-Cola': 'KO',
    'Ecopetrol': 'ECOPETROL.CL'
}

# Define the period for historical data (up to 5 years)
period = '5y'

# Directory to save the files
save_directory = r'C:\Users\yaboniav\Documents\Finanzas\Historial de acciones'

# Create directory if it does not exist
os.makedirs(save_directory, exist_ok=True)

# Initialize a dictionary to hold data
historical_data = {}

# Fetch historical data for each company
for company, ticker in companies.items():
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    
    # Calculate Technical Indicators
    
    # Calculate Stochastic Oscillator
    high_14 = hist['High'].rolling(window=14).max()
    low_14 = hist['Low'].rolling(window=14).min()
    hist['%K'] = (hist['Close'] - low_14) * 100 / (high_14 - low_14)
    hist['%D'] = hist['%K'].rolling(window=3).mean()
    
    # Simple Moving Average (SMA)
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
    
    # Exponential Moving Average (EMA)
    hist['EMA_12'] = hist['Close'].ewm(span=12, adjust=False).mean()
    hist['EMA_26'] = hist['Close'].ewm(span=26, adjust=False).mean()
    
    # Relative Strength Index (RSI)
    rsi = RSIIndicator(hist['Close'])
    hist['RSI'] = rsi.rsi()
    
    # Bollinger Bands
    bollinger = BollingerBands(hist['Close'])
    hist['BB_High'] = bollinger.bollinger_hband()
    hist['BB_Low'] = bollinger.bollinger_lband()
    hist['BB_Mid'] = bollinger.bollinger_mavg()
    
    # MACD
    macd = MACD(hist['Close'])
    hist['MACD'] = macd.macd()
    hist['MACD_Signal'] = macd.macd_signal()
    hist['MACD_Diff'] = macd.macd_diff()
    
    # Fibonacci Levels (Using High and Low of the entire period)
    high_price = hist['High'].max()
    low_price = hist['Low'].min()
    diff = high_price - low_price
    hist['Fibo_23.6'] = high_price - (0.236 * diff)
    hist['Fibo_38.2'] = high_price - (0.382 * diff)
    hist['Fibo_50'] = (high_price + low_price) / 2
    hist['Fibo_61.8'] = high_price - (0.618 * diff)
    hist['Fibo_78.6'] = high_price - (0.786 * diff)
    
    historical_data[company] = hist
    
    # Save to CSV file
    csv_file_path = os.path.join(save_directory, f'{company}.csv')
    hist.to_csv(csv_file_path)

# Create a new DataFrame to hold summary statistics
summary_data = []

for company, data in historical_data.items():
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    avg_price = data['Close'].mean()
    summary_data.append({
        'Company': company,
        'Max Price': max_price,
        'Min Price': min_price,
        'Average Price': avg_price
    })

summary_df = pd.DataFrame(summary_data)

# Save summary statistics to a CSV file
summary_csv_path = os.path.join(save_directory, 'Summary_Statistics.csv')
summary_df.to_csv(summary_csv_path, index=False)

print(f"Archivos CSV creados exitosamente en: '{save_directory}'")
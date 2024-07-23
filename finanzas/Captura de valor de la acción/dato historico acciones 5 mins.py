# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 19:59:38 2024

@author: Yaboniav
"""

import os
import yfinance as yf
import pandas as pd

# List of companies with their tickers
companies = {
    'Bancolombia': 'CIB',
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Johnson & Johnson': 'JNJ',
    'Procter & Gamble': 'PG',
    'Coca-Cola': 'KO',
    'Ecopetrol': 'EC',
    'Tesla': 'TSLA',
    'Amazon':'AMZN',
    'NU bank': 'NU',
    'BYD': 'BYDDF',
    'PDD Holdings Inc.':'PDD',
    'Airbnb, Inc.': 'ABNB',
    'EOG Resources, Inc.': 'EOG',
    'NetEase Inc. ADR': 'NTES',
    'ST Microelectronics': 'STM',
    'Steel Dynamics, Inc.': 'STLD',
    'Tenaris S.A. ADR': 'TS',
    'Lantheus Holdings Inc': 'LNTH',
    'Roivant Sciences Ltd': 'ROIV',
    'Eagle Materials Inc.': 'EXP',
    'Nextracker Inc': 'NXT',
    'MINISO Group Holding Ltd ADR': 'MNSO',
    'Marathon Digital Holdings Inc': 'MARA',
    'Atkore Inc': 'ATKR',
    'Axcelis Technologies Inc': 'ACLS',
    'Alpha Metallurgical Resources Inc': 'AMR',
    'Alkermes plc': 'ALKS',
    'Hafnia Ltd': 'HAFN',
    'Liberty Energy Inc': 'LBRT',
    'Torm Plc': 'TRMD',
    'Euronav NV': 'EURN',
    'Consol Energy Inc': 'CEIX',
    'International Seaways Inc': 'INSW',
    'Tecnoglass Inc': 'TGLS',
    'Teekay Tankers Ltd': 'TNK',
    'Atour Lifestyle Holdings Ltd ADR': 'ATAT',
    'Protagonist Therapeutics Inc': 'PTGX',
    'Harmony Biosciences Holdings Inc': 'HRMY',
    'Dorian LPG Ltd': 'LPG',
    'Danaos Corporation': 'DAC',
    'Inmode Ltd': 'INMD',
    'Central Puerto ADR': 'CEPU',
    'Opera Ltd ADR': 'OPRA',
    'Global Ship Lease Inc': 'GSL',
    'Target Hospitality Corp': 'TH',
    'DRDGOLD Ltd. ADR': 'DRD',
    'Ardmore Shipping Corp': 'ASC',
    'Yalla Group Limited ADR': 'YALA',
    'SIGA Technologies Inc': 'SIGA',
    'Bit Digital Inc': 'BTBT',
    'Consolidated Water Co. Ltd.': 'CWCO',
    'Hudson Technologies, Inc.': 'HDSN',
    'Semler Scientific Inc': 'SMLR',
    'Medifast Inc': 'MED',
    'Scynexis Inc': 'SCYX',
    'Profire Energy Inc': 'PFIE',
    'Spero Therapeutics Inc': 'SPRO',
    'QuantaSing Group Ltd ADR': 'QSG',
    'Surgepays Inc': 'SURG',
    'Pyxis Tankers Inc': 'PXS',
    'Performance Shipping Inc': 'PSHG',
    'MEI Pharma Inc': 'MEIP',
    'S&P 500': '^GSPC',
    'AXON': 'AXON',
    'Enovix Corp': 'ENVX',
    'KKR & CO new': 'KKR'
}


# Define the period for historical data (up to 5 years)
period = '1mo'

# Directory to save the files
save_directory = r'C:\Users\yaboniav\Documents\Finanzas\Historial de acciones cada 5 min'
save_dir2 =r'C:\Users\yaboniav\Documents\Finanzas\Análisis de acciones cada 5 min'
# Create directory if it does not exist
os.makedirs(save_directory, exist_ok=True)

# Function to calculate RSI
def calculate_rsi(data, window):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate Bollinger Bands
def calculate_bollinger_bands(data, window):
    sma = data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    bollinger_high = sma + (std * 2)
    bollinger_low = sma - (std * 2)
    return sma, bollinger_high, bollinger_low

# Function to calculate MACD
def calculate_macd(data, short_window, long_window, signal_window):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    macd_diff = macd - signal
    return macd, signal, macd_diff

# Function to calculate Stochastic Oscillator
def calculate_stochastic_oscillator(data, window):
    low_14 = data['Low'].rolling(window=window).min()
    high_14 = data['High'].rolling(window=window).max()
    data['%K'] = 100 * (data['Close'] - low_14) / (high_14 - low_14)
    data['%D'] = data['%K'].rolling(window=3).mean()
    return data

# Initialize a dictionary to hold data
historical_data = {}

# Fetch historical data for each company
for company, ticker in companies.items():
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval='5m')
    
    # Calculate Technical Indicators
    
    # Simple Moving Average (SMA)
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
    
    # Exponential Moving Average (EMA)
    hist['EMA_12'] = hist['Close'].ewm(span=12, adjust=False).mean()
    hist['EMA_26'] = hist['Close'].ewm(span=26, adjust=False).mean()
    
    # Relative Strength Index (RSI)
    hist['RSI'] = calculate_rsi(hist, 14)
    
    # Bollinger Bands
    hist['BB_Mid'], hist['BB_High'], hist['BB_Low'] = calculate_bollinger_bands(hist, 20)
    
    # MACD
    hist['MACD'], hist['MACD_Signal'], hist['MACD_Diff'] = calculate_macd(hist, 12, 26, 9)
    
    # Stochastic Oscillator
    hist = calculate_stochastic_oscillator(hist, 14)
    
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

#summary_df = pd.DataFrame(summary_data)

# Save summary statistics to a CSV file
#summary_csv_path = os.path.join(save_directory, 'Summary_Statistics.csv')
#summary_df.to_csv(summary_csv_path, index=False)

print(f"Archivos CSV creados exitosamente en: '{save_directory}'")
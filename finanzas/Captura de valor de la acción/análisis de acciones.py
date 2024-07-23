"""
Created on Sat Jul 13 23:31:23 2024

@author: yaboniav
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Listado de acciones con sus respectivos símbolos
acciones = {
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
    'KKR & CO new': 'KKR',
    'SQQQ': 'SQQQ',
    'McDonalds':'MCD',
    'Nvidia': 'NVDA',
    'Vanguard S&P 500 ETF': 'VOO'
}

# Definir el intervalo de tiempo
hoy = datetime.now()
inicio_30_dias = hoy - timedelta(days=30)
inicio_2_anos = hoy - timedelta(days=730)
inicio_5_anos = hoy - timedelta(days=5*365)  # 5 años a partir del año en curso

# Listas para acumular resultados
resultados_30_dias = []
resultados_2_anos = []
resultados_dividendos = []

# Obtener datos
for nombre, simbolo in acciones.items():
    # Datos de 30 días
    try:
        data_30_dias = yf.download(simbolo, start=inicio_30_dias, end=hoy)
        precio_dia_1 = data_30_dias['Close'].iloc[0] if not data_30_dias.empty else 0
        precio_dia_30 = data_30_dias['Close'].iloc[-1] if not data_30_dias.empty else 0
        porcentaje_cambio = ((precio_dia_30 - precio_dia_1) / precio_dia_1) * 100 if precio_dia_1 != 0 else 0
        resultados_30_dias.append({
            'Accion': nombre,
            'Precio Dia 1': precio_dia_1,
            'Precio Dia 30': precio_dia_30,
            '% Cambio': porcentaje_cambio
        })
    except Exception as e:
        print(f"No se pudieron obtener datos para {nombre} ({simbolo}): {e}")

    # Datos de 2 años
    try:
        data_2_anos = yf.download(simbolo, start=inicio_2_anos, end=hoy)
        if not data_2_anos.empty:
            data_2_anos['Accion'] = nombre
            data_2_anos['Fecha'] = data_2_anos.index
            resultados_2_anos.append(data_2_anos[['Fecha', 'Accion', 'Close']])
        else:
            empty_df = pd.DataFrame({'Fecha': [inicio_2_anos], 'Accion': [nombre], 'Close': [0]})
            resultados_2_anos.append(empty_df)
    except Exception as e:
        print(f"No se pudieron obtener datos para {nombre} ({simbolo}): {e}")

    # Datos de dividendos
    try:
        data_dividendos = yf.Ticker(simbolo).dividends
        data_dividendos.index = pd.to_datetime(data_dividendos.index).tz_localize(None)
        data_dividendos = data_dividendos[(data_dividendos.index >= inicio_5_anos) & (data_dividendos.index <= hoy)]
        if not data_dividendos.empty:
            dividendos_anuales = data_dividendos.resample('Y').sum()
            num_entregas = data_dividendos.groupby(data_dividendos.index.year).size()
            resultado = {
                'Accion': nombre,
                'Entrega Dividendos': 'Si',
                'Dividendos Año 1': dividendos_anuales.iloc[-5] if len(dividendos_anuales) >= 5 else 0,
                'Dividendos Año 2': dividendos_anuales.iloc[-4] if len(dividendos_anuales) >= 4 else 0,
                'Dividendos Año 3': dividendos_anuales.iloc[-3] if len(dividendos_anuales) >= 3 else 0,
                'Dividendos Año 4': dividendos_anuales.iloc[-2] if len(dividendos_anuales) >= 2 else 0,
                'Dividendos Año 5': dividendos_anuales.iloc[-1] if len(dividendos_anuales) >= 1 else 0,
                'Num Entrega Año': num_entregas.iloc[-1] if len(num_entregas) > 0 else 0
            }
        else:
            resultado = {
                'Accion': nombre,
                'Entrega Dividendos': 'No',
                'Dividendos Año 1': 0,
                'Dividendos Año 2': 0,
                'Dividendos Año 3': 0,
                'Dividendos Año 4': 0,
                'Dividendos Año 5': 0,
                'Num Entrega Año': 0
            }
        resultados_dividendos.append(resultado)
    except Exception as e:
        print(f"No se pudieron obtener datos de dividendos para {nombre} ({simbolo}): {e}")

# Convertir listas a DataFrames
df_30_dias = pd.DataFrame(resultados_30_dias)
df_2_anos = pd.concat(resultados_2_anos)
df_dividendos = pd.DataFrame(resultados_dividendos)

# Guardar resultados en CSV
df_30_dias.to_csv(r'C:\Users\yaboniav\Documents\Finanzas\analisis de acciones\precios_30_dias.csv', index=False)
df_2_anos.to_csv(r'C:\Users\yaboniav\Documents\Finanzas\analisis de acciones\precios_2_anos.csv', index=False)
df_dividendos.to_csv(r'C:\Users\yaboniav\Documents\Finanzas\analisis de acciones\dividendos_5_anos.csv', index=False)

print("Datos guardados exitosamente.")

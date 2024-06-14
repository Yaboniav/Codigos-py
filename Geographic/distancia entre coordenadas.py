# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:06:14 2023

@author: yaboniav
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs
from pylab import *
from numpy import *
import math

Data_recos = pd.read_csv('D:/OneDrive - Grupo EPM/3. CENS/7. solicitudes de información/9. Maria Camila Arenas/base radioenlaces_1.csv',sep=';',decimal='.',dtype='object') #,dtype='object'
#def distancia(lat1, lon1, lat2, lon2):
    # Radio de la tierra en km
radio_tierra = 6371

    # Convertir las coordenadas de grados a radianes
Data_recos[['LATITUD final', 'LONGITUD final', 'LATITUD ini', 'LONGITUD ini']].astype(float)
Data_recos.dtypes
Data_recos['LATITUD final']=Data_recos['LATITUD final'].astype('float')
Data_recos['LONGITUD final']=Data_recos['LONGITUD final'].astype('float')
Data_recos['LATITUD ini']=Data_recos['LATITUD ini'].astype('float')
Data_recos['LONGITUD ini']=Data_recos['LONGITUD ini'].astype('float')
#Data_recos['Alimentador.UIS INICIAL']=Data_recos['Alimentador.UIS INICIAL'].astype('string')
Data_recos.dtypes
Data_recos['lat1'] = ''
Data_recos['lon1'] = ''
Data_recos['lat2'] = ''
Data_recos['lon2'] = ''
Data_recos['delta_lon'] = ''
Data_recos['coseno'] = ''
Data_recos['distancia [km]'] = ''

for j in range (0, len(Data_recos)):
    Data_recos['lat2'].iloc[j]=math.radians(Data_recos['LATITUD final'].iloc[j])
    Data_recos['lon2'].iloc[j]=math.radians(Data_recos['LONGITUD final'].iloc[j])
    Data_recos['lat1'].iloc[j]=math.radians(Data_recos['LATITUD ini'].iloc[j])
    Data_recos['lon1'].iloc[j]=math.radians(Data_recos['LONGITUD ini'].iloc[j])

Data_recos['delta_lon'] = Data_recos['lon2'] - Data_recos['lon1']

# Fórmula de Haversine
for j in range (0, len(Data_recos)):
    Data_recos['coseno'].iloc[j] = math.sin(Data_recos['lat1'].iloc[j])* math.sin(Data_recos['lat2'].iloc[j]) + (math.cos(Data_recos['lat1'].iloc[j]) * math.cos(Data_recos['lat2'].iloc[j])*math.cos(Data_recos['delta_lon'].iloc[j]))
    Data_recos['distancia [km]'].iloc[j] = radio_tierra * math.acos(Data_recos['coseno'].iloc[j])

del(Data_recos['lat1'])
del(Data_recos['lat2'])
del(Data_recos['lon1'])
del(Data_recos['lon2'])
del(Data_recos['delta_lon'])
del(Data_recos['coseno'])
del(Data_recos['LATITUD ini'])
del(Data_recos['LONGITUD ini'])
Data_recos.to_excel('D:/OneDrive - Grupo EPM/3. CENS/7. solicitudes de información/9. Maria Camila Arenas/resultados reconectadores.xlsx',index=False) 


# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:12:27 2023

@author: yaboniav
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:52:15 2022

@author: yaboniav
"""

import pandas as pd
#import numpy as np

#import seaborn as plt
#from IPython.display import display
#from IPython.core.pylabtools import figsize, getfigs

#from pylab import *
#from numpy import *

Data_tensiones = pd.read_csv('D:/archivos txt Diagnostico/Data_tensiones.csv',sep=';',decimal='.')
Data_Trafo_S_bi = pd.read_csv('D:/archivos txt Diagnostico/Data_Trafo_S_bi.csv',sep=';',decimal='.')
Data_Trafo_S_tri = pd.read_csv('D:/archivos txt Diagnostico/Data_Trafo_S_tri.csv',sep=';',decimal='.')
Data_I_kA = pd.read_csv('D:/archivos txt Diagnostico/Data_I_kA.csv',sep=';',decimal='.')
Data_P_MW = pd.read_csv('D:/archivos txt Diagnostico/Data_P_MW.csv',sep=';',decimal='.')
Data_Q_MVAr = pd.read_csv('D:/archivos txt Diagnostico/Data_Q_MVAr.csv',sep=';',decimal='.')
Data_Per_MW = pd.read_csv('D:/archivos txt Diagnostico/Data_Per_MW.csv',sep=';',decimal='.')
coordenadas_nodos = pd.read_csv('D:/archivos txt Diagnostico/coordenadas nodos.csv',sep=';',decimal='.')
lineas_nodos = pd.read_csv('D:/archivos txt Diagnostico/lineas_nodos.csv',sep=';',decimal='.')
loads = pd.read_csv('D:/archivos txt Diagnostico/loads.csv',sep=';',decimal=',')
info_base_redes = pd.read_csv('D:/archivos txt Diagnostico/redes.csv',sep=';',decimal='.',encoding='latin-1')
graf_kv_max_base = pd.read_csv('D:/graficando data frames/1. input/graf_kv_max_base.csv',sep=';',decimal='.')#D:\graficando data frames\1. input
graf_kv_min_base = pd.read_csv('D:/graficando data frames/1. input/graf_kv_min_base.csv',sep=';',decimal='.')
graf_Ik_max_base = pd.read_csv('D:/graficando data frames/1. input/graf_Ik_max_base.csv',sep=';',decimal='.')
CT_Ik = pd.read_csv('D:/graficando data frames/1. input/corrientes CTs.csv',sep=';',decimal='.')

import tkinter as tk
from tkinter import ttk

# Función para filtrar el DataFrame, cerrar la ventana y guardar en CSV
def filter_dataframe():
    selected_feeder1 = combobox1.get()
    selected_feeder2 = combobox2.get()
    tensiones_df = Data_tensiones[Data_tensiones['Feeder'].isin([selected_feeder1, selected_feeder2])]
    tensiones_df.to_csv('D:/tensiones_data.csv',sep=';',decimal='.',index=False)
    root.destroy()  # Cierra la ventana

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Filtrar DataFrame")

# Crear comboboxes (menús desplegables)
combobox1 = ttk.Combobox(root, values=list(Data_tensiones['Feeder'].unique()))
combobox2 = ttk.Combobox(root, values=list(Data_tensiones['Feeder'].unique()))

# Botón para aplicar el filtro y guardar en CSV
button = tk.Button(root, text="Filtrar, Guardar y Cerrar", command=filter_dataframe)

# Posicionamiento de los widgets
combobox1.pack()
combobox2.pack()
button.pack()

# Ejecutar la ventana de Tkinter
root.mainloop()

# Nota: El DataFrame filtrado se guarda en D:/filtered_data.csv
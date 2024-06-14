# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 20:12:43 2023

@author: yaboniav
"""

import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import os

# Carga de DataFrames desde los archivos CSV
data_tensiones_base = pd.read_csv("D:\\archivos txt Diagnostico - base\\Data_tensiones_base.csv", decimal=".", sep=";")
data_tensiones = pd.read_csv("D:\\archivos txt Diagnostico\\Data_tensiones.csv", decimal=".", sep=";")
data_corrientes_base = pd.read_csv("D:\\archivos txt Diagnostico - base\\Data_I_kA_base.csv", decimal=".", sep=";")
data_corrientes = pd.read_csv("D:\\archivos txt Diagnostico\\Data_I_kA.csv", decimal=".", sep=";")
data_corrientes_base.rename(columns={'I_nom [kA]': 'I_nom'}, inplace=True)
data_corrientes.rename(columns={'I_nom [kA]': 'I_nom'}, inplace=True)
data_corrientes.drop(columns=['long [km]'], inplace=True)
data_corrientes_base.drop(columns=['long [km]'], inplace=True)
data_CT = pd.read_csv("D:\\archivos txt Diagnostico - base\\corrientes CTs.csv", decimal=".", sep=";")
# =============================================================================
# # Variables globales para almacenar las selecciones
# =============================================================================
feeder_1 = None
feeder_2 = None

# =============================================================================
# MENU DESPLEGABLE
# =============================================================================

# Supongamos que ya has cargado tus DataFrames
# data_tensiones = pd.read_csv(tu_ruta_de_archivo)

# Función para manejar la selección y actualizar las variables globales
def seleccionar():
    global feeder_1, feeder_2

    feeder_1 = seleccion_feeder1.get()
    feeder_2 = seleccion_feeder2.get()
    print("Feeder 1 seleccionado:", feeder_1)
    print("Feeder 2 seleccionado:", feeder_2)

    root.destroy()

# Configuración inicial de Tkinter
root = tk.Tk()
root.title("Selección de Feeder")
root.geometry('300x200')  # Tamaño de la ventana

# Agregar etiquetas y separaciones para mejorar la interfaz
tk.Label(root, text="Seleccione el primer Feeder:").pack(pady=5)
seleccion_feeder1 = tk.StringVar()
feeder_dropdown1 = ttk.Combobox(root, textvariable=seleccion_feeder1, values=sorted(data_tensiones_base['Feeder'].unique()))
feeder_dropdown1.pack(pady=5)

tk.Label(root, text="Seleccione el segundo Feeder:").pack(pady=5)
seleccion_feeder2 = tk.StringVar()
feeder_dropdown2 = ttk.Combobox(root, textvariable=seleccion_feeder2, values=sorted(data_tensiones_base['Feeder'].unique()))
feeder_dropdown2.pack(pady=5)

# Botón para confirmar la selección
boton_seleccionar = tk.Button(root, text="Seleccionar y Cerrar", command=seleccionar)
boton_seleccionar.pack(pady=10)

# Iniciar la interfaz de Tkinter
root.mainloop()

# =============================================================================
# Crear copias de los DataFrames
# =============================================================================
base = data_tensiones_base.copy()
enlace = data_tensiones.copy()
base_I = data_corrientes_base.copy()
enlace_I = data_corrientes.copy()

# =============================================================================
# Filtrar los DataFrames con las selecciones de Feeder
# =============================================================================

base = base[base['Feeder'].isin([feeder_1, feeder_2])]
enlace = enlace[enlace['Feeder'].isin([feeder_1, feeder_2])]
base_I = base_I[base_I['Feeder'].isin([feeder_1, feeder_2])]
enlace_I = enlace_I[enlace_I['Feeder'].isin([feeder_1, feeder_2])]

# =============================================================================
# =============================================================================
# #  ******************* TENSIONES *******************************
# =============================================================================
# =============================================================================

# =============================================================================
# Eliminar filas donde la columna "Phases" sea 1 o 2 en ambos DataFrames
# =============================================================================
base = base[base["Phases"] > 2]
enlace = enlace[enlace["Phases"] > 2]

# =============================================================================
# Reemplazar valores en la columna 'k_nom' menores a 30 por 13.2 en ambos 
# DataFrames
# =============================================================================
base.loc[base['k_nom'] < 30, 'k_nom'] = 13.2
enlace.loc[enlace['k_nom'] < 30, 'k_nom'] = 13.2

# =============================================================================
# CREAR DATA FRAMES DE MINIMO
# =============================================================================

# Identificar columnas que contienen '[kV]' en su nombre
columnas_kv_base = [col for col in base.columns if '[kV]' in col]
columnas_kv_enlace = [col for col in enlace.columns if '[kV]' in col]

# Calcular el valor mínimo de estas columnas por fila
base['Min [kV]'] = base[columnas_kv_base].min(axis=1)
enlace['Min [kV]'] = enlace[columnas_kv_enlace].min(axis=1)

# Crear los nuevos DataFrames min_base y min_enlace
min_base = base.copy()
min_enlace = enlace.copy()

# =============================================================================
# ENCONTRAR EL MINIMO
# =============================================================================
# Encontrar el índice de la fila con el valor mínimo en 'Min [kV]' para cada 'Feeder' en min_base
idx_min_base = min_base.groupby('Feeder')['Min [kV]'].idxmin()

# Filtrar min_base para conservar solo las filas con el valor mínimo en 'Min [kV]' por 'Feeder'
min_base = min_base.loc[idx_min_base]

# Realizar la misma operación para min_enlace
idx_min_enlace = min_enlace.groupby('Feeder')['Min [kV]'].idxmin()
min_enlace = min_enlace.loc[idx_min_enlace]

# =============================================================================
# DEJANDO EN VALORES EN P.U
# =============================================================================
# Eliminar la columna 'Min [kV]' de ambos DataFrames
min_base.drop(columns=['Min [kV]'], inplace=True)
min_enlace.drop(columns=['Min [kV]'], inplace=True)

# Dividir todos los campos numéricos por la columna 'k_nom' en min_base
columnas_numericas = min_base.select_dtypes(include=['number']).columns
min_base[columnas_numericas] = min_base[columnas_numericas].div(min_base['k_nom'], axis=0)

# Realizar la misma operación para min_enlace
columnas_numericas = min_enlace.select_dtypes(include=['number']).columns
min_enlace[columnas_numericas] = min_enlace[columnas_numericas].div(min_enlace['k_nom'], axis=0)

# Eliminar las columnas especificadas de ambos DataFrames
columnas_a_eliminar = ['Name_Nodo', 'Phases', 'k_nom', 'Energizado']

min_base.drop(columns=columnas_a_eliminar, errors='ignore', inplace=True)
min_enlace.drop(columns=columnas_a_eliminar, errors='ignore', inplace=True)

# Establecer 'Feeder' como índice y luego trasponer

min_base = min_base.set_index('Feeder').T
min_enlace = min_enlace.set_index('Feeder').T

# Eliminar la fila 'Feeder' si existe después de la trasposición

min_base.drop(index='Feeder', errors='ignore', inplace=True)
min_enlace.drop(index='Feeder', errors='ignore', inplace=True)
min_base.index = np.arange(0, 24)
min_enlace.index = np.arange(0, 24)

# =============================================================================
# GRAFICAS
# =============================================================================

# Encuentra las columnas coincidentes entre los dos DataFrames
columnas_comunes = min_base.columns.intersection(min_enlace.columns)
np.random.seed(0)  # Semilla para reproducibilidad
horas = np.arange(0, 24)
# Itera sobre cada columna común y crea una gráfica para ella
for columna in columnas_comunes:
    plt.figure(figsize=(13, 7), dpi=500)  # Ajustar el tamaño de la figura según sea necesario y la calidad de la imagen
    plt.plot(min_base.index, min_base[columna], marker='o', color='blue', label=f'{columna} base')
    plt.plot(min_enlace.index, min_enlace[columna], marker='o', color='green', label=f'{columna} enlace')
    
    # Añadir las líneas horizontales de referencia
    plt.axhline(0.9, color='orange', linestyle='--', label='Min (0.9)')
    plt.axhline(1.1, color='red', linestyle='--', label='Max (1.1)')
    
    # Añadir título y etiquetas
    plt.title(f'Tensión mínima alimentador: {columna}',fontsize=20, pad=20)
    plt.xlabel('Hora',fontsize=14)
    plt.ylabel('Tensión P.U.',fontsize=14)
    
    # Definir límites y marcaciones del eje x
    plt.xlim(0, 23)
    plt.xticks(horas)  # Asegurar que las marcas del eje x sean de 0 a 23
    plt.grid(True)  # Añadir una cuadrícula para mayor claridad
    # Mostrar leyenda
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4,fontsize=14)
    
    #guardar la gráfica
    title = 'Tensión mínima ' + columna
    file_path = f"D:\\archivos txt Diagnostico\\Graficas\\{title}.png"
    # Asegurarse de que el directorio existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    plt.savefig(file_path, bbox_inches='tight')
    
    # Mostrar la gráfica
     
    plt.show()
    
# =============================================================================
# 
# =============================================================================
#   CORRIENTES
# =============================================================================
# 
# =============================================================================

# =============================================================================
# CREAR DATA FRAMES DE MAXIMO
# =============================================================================

# Identificar columnas que contienen '[kA]' en su nombre
columnas_kA_base = [col for col in base_I.columns if '[kA]' in col]
columnas_kA_enlace = [col for col in enlace_I.columns if '[kA]' in col]

# Calcular el valor máximo de estas columnas por fila
base_I['Max [kA]'] = base_I[columnas_kA_base].max(axis=1)
enlace_I['Max [kA]'] = enlace_I[columnas_kA_enlace].max(axis=1)

# Crear los nuevos DataFrames max_base y max_enlace
max_base_I = base_I.copy()
max_enlace_I = enlace_I.copy()

# =============================================================================
# ENCONTRAR EL MAXIMO
# =============================================================================
# Encontrar el índice de la fila con el valor mínimo en 'Max [kA]' para cada 'Feeder' en min_base
idx_max_base_I = max_base_I.groupby('Feeder')['Max [kA]'].idxmax()

# Filtrar min_base para conservar solo las filas con el valor mínimo en 'Max [kA]' por 'Feeder'
max_base_I = max_base_I.loc[idx_max_base_I]

# Realizar la misma operación para min_enlace
idx_max_enlace_I = max_enlace_I.groupby('Feeder')['Max [kA]'].idxmax()
max_enlace_I = max_enlace_I.loc[idx_max_enlace_I]

# =============================================================================
# DEJANDO EN VALORES EN P.U
# =============================================================================
#Tomar dato de la sección de línea con mayor tensión

Seccion_linea = max_enlace_I[['Feeder', 'Name_line', 'Calibre','I_nom','Max [kA]']]
for feeder in Seccion_linea['Feeder']:
    if feeder in data_CT.columns:
        Seccion_linea[feeder] = data_CT.at[0, feeder]
# Eliminar la columna 'Max [kA]' de ambos DataFrames

max_base_I.drop(columns=['Max [kA]'], inplace=True)
max_enlace_I.drop(columns=['Max [kA]'], inplace=True)

# Creación de data frame de corrientes nominales

I_nom = max_enlace_I[['Feeder', 'I_nom']]
I_nom = I_nom.set_index('Feeder').T
I_nom = pd.concat([I_nom]*24, ignore_index= True)

# Eliminar las columnas especificadas de ambos DataFrames
columnas_a_eliminar = ['Name_line','long [km]', 'I_nom', 'Calibre']

max_base_I.drop(columns=columnas_a_eliminar, errors='ignore', inplace=True)
max_enlace_I.drop(columns=columnas_a_eliminar, errors='ignore', inplace=True)

# Establecer 'Feeder' como índice y luego trasponer

max_base_I = max_base_I.set_index('Feeder').T
max_enlace_I = max_enlace_I.set_index('Feeder').T

# Eliminar la fila 'Feeder' si existe después de la trasposición

max_base_I.drop(index='Feeder', errors='ignore', inplace=True)
max_enlace_I.drop(index='Feeder', errors='ignore', inplace=True)
max_base_I.index = np.arange(0, 24)
max_enlace_I.index = np.arange(0, 24)

# =============================================================================
# GRAFICAS DE CORRIENTE SIN I_NOM Y VALOR DE CORRIENTE DEL CT
# =============================================================================

# Encuentra las columnas coincidentes entre los dos DataFrames
columnas_comunes = max_base_I.columns.intersection(max_enlace_I.columns)
np.random.seed(0)  # Semilla para reproducibilidad
horas = np.arange(0, 24)
# Itera sobre cada columna común y crea una gráfica para ella
for columna in columnas_comunes:
    plt.figure(figsize=(13, 7), dpi=500)  # Ajustar el tamaño de la figura según sea necesario y la calidad de la imagen
    plt.plot(max_base_I.index, max_base_I[columna], marker='o', color='blue', label=f'{columna} base*')
    plt.plot(max_enlace_I.index, max_enlace_I[columna], marker='o', color='green', label=f'{columna} enlace*')
        
    # Añadir título y etiquetas
    plt.title(f'Corriente máxima alimentador: {columna}',fontsize=20, pad=20)
    plt.xlabel('Hora',fontsize=14)
    plt.ylabel('Corriente [kA]',fontsize=14)
    
    # Definir límites y marcaciones del eje x
    plt.xlim(0, 23)
    plt.xticks(horas)  # Asegurar que las marcas del eje x sean de 0 a 23
    
    # Mostrar leyenda
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4,fontsize=14)
    plt.grid(True)  # Añadir una cuadrícula para mayor claridad
  
    #guardar la gráfica
    title = 'Corriente máxima_ ' + columna
    file_path = f"D:\\archivos txt Diagnostico\\Graficas\\{title}.png"
    # Asegurarse de que el directorio existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    plt.savefig(file_path, bbox_inches='tight')
    
    # Mostrar la gráfica
    
    plt.show()
    
# =============================================================================
# GRAFICAS DE CORRIENTE CON I_NOM Y VALOR DE CORRIENTE DEL CT
# =============================================================================

# Encuentra las columnas coincidentes entre los dos DataFrames
columnas_comunes = max_base_I.columns.intersection(max_enlace_I.columns)
np.random.seed(0)  # Semilla para reproducibilidad
horas = np.arange(0, 24)
# Itera sobre cada columna común y crea una gráfica para ella
for columna in columnas_comunes:
    plt.figure(figsize=(13, 7), dpi=500)  # Ajustar el tamaño de la figura según sea necesario y la calidad de la imagen
    plt.plot(max_base_I.index, max_base_I[columna], marker='o', color='blue', label=f'{columna} base')
    plt.plot(max_enlace_I.index, max_enlace_I[columna], marker='o', color='green', label=f'{columna} enlace')
    plt.plot(I_nom.index, I_nom[columna], marker='o', color='orange', linestyle='--', label=f'{columna} I_Nom')
    plt.plot(data_CT.index, data_CT[columna], marker='o', color='red', linestyle='--', label=f'{columna} CT')

    
    # Añadir título y etiquetas
    plt.title(f'Corriente máxima alimentador: {columna}',fontsize=20, pad=20)
    plt.xlabel('Hora',fontsize=14)
    plt.ylabel('Corriente [kA]',fontsize=14)
    
    # Definir límites y marcaciones del eje x
    plt.xlim(0, 23)
    plt.xticks(horas)  # Asegurar que las marcas del eje x sean de 0 a 23
    
    # Mostrar leyenda
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4,fontsize=14)
    plt.grid(True)  # Añadir una cuadrícula para mayor claridad
  
    #guardar la gráfica
    title = 'Corriente máxima ' + columna
    
    file_path = f"D:\\archivos txt Diagnostico\\Graficas\\{title}.png"
    print (file_path)
    # Asegurarse de que el directorio existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    plt.savefig(file_path, bbox_inches='tight')
    
    # Mostrar la gráfica
    
    plt.show()
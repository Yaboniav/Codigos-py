# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:19:48 2023

@author: yaboniav
"""

import pandas as pd
import os

# Establecer el directorio donde se encuentran los archivos CSV
path = 'D://OneDrive - Grupo EPM//2. PLANEACION OPTIMA//BD_CALIDA//3. Calidad//2021'

# Lista para almacenar los DataFrames de cada archivo
all_dfs = []

for filename in os.listdir(path):
    # Verificar que el archivo es CSV
    if filename.endswith('.csv'):
        file_path = os.path.join(path, filename)
        
        try:
            # Leer el archivo CSV (usando ; como separador y especificando la codificación)
            df = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1')
            
            # Eliminar las columnas especificadas si existen en el DataFrame
            cols_to_remove = ["USUARIOS", 
                              "FECHA AÑO",
                              "kVA TRAFO",
                              "POBLACION.1",
                              "FECHA MES",
                              "FECHA AÑO",
                              "CLASIFICACION_PODA",
                              "XPOS_BREAKER",
                              "YPOS_BREAKER",
                              "LONGITUD_BREAKER",
                              "LATITUD_BREAKER",
                              "CAUSA_SSPD_DETALLADA"
                              ]
            df = df.drop(columns=[col for col in cols_to_remove if col in df.columns])
            
            all_dfs.append(df)
            # Imprimir mensaje de éxito
            print(f"El archivo {filename} fue cargado exitosamente!")
        
        except Exception as e:
            # Imprimir mensaje de error si hay problemas al cargar el archivo
            print(f"Error al cargar el archivo {filename}. Detalle del error: {e}")

# Concatenar todos los DataFrames en uno solo
final_df = pd.concat(all_dfs, ignore_index=True)

# Guardar el DataFrame final en un archivo CSV con punto y coma como separador
csv_filename = "D://OneDrive - Grupo EPM//2. PLANEACION OPTIMA//BD_CALIDA//1. recopilación calidad//2021.csv"
final_df.to_csv(csv_filename, sep=';', index=False)
print(f"¡El DataFrame se ha guardado exitosamente en {csv_filename}!")
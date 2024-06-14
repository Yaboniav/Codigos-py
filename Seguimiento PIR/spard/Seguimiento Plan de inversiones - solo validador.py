# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:30:17 2023

@author: yaboniav
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import os
#import seaborn as plt
#from IPython.display import display
#from IPython.core.pylabtools import figsize, getfigs

#from pylab import *
#from numpy import *


#----------------Seleccionar equipo de trabajo para cargue de info-----------#

from menu_solo_validador import seleccionar_opcion_desde_menu

if __name__ == "__main__":
    equipo_trabajo = seleccionar_opcion_desde_menu()
    print(f"La opción seleccionada fue: {equipo_trabajo}")
    # Ahora puedes usar la variable opcion_final como desees.
  
#--------------Creación de data frame con todos los campos ------------------# 

global_data = pd.read_csv('D:/validador/campos a reportar.csv',sep=';',decimal='.')

plantilla = global_data.copy()
plantilla = plantilla[['Nombre del Campo']]
plantilla = plantilla.transpose()
plantilla.set_axis(plantilla.iloc[0], axis='columns', inplace=True)
plantilla = plantilla[1:]

cols_to_convert = [
    'Capacidad', 'INVR Cop', 'INVR Mill', "Descripción UC's",
    'Categoria', 'BRAR', 'CR_rep', 'CRA_rep', 'AR', 'k', 'ActivoReconocido', 'Altitud',
    'Área', 'Área especial', 'AreaReconocida', 'FactorSecundario', 'FactorTerciario',
    'Latitud', 'Longitud', 'Nivel alta', 'Nivel baja 1', 'Nivel baja 2', 'Nivel baja 3',
    'Potencia baja 1', 'Potencia baja 2', 'Potencia baja 3', 'Valor catastral', 'CR',
    'PU', 'FU', 'Psn', 'Valor Regulatorio Aprobado', 'Relación Beneficio Costo',
    'Valor de Ejecución Real del Proyecto ($)', 'Valor de Ejecución Regulatorio',
    'BRAEN_RP', 'INVTR_RP', 'IREC_RP', 'BRAFO', 'RCBIAFO', 'RCNAFO', 'BRT', 'Capacidad_rep'
]

# Convertir las columnas a tipo float
for col in cols_to_convert:
    if col in plantilla.columns:
        plantilla[col] = plantilla[col].astype(float)
    else:
        print(f"La columna '{col}' no se encuentra en el DataFrame 'plantilla'.")
#-----------------------------------------------------------------------------#

#--------------lectura de archivos de gestión de la información---------------#

from creador_data_frame_por_equipos import read_excel_from_directory

if __name__ == "__main__":
    #Crear en el disco D una carpeta llamada validador
    folder_path = (f"D:/validador/{equipo_trabajo}")
    plantilla_equipo = read_excel_from_directory(folder_path)

#------------------------VALIDADOR DE LAS PLANTILLAS--------------------------#

from script_validador_GIT import validador

if __name__ == "__main__":
    # Llamar a la función con el DataFrame creado
    df_corregido, df_resultados = validador(plantilla_equipo)
    # Guardar el DataFrame de errores en un archivo Excel
    df_resultados = df_resultados[df_resultados["Descripción del Error"] != "Sin errores"]
    nombre_archivo = f"{equipo_trabajo} errores.xlsx"
    ruta_errores = "D:/validador/errores plantillas seguimiento/"
    ruta_completa = ruta_errores + nombre_archivo
    df_resultados.to_excel(ruta_completa, index=False)

# Identifica las columnas que están en df_corregido pero no en plantilla
missing_columns = [col for col in df_corregido.columns if col not in plantilla.columns]

# Imprime la cantidad y los nombres de las columnas faltantes
num_missing_columns = len(missing_columns)
print(f"El DataFrame 'df_corregido' tiene {num_missing_columns} columnas que no están en 'plantilla'.")
print("Las columnas son:", ', '.join(missing_columns))

# Identifica las columnas que están en plantilla pero no en df_corregido
columns_not_in_df_corregido = [col for col in plantilla.columns if col not in df_corregido.columns]

# Columnas compartidas entre ambos DataFrames
shared_columns = [col for col in df_corregido.columns if col in plantilla.columns]


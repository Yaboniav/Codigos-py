# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 20:01:43 2023

@author: yaboniav
"""

import pandas as pd
import os


# Establecer el directorio donde se encuentran los archivos CSV
path = 'D://OneDrive - Grupo EPM//2. PLANEACION OPTIMA//BD_CALIDA//1. recopilación calidad'

# Diccionario para almacenar los títulos de las columnas de cada archivo
column_titles = {}

# Recorrer cada archivo en el directorio
for filename in os.listdir(path):
    if filename.endswith('.csv'):
        file_path = os.path.join(path, filename)

        # Leer solo los encabezados (primer fila) del archivo CSV
        df = pd.read_csv(file_path, nrows=0, sep=';', encoding='ISO-8859-1')
        column_titles[filename] = set(df.columns)

# Asegúrate de que haya al menos dos archivos para comparar
if len(column_titles) < 2:
    print("No hay suficientes archivos para comparar.")
    exit()

# Tomar los nombres de los dos primeros archivos
first_file, second_file = list(column_titles.keys())[:2]
first_titles = column_titles[first_file]
second_titles = column_titles[second_file]

# Identificar las columnas que están en el primero pero no en el segundo
diff_first_vs_second = first_titles - second_titles

# Comparar los títulos de las columnas de todos los archivos
differences = {}

for filename, titles in column_titles.items():
    # Todos los otros archivos excepto el actual
    other_titles = set().union(*(s for k, s in column_titles.items() if k != filename))

    # Diferencia entre el conjunto de títulos del archivo actual y todos los otros
    diff = titles.symmetric_difference(other_titles)
    if diff:
        differences[filename] = ', '.join(diff)

# Crear un DataFrame con las diferencias
diff_df = pd.DataFrame(list(differences.items()), columns=['Filename', 'Differences'])

# Agregar una columna con las diferencias específicas del primero contra el segundo
diff_df['Diff First vs Second'] = ''
diff_df.loc[diff_df['Filename'] == first_file, 'Diff First vs Second'] = ', '.join(diff_first_vs_second)

print(diff_df)

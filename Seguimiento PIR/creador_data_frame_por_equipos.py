# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 18:18:57 2023

@author: yaboniav
"""

import os
import pandas as pd

def read_excel_from_directory(folder_path):
    """
    Lee todos los archivos Excel (.xlsx y .xlsm) en un directorio especificado y los concatena en un único DataFrame.

    :param folder_path: Ruta del directorio donde están los archivos Excel.
    :return: DataFrame concatenado con todos los datos.
    """

    all_dataframes = []

    # Definir columnas para convertir a string
    columns_to_str = {
        'IUL': str, 
        'IUS': str, 
        'IUA': str, 
        'IUA remplazado': str, 
        'IUA Transformador': str,
        'IUL Línea': str, 
        'IUS final': str,
        'IUS inicial': str,
        'IUA ajustado': str, 
        'IUA elemento': str
    }

    # Iterar sobre todos los archivos en el directorio especificado
    for filename in os.listdir(folder_path):
        if filename.endswith(('.xlsm', '.xlsx','xls')):  # Asegurar que es un archivo Excel
            file_path = os.path.join(folder_path, filename)
            try:
                # Leer todas las hojas del archivo Excel especificando dtypes
                xlsx = pd.read_excel(file_path, engine='openpyxl', sheet_name=None, dtype=columns_to_str)

                # Obtener el nombre del archivo sin la extensión
                filename_without_extension = os.path.splitext(filename)[0]

                # Iterar sobre cada hoja y agregar su contenido a la lista
                for sheet_name, df in xlsx.items():
                    if sheet_name != "Listas":  # Excluir hoja específica
                        # Añadir columnas con el nombre del archivo (sin extensión) y el nombre de la hoja
                        df['Nombre de la Plantilla 2'] = filename_without_extension
                        df['Hoja archivo'] = sheet_name

                        # Añadir número de fila de cada hoja del archivo Excel
                        df['Número de Fila'] = df.index + 2
                        
                        # Asegurarse de que la columna "Nivel de Tensión" sea de tipo entero
                        df['Nivel'] = df['Nivel'].apply(lambda x: x if isinstance(x, int) else 9999)

                        # Asegurarse de que la columna "Fracción costo" sea de tipo decimal
                        df['Nivel'] = df['Nivel'].apply(lambda x: x if isinstance(x, int) else 9999)                        
                        all_dataframes.append(df)
                print(f"Archivo leído con éxito: {filename}")
            except Exception as e:
                print(f"Error al leer el archivo {filename}: {e}")

    # Concatenar todos los DataFrames en uno solo
    final_dataframe = pd.concat(all_dataframes, ignore_index=True)

    return final_dataframe
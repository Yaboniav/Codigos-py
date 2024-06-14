# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 14:03:51 2023

@author: yaboniav
"""

import pandas as pd
import simplekml

def excel_to_kml(excel_path, kml_path):
    # Leer el archivo Excel
    df = pd.read_excel(excel_path, engine='openpyxl')
    
    # Crear un nuevo KML
    kml = simplekml.Kml()

    # Suponiendo que las columnas de tu Excel se llaman 'Latitud' y 'Longitud'
    # Recorre cada fila y añade las coordenadas al KML
    for index, row in df.iterrows():
        kml.newpoint(name=str(index), coords=[(row['Longitud'], row['Latitud'])])

    # Guardar el KML
    kml.save(kml_path)


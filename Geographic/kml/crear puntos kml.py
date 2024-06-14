# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 14:05:47 2023

@author: yaboniav
"""
import pandas as pd
import simplekml

# Leer el archivo Excel
ruta_excel = "D://reconectadores a instalar - 1.xlsx"
df = pd.read_excel(ruta_excel, engine='openpyxl')

# Crear el objeto KML
kml = simplekml.Kml()

#Iterar a través de la categorias para crear carpetas regional

# Iterar a través de las regionales únicas para crear carpetas de regional
for regional in df['Regional'].unique():
    regional_df = df[df['Regional'] == regional]
    regional_folder = kml.newfolder(name=regional)
    
    # Iterar a través de los alimentadores únicos dentro de cada regional
    for alimentador in regional_df['Alimentador A'].unique():
        alimentador_df = regional_df[regional_df['Alimentador A'] == alimentador]
        alimentador_folder = regional_folder.newfolder(name=alimentador)
        
        # Crear puntos dentro de las carpetas de alimentador
        for _, row in alimentador_df.iterrows():
            pnt = alimentador_folder.newpoint(name=row['Código'])
            pnt.coords = [(row['Longitud'], row['Latitud'])]
            pnt.description = (f"Proyecto: {row['Categoría']}\n"
                               f"Regional: {row['Regional']}\n"
                               f"Alimentador: {row['Alimentador A']}\n"
                               f"Detalle: {row['Enlaces Alimentadores A - B']}")

# Guardar el archivo KML
kml.save("D://recos priorizados-1.kml")
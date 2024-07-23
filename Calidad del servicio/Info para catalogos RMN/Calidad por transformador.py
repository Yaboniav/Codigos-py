# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:00:04 2024

@author: yaboniav
"""

import pandas as pd
import os
import numpy as np

# Definir los nombres de las columnas para el DataFrame
columnas_deseadas = [
    'FDD_DURACION', 'FDD_CODIGOELEMENTO', 'USUARIOS_TAFO', 'FDD_UIXTI', 'UI_MES',
    'FPARENT', 'DESCRIPCION_CAUSA_CREG', 'FDD_CAUSA_SSPD', 'NOMBRE DEL LIBRO', 'AÑO', 'NOMBRE_MES'
]

# Crear un DataFrame vacío con las columnas especificadas
df_calidad = pd.DataFrame(columns=columnas_deseadas)

# Ruta donde se encuentran los archivos CSV
ruta_csv = 'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//3. Calidad del servicio//2. compilado Calidad'

# Listar todos los archivos en la carpeta que terminan en .csv
archivos_csv = [archivo for archivo in os.listdir(ruta_csv) if archivo.endswith('.csv')]

# Cargar los datos de cada archivo CSV y concatenar solo las columnas relevantes
for archivo in archivos_csv:
    ruta_completa = os.path.join(ruta_csv, archivo)
    try:
        # Cargar el archivo CSV usando un delimitador específico y manejando comillas
        df_temp = pd.read_csv(ruta_completa, delimiter=';', low_memory=False)
        # Seleccionar solo las columnas que nos interesan, si están disponibles
        df_temp = df_temp.loc[:, df_temp.columns.isin(columnas_deseadas)]
        df_calidad = pd.concat([df_calidad, df_temp], ignore_index=True)
    except Exception as e:
        print(f"Error al procesar el archivo {archivo}: {e}")

# LIMPIEZA DE DATOS
df_calidad['FPARENT'] = df_calidad['FPARENT'].replace(to_replace=r'.*EL_TARRA.*', value='TARC1', regex=True)
df_calidad['FPARENT'] = df_calidad['FPARENT'].replace(to_replace=r'.*ORU.*', value='ORUC1', regex=True)
df_calidad['FPARENT'] = df_calidad['FPARENT'].replace(to_replace=r'.*TIBPUEBLOS.*', value='TIBTIBU3', regex=True)
df_calidad = df_calidad[df_calidad['FPARENT'] != 'ECO']
df_calidad = df_calidad[df_calidad['FPARENT'] != 'BUTCSAUX']
df_calidad = df_calidad[df_calidad['FPARENT'] != 'SANOL25']
df_calidad = df_calidad[df_calidad['FPARENT'] != 'SANOL45']
df_calidad = df_calidad[df_calidad['FPARENT'] != 'TIBECP']
df_calidad = df_calidad[df_calidad['FPARENT'] != 'BELC38']
df_calidad = df_calidad[df_calidad['FPARENT'] != 'INSC77']
df_calidad = df_calidad[df_calidad['FPARENT'] != 'TOLPALERMO']

# PROCESAMIENTO DE DATOS
causas_permitidas = [
    
   'Falla en transformador de distribución o sus elementos asociados.',
    
]

df_alimentador = df_calidad[df_calidad['DESCRIPCION_CAUSA_CREG'].isin(causas_permitidas)]
df_alimentador = df_alimentador[['FDD_CODIGOELEMENTO', 'FDD_UIXTI', 'UI_MES', 'AÑO', "FDD_CAUSA_SSPD"]]

# Eliminar filas donde 'FDD_CAUSA_SSPD' es diferente de "0"
df_alimentador = df_alimentador[df_alimentador['FDD_CAUSA_SSPD'] == 0]

# Eliminar la columna 'FDD_CAUSA_SSPD'
df_alimentador = df_alimentador.drop(columns=['FDD_CAUSA_SSPD'])

# Convertimos la columna 'AÑO' a cadena para facilitar la creación de las nuevas columnas
df_alimentador['AÑO'] = df_alimentador['AÑO'].astype(str)

# Agrupamos por 'FPARENT' y 'AÑO' y sumamos los valores
df_agrupado = df_alimentador.groupby(['FDD_CODIGOELEMENTO', 'AÑO']).agg({
    'UI_MES': 'sum',
    'FDD_UIXTI': 'sum'
}).reset_index()

# Creamos un DataFrame pivotado para tener años como columnas y sumas correspondientes
pivot_ui_mes = df_agrupado.pivot_table(values='UI_MES', index='FDD_CODIGOELEMENTO', columns='AÑO', aggfunc='sum').fillna(0)
pivot_fdd_uixti = df_agrupado.pivot_table(values='FDD_UIXTI', index='FDD_CODIGOELEMENTO', columns='AÑO', aggfunc='sum').fillna(0)

# Renombrar las columnas para reflejar el contenido correctamente
pivot_ui_mes.columns = [f'Suma de UI_MES {col}' for col in pivot_ui_mes.columns]
pivot_fdd_uixti.columns = [f'Suma de FDD_UIXTI {col}' for col in pivot_fdd_uixti.columns]

# Unimos los dos dataframes pivotados
df_final = pd.concat([pivot_ui_mes, pivot_fdd_uixti], axis=1)

# Reordenamos las columnas en el orden deseado, asegurándonos de que todas las columnas existan
columnas_ordenadas = []
for año in sorted(set(df_agrupado['AÑO'])):  # Nos aseguramos de que el conjunto de años esté ordenado
    columnas_ordenadas.extend([f'Suma de UI_MES {año}', f'Suma de FDD_UIXTI {año}'])

df_final = df_final[columnas_ordenadas]

#******************************************************************************
# Ruta al archivo de Excel y al archivo CSV
ruta_excel = 'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//3. Calidad del servicio//información de transformadores 2019 - 2023.xlsx'
ruta_csv = 'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//3. Calidad del servicio//datos.csv'

# Cargar el archivo Excel en un DataFrame
df_info_alimentadores = pd.read_excel(ruta_excel)

# Seleccionamos solo las columnas necesarias (esto asume que las columnas se llaman exactamente así en el archivo)
columnas_info = ['CODE', 'usuarios']
df_info_seleccionado = df_info_alimentadores[columnas_info]

#*******************************************************************************

# Suponemos que df_final ya está definido y cargado con datos relevantes
# Aquí deberías cargar o definir df_final según tus datos existentes, como un ejemplo:
# df_final = pd.read_csv(ruta_csv)

# Realizamos el merge con el DataFrame final (df_final) basándonos en 'FPARENT' y 'Código'
df_final_con_clientes = pd.merge(df_final, df_info_seleccionado, left_on='FDD_CODIGOELEMENTO', right_on='CODE', how='left')

# Eliminar la columna 'Código' ya que es redundante con 'FPARENT'
#df_final_con_clientes.drop('Código', axis=1, inplace=True)

# Realiza los cálculos de SAIFI y SAIDI por cada año
for año in range(2019, 2024):
    # Preparamos los nombres de las columnas para cada año
    ui_mes_column = f'Suma de UI_MES {año}'
    fdd_uixti_column = f'Suma de FDD_UIXTI {año}'
    clientes_column = f'usuarios'

    # Inicializamos las nuevas columnas SAIFI y SAIDI para el año con ceros
    df_final_con_clientes[f'SAIFI {año}'] = 0
    df_final_con_clientes[f'SAIDI {año}'] = 0

    # Verificamos si hay clientes antes de dividir para evitar divisiones por cero
    # y calcular los índices SAIFI y SAIDI de manera vectorizada
    mask = df_final_con_clientes[clientes_column] > 0  # Máscara para verificar donde hay clientes
    df_final_con_clientes.loc[mask, f'SAIFI {año}'] = df_final_con_clientes.loc[mask, ui_mes_column] / df_final_con_clientes.loc[mask, clientes_column]
    df_final_con_clientes.loc[mask, f'SAIDI {año}'] = df_final_con_clientes.loc[mask, fdd_uixti_column] / df_final_con_clientes.loc[mask, clientes_column]

# Aseguramos que 'Código' es la primera columna
# Creamos una lista de columnas donde 'Código' esté al principio
columnas = ['CODE'] + [col for col in df_final_con_clientes.columns if col != 'CODE']

# Reordenamos el DataFrame según esta nueva lista de columnas
df_final_con_clientes = df_final_con_clientes[columnas]
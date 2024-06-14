# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:52:04 2024
r"D:\OneDrive - Grupo EPM\1. PLANEACIÓN DE INFRAESTRUCTURA\06_Proyecciones Financieras\PROYECCIONES 2024-2043 - PIE 2025-2028\5_Unidades Constructivas\Análisis adicionales\Exp & Rep\ESTIMACIÓN UUCC PIR 2025- 2026.xlsx"
@author: yaboniav
"""

import pandas as pd

def leer_archivo_excel(ruta_archivo, nombre_hoja):
    """
    Lee un archivo de Excel y devuelve la hoja especificada como un DataFrame.
    
    Parámetros:
    ruta_archivo (str): Ruta del archivo de Excel.
    nombre_hoja (str): Nombre de la hoja a leer.
    
    Retorna:
    pd.DataFrame: DataFrame con los datos de la hoja especificada.
    """
    try:
        print(f"Leyendo archivo: {ruta_archivo}")
        print(f"Nombre de la hoja: {nombre_hoja}")
        df = pd.read_excel(ruta_archivo, sheet_name=nombre_hoja)
        print(f"Lectura exitosa de {nombre_hoja}")
        return df
    except FileNotFoundError:
        print(f"El archivo no se encontró: {ruta_archivo}")
        return None
    except ValueError as ve:
        print(f"Error en el valor al leer la hoja '{nombre_hoja}' en el archivo '{ruta_archivo}': {ve}")
        return None
    except Exception as e:
        print(f"Error inesperado al leer la hoja '{nombre_hoja}' desde '{ruta_archivo}': {e}")
        return None

def limpiar_datos(df):
    """
    Limpia el DataFrame eliminando filas y columnas innecesarias,
    manejando valores nulos y estandarizando formatos de datos.
    
    Parámetros:
    df (pd.DataFrame): DataFrame a limpiar.
    
    Retorna:
    pd.DataFrame: DataFrame limpio.
    """
    # Ejemplo de eliminación de columnas innecesarias
    # df = df.drop(columns=['ColumnaInnecesaria1', 'ColumnaInnecesaria2'])

    # Manejo de valores nulos
    df = df.dropna(how='all')  # Eliminar filas donde todos los elementos son NaN
    df = df.fillna(method='ffill')  # Rellenar NaNs usando el método forward fill

    # Estandarizar formatos de datos
    if 'ColumnaFecha' in df.columns:
        df['ColumnaFecha'] = pd.to_datetime(df['ColumnaFecha'], errors='coerce')
    
    return df

def procesar_archivos(ruta_archivo_1, nombre_hoja_1, ruta_archivo_2, nombre_hoja_2):
    """
    Procesa dos archivos de Excel y devuelve DataFrames limpios.
    
    Parámetros:
    ruta_archivo_1 (str): Ruta del primer archivo de Excel.
    nombre_hoja_1 (str): Nombre de la hoja del primer archivo.
    ruta_archivo_2 (str): Ruta del segundo archivo de Excel.
    nombre_hoja_2 (str): Nombre de la hoja del segundo archivo.
    
    Retorna:
    tuple: Dos DataFrames limpios.
    """
    df1 = leer_archivo_excel(ruta_archivo_1, nombre_hoja_1)
    df2 = leer_archivo_excel(ruta_archivo_2, nombre_hoja_2)
    
    if df1 is not None:
        df1 = limpiar_datos(df1)
    
    if df2 is not None:
        df2 = limpiar_datos(df2)
    
    return df1, df2

# Rutas de archivos y nombres de hojas actualizados
ruta_archivo_1 = r"D:\OneDrive - Grupo EPM\1. PLANEACIÓN DE INFRAESTRUCTURA\06_Proyecciones Financieras\PROYECCIONES 2024-2043 - PIE 2025-2028\5_Unidades Constructivas\Análisis adicionales\Exp & Rep\ESTIMACIÓN UUCC PIR 2025- 2026.xlsx"
nombre_hoja_1 = 'UCs 25 - 26'
ruta_archivo_2 = r"D:\OneDrive - Grupo EPM\3. CENS\0. PIE - PIR - PF\2. Insumos Exp - Rep\UC's Exp & Rep-calidad MT.xlsx"
nombre_hoja_2 = 'Obras Exp & Rep'

# Procesar los archivos
df_plan_25_26, df_plan_full_calidad = procesar_archivos(ruta_archivo_1, nombre_hoja_1, ruta_archivo_2, nombre_hoja_2)

# Mostrar los DataFrames limpios
if df_plan_25_26 is not None:
    print("Datos limpios del primer archivo (df_plan_25_26):")
    print(df_plan_25_26.head())
else:
    print("No se pudo leer o limpiar el primer archivo.")

if df_plan_full_calidad is not None:
    print("\nDatos limpios del segundo archivo (df_plan_full_calidad):")
    print(df_plan_full_calidad.head())
else:
    print("No se pudo leer o limpiar el segundo archivo.")

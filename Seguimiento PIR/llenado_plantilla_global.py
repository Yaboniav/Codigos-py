# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:29:51 2024

@author: yaboniav
"""

import pandas as pd
import tkinter as tk
import numpy as np
from tkinter import ttk
import datetime

# Función que muestra un menú desplegable para seleccionar el equipo ejecutor
def seleccionar_equipo_ejecutor():
    """Muestra un menú desplegable y permite al usuario seleccionar el equipo ejecutor."""

    opciones = [
        "Sub & Lín",
        "Exp & Rep",
        "Proy Pérdidas",
        "Mtto",
        "Unidad de Proyectos",
        "Comercial: Compra Bien Futuro",
        "Activos de Uso propiedad de Terceros",
        "Electrificación Rural",
        "Gestión de Activos",
        "UGO"
    ]

    # Crear una ventana
    root = tk.Tk()
    root.title("Seleccionar Equipo Ejecutor")

    # Añadir mensaje al usuario
    label = tk.Label(root, text="Cual es el equipo ejecutor:")
    label.pack(pady=20)

    # Crear y llenar el dropdown
    equipo_var = tk.StringVar()
    dropdown = ttk.Combobox(root, textvariable=equipo_var, values=opciones)
    dropdown.pack(pady=20)
    dropdown.set(opciones[0])  # Establecer la primera opción como predeterminada

    # Función para cerrar la ventana
    def on_ok():
        root.quit()  # Finalizar el mainloop
        root.destroy()

    # Botón de OK
    btn_ok = tk.Button(root, text="OK", command=on_ok)
    btn_ok.pack(pady=20)

    root.mainloop()  # Iniciar el bucle principal

    # Devolver el valor seleccionado
    return equipo_var.get()
# Función para diligenciar el campo de Subgerencia ejecutora
def mapear_subgerencia(equipo_ejecutor):
    """Toma el equipo ejecutor seleccionado y devuelve la subgerencia correspondiente."""
    
    mapeo_opciones = {
        "Sub & Lín": "Subgerencia de Subestaciones y Líneas",
        "Exp & Rep": "Subgerencia de Distribución",
        "Proy Pérdidas": "Subgerencia de Distribución",
        "Mtto": "Subgerencia de Distribución",
        "Comercial: Compra Bien Futuro": "Comercial T&D",
        "Unidad de Proyectos": "Unidad de Proyectos",
        "Gestión de Activos": "Unidad de gestión Operativa",
        "Unidad Gestión Operativa": "Unidad Gestión Operativa",
        "UGO": "Unidad de Gestión Operativa",
        "Activos de Uso propiedad de Terceros": "Activos de Uso propiedad de Terceros"
    }
    
    return mapeo_opciones.get(equipo_ejecutor, "")  # Devuelve un valor vacío si el equipo ejecutor no está en el mapeo.
"""
Función calculo de CR
"""
def calcular_CR(plantilla_df):
    # 1. Cargar el archivo Excel "UCs.xlsx"
    ucs_data = pd.read_excel("D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/3. inputs/1. información basica - redes - trafos - municipios/UCs.xlsx")

# Evitar agregar la columna 'Código UC' después del merge
    merged_data = plantilla_df.merge(
        ucs_data[['Código UC', 'Valor instalación [$ dic 2017]', 'Valor unitario [$ dic 2017/MVA]']], 
        left_on='Unidad Constructiva', 
        right_on='Código UC', 
        how='left'
    ).drop(columns='Código UC')  # Eliminar la columna 'Código UC'
    # Rellena los valores vacíos en 'capacidad' y 'capacidad_rep' con 0
    merged_data['Capacidad'].fillna(0, inplace=True)
    merged_data['Capacidad_rep'].fillna(0, inplace=True)
    merged_data['Valor1'] = merged_data['Cantidad'] * merged_data['Valor instalación [$ dic 2017]']
    merged_data['Valor2'] = merged_data['Capacidad'] * merged_data['Valor unitario [$ dic 2017/MVA]']

    # Si Valor1 o Valor2 no es un número (NaN), asignar 0
    merged_data['Valor1'] = np.where(np.isnan(merged_data['Valor1']), 0, merged_data['Valor1'])
    merged_data['Valor2'] = np.where(np.isnan(merged_data['Valor2']), 0, merged_data['Valor2'])
    
    merged_data['CR'] = merged_data['Valor1'] + merged_data['Valor2']

    # Ajustes para multiplicar por el número de conductores según las condiciones
    cond_n1 = (merged_data['Nivel'] == 1) & (merged_data['Hoja archivo'].isin(['Conductor_N1'])) & (merged_data['DESCRIPCION'].str.contains("km de conductor"))
    cond_n23 = (merged_data['Nivel'].isin([2, 3, 4])) & (merged_data['Hoja archivo'].isin(['Conductor_N2-N3'])) & (merged_data['DESCRIPCION'].str.contains("km de conductor"))

    merged_data.loc[cond_n1, 'CR'] *= merged_data.loc[cond_n1, 'Número de conductores']
    merged_data.loc[cond_n23, 'CR'] *= merged_data.loc[cond_n23, 'Número de conductores'] / 3

    # Las siguientes líneas no son necesarias ya que 'CR' ya es una columna de 'merged_data'
    # final_df = merged_data[plantilla_df.columns.tolist() + ['CR']]
    merged_data.drop(columns=['Valor1', 'Valor2', 'Valor instalación [$ dic 2017]', 'Valor unitario [$ dic 2017/MVA]'], inplace=True)
    
    return merged_data

"""
Función que copia los campos 'Fracción costo' y 'Porcentaje uso' en los campos 'FU' y 'PU' respectivamente.
"""
def copiar_FU_PU(plantilla_df):

    # Copiar el campo "Fracción costo" al campo "FU" y dividir por 100
    plantilla_df['FU'] = plantilla_df['Fracción costo']

    # Copiar el campo "Porcentaje uso" al campo "PU" y dividir por 100
    plantilla_df['PU'] = plantilla_df['Porcentaje uso']

    return plantilla_df

"""
función para diligenciar el factor FRT cobertura
"""

def llenar_FTR(plantilla_df):
    # Verificar la condición de que "PIEC" sea igual a 'S'
    condicion_PIEC = plantilla_df['PIEC'] == 'S'
    
    # Asignar 1.08 a "FTR" si "Nivel" es 1 o 2
    condicion_Nivel_1_2 = plantilla_df['Nivel'].isin([1, 2])
    plantilla_df.loc[condicion_PIEC & condicion_Nivel_1_2, 'FTR'] = 1.08
    
    # Asignar 1 a "FTR" si "Nivel" es 3 o 4
    condicion_Nivel_3_4 = plantilla_df['Nivel'].isin([3, 4])
    plantilla_df.loc[condicion_PIEC & condicion_Nivel_3_4, 'FTR'] = 1
    
    # Asignar 0 a "FTR" si "PIEC" es igual a 'N'
    condicion_PIEC_N = plantilla_df['PIEC'] == 'N'
    plantilla_df.loc[condicion_PIEC_N, 'FTR'] = 0

    return plantilla_df

"""
Función que permite cálcular el campo IREC (cobertura)
"""
def calcular_IREC(plantilla_df):
    # Inicializa la columna "IREC" con valores de 0
    plantilla_df['IREC'] = 0

    # 1. Verifica si "PIEC" es 'S'
    condicion_PIEC_S = plantilla_df['PIEC'] == 'S'
    
    # 2. Si PIEC es S, multiplica "CR" por "FTR"
    plantilla_df.loc[condicion_PIEC_S, 'IREC'] = plantilla_df['CR'] * plantilla_df['FTR']
    
    # 3. Multiplica el resultado por "PU" dividido 100
    plantilla_df.loc[condicion_PIEC_S, 'IREC'] = plantilla_df['IREC'] * (plantilla_df['PU'] / 100)
    
    # 4. Multiplica el resultado por (1 - "RPP")
    plantilla_df.loc[condicion_PIEC_S, 'IREC'] = plantilla_df['IREC'] * (1 - plantilla_df['RPP'])
    
    return plantilla_df

"""
Función para calcular la Variable INVR, tanto en pesos como en millones de
pesos
"""
def calcular_invr(plantilla_df):
    # Si el campo PIEC es 'S', "INVR Cop" = "IREC"
    plantilla_df.loc[plantilla_df['PIEC'] == 'S', 'INVR Cop'] = plantilla_df['IREC']

    # Si el campo PIEC es 'N'
    mask_piec_n = plantilla_df['PIEC'] == 'N'
    resultado = (plantilla_df['CR'] * (plantilla_df['PU'] / 100) * (plantilla_df['FU'] / 100) * (1 - plantilla_df['RPP']))
    plantilla_df.loc[mask_piec_n, 'INVR Cop'] = resultado

    # Calcular "INVR Mill"
    plantilla_df['INVR Mill'] = plantilla_df['INVR Cop'] / 1000000

    return plantilla_df
"""
Función para incluir el campo de Categoría y Descripción de categoría
"""
def categoria_df(plantilla_df):
    # 1. Cargar el archivo Excel en un DataFrame
    ruta_excel = "D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/3. inputs/1. información basica - redes - trafos - municipios/UCs.xlsx"
    excel_df = pd.read_excel(ruta_excel, engine='openpyxl')

    # 2. Combinar plantilla_df con excel_df basado en la llave Unidad Constructiva y Código UC
    merged_df = plantilla_df.merge(excel_df, left_on='Unidad Constructiva', right_on='Código UC', how='left')

    # Actualizar las columnas 'Categoria' y 'Descripción Categoria' en plantilla_df
    plantilla_df['Categoria'] = merged_df['Categoria_y']
    plantilla_df['Descripción Categoria'] = merged_df['Descripción Categoria_y']

    return plantilla_df
"""
Función para incluir el campo de Descripción de UC que sale de operación
"""

def descripcion_uc_out_df(plantilla_df):
    # Cargar el archivo Excel en un DataFrame
    ruta_excel = "D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/3. inputs/1. información basica - redes - trafos - municipios/UCs.xlsx"
    excel_df = pd.read_excel(ruta_excel, engine='openpyxl')

    # Convertir las columnas de merge a string
    plantilla_df['Codigo UC_rep'] = plantilla_df['Codigo UC_rep'].astype(str)
    excel_df['Código UC'] = excel_df['Código UC'].astype(str)

    # Combinar plantilla_df con excel_df basado en la llave Unidad Constructiva y Código UC
    merged_df = plantilla_df.merge(excel_df, left_on='Codigo UC_rep', right_on='Código UC', how='left')

    # Condición para dejar la columna 'Descripción UCs dada de baja' en blanco si 'Codigo UC_rep' está vacío
    # Aquí también asegúrate de manejar correctamente los NaN o valores vacíos después del merge.
    plantilla_df['Descripción UCs dada de baja'] = merged_df['Descripción UC'].where(plantilla_df['Codigo UC_rep'] != 'nan', '')

    return plantilla_df
"""
Función para incluir el campo de Descripción de UC
"""
def descripcion_uc_in_df(plantilla_df):
    # 1. Cargar el archivo Excel en un DataFrame
    ruta_excel = "D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/3. inputs/1. información basica - redes - trafos - municipios/UCs.xlsx"
    excel_df = pd.read_excel(ruta_excel, engine='openpyxl')

    # 2. Combinar plantilla_df con excel_df basado en la llave Unidad Constructiva y Código UC
    merged_df = plantilla_df.merge(excel_df, left_on='Unidad Constructiva', right_on='Código UC', how='left')

    # Actualizar las columnas 'Categoria' y 'Descripción Categoria' en plantilla_df
    plantilla_df['Descripción UCs'] = merged_df['Descripción UC']

    return plantilla_df
"""
Función para calcular el BRAR
"""
def calculo_BRAR(plantilla_df):
    # Paso 1: Leer archivo Excel
    ruta_excel = "D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/3. inputs/1. información basica - redes - trafos - municipios/UCs.xlsx"
    ucs_df = pd.read_excel(ruta_excel, engine='openpyxl')
    
    # Paso 2: Llenar campos k y AR en plantilla_df
    plantilla_df['k'] = plantilla_df['Año entrada operación_rep'].apply(lambda x: 1 if x <= 2007 else 2)
    plantilla_df['AR'] = plantilla_df['Año entrada operación_rep'].apply(lambda x: 10 if x <= 2007 else 0)
    
    # Paso 3: Copiar "Valor instalación [$ dic 2017]" en "CR_rep"
    merged_df = plantilla_df.merge(ucs_df[['Código UC', 'Valor instalación [$ dic 2017]']], left_on='Codigo UC_rep', right_on='Código UC', how='left')
    plantilla_df['CR_rep'] = merged_df['Valor instalación [$ dic 2017]']
    plantilla_df['Área especial'] = merged_df['Área especial']
    # Paso 4: Copiar "CRA" en "CRA_rep" si k=1, de lo contrario es 1. Vacío si "Codigo UC_rep" está vacío
    def get_cra(row):
        if pd.isnull(row['Codigo UC_rep']):
            return ''
        if row['k'] == 1:
            return row['CRA']
        return 1
    
    merged_df = merged_df.merge(ucs_df[['Código UC', 'CRA']], on='Código UC', how='left')
    plantilla_df['CRA_rep'] = merged_df.apply(get_cra, axis=1)
    
    # Paso 5: Copiar "Vida útil" en "VU_rep"
    merged_df = merged_df.merge(ucs_df[['Código UC', 'Vida útil']], on='Código UC', how='left')
    plantilla_df['VU_rep'] = merged_df['Vida útil']
    
    # Limpiamos las columnas extras de las fusiones
    for col in ['Código UC', 'Valor instalación [$ dic 2017]', 'CRA', 'Vida útil']:
        if col in plantilla_df:
            plantilla_df = plantilla_df.drop(columns=col)
    
    # Resta entre 2019 y el año actual
    t = datetime.datetime.now().year - 2018
    plantilla_df['t'] = t
    
    conditions = (plantilla_df['CR_rep'] != 0) & (plantilla_df['CR_rep'].notna()) & \
                 (plantilla_df['CRA_rep'] != 0) & (plantilla_df['CRA_rep'].notna()) & \
                 (plantilla_df['VU_rep'] != 0) & (plantilla_df['VU_rep'].notna()) & \
                 (plantilla_df['AR'] != 0) & (plantilla_df['AR'].notna())

    plantilla_df['BRAR'] = np.where(
        conditions,
        (plantilla_df['CR_rep'] * plantilla_df['PU']/100 * plantilla_df['FU']/100 * 
         (1 - plantilla_df['Rpp_rep']) * plantilla_df['CRA_rep']) * 
         (1 - (t - 1) / (plantilla_df['VU_rep'] - plantilla_df['AR'])),
        0
    )
    plantilla_df['BRAFO'] = plantilla_df['BRAR']
    return plantilla_df

# =============================================================================
# Diligenciamiento automatico de campos 0 o 1, S o N, etc
# =============================================================================

def diligencia_auto(plantilla_df):
    
    plantilla_df['ActivoReconocido'] = 0
    
    return plantilla_df

# =============================================================================
# Diligenciaminento de datos de subestación
# =============================================================================

def info_subestaciones(plantilla_df):
    
    ruta_csv = "D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/3. inputs/1. información basica - redes - trafos - municipios/Subestaciones.csv"
    subestaciones = pd.read_csv(ruta_csv, encoding="ISO-8859-1",sep=';',decimal='.', dtype={"IU": str})
    #Se renombra el campo Nombre a Nombre S
    subestaciones.rename(columns={'Nombre': 'Nombre S'}, inplace=True)
    #Se eliminan las columnas que no se necesitan para seleccionar las coordenadas
    eliminar_columnas = ['CRI/CRIN', 'Año entrada operación', 'Salinidad', 'Operación']
    subestaciones.drop(eliminar_columnas,axis=1,inplace=True)
    # Combinar los DataFrames en función de las columnas "IUS" y "IU"
    plantilla_df = pd.merge(plantilla_df, subestaciones, left_on='IUS', right_on='IU', how='left')  
    #Copiar campos
    plantilla_df['Altitud']=plantilla_df['Altitud_y']
    plantilla_df['Latitud']=plantilla_df['Latitud_y']
    plantilla_df['Longitud']=plantilla_df['Longitud_y']
    plantilla_df['AreaReconocida']=plantilla_df['Área_y']
    plantilla_df['Área']=plantilla_df['Área_y']
    plantilla_df['Valor catastral']=plantilla_df['Valor catastral_y']
    plantilla_df['Código subestación']=plantilla_df['Código OR']
    plantilla_df['Nombre subestación']=plantilla_df['Nombre S']
    # Llenar los campos faltantes o no coincidentes con los valores especificados
    plantilla_df['Altitud'].fillna(0, inplace=True)
    plantilla_df['Longitud'].fillna(-1000, inplace=True)
    plantilla_df['Latitud'].fillna(-1000, inplace=True)
    
    # Eliminar las columnas duplicadas si es necesario
    columnas_duplicadas = ['Altitud_y', 'Longitud_y', 'Latitud_y','IU','Altitud_x', 'Longitud_x', 'Latitud_x','Área_x', 'Área_y', 'Valor catastral_y', 'Valor catastral_x', 'Nombre S']
    plantilla_df.drop(columnas_duplicadas, axis=1, inplace=True)
    return plantilla_df

# =============================================================================
# Llenado Área especial
# =============================================================================

def area_especial(plantilla_df):
     #llamamos el excel de UCs
     ruta_excel = "D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/3. inputs/1. información basica - redes - trafos - municipios/UCs.xlsx"
     ucs_df = pd.read_excel(ruta_excel, engine='openpyxl')
     eliminar_columnas = ['Descripción Categoria', 'Descripción UC', 'Valor instalación [$ dic 2017]', 'Valor unitario [$ dic 2017/MVA]','Vida útil','Desagregación UC','Formato','CRA','Categoria','Nivel de tensión UC']
     ucs_df.drop(eliminar_columnas,axis=1,inplace=True)
     merged_df = plantilla_df.merge(ucs_df, left_on='Unidad Constructiva', right_on='Código UC', how='left')
     plantilla_df['Área especial']=merged_df['Área especial_y']
     return plantilla_df

# =============================================================================


# =============================================================================
# Llenado de observaciones
# =============================================================================

def llenado_observaciones(plantilla_df):
    # Verifica si la columna 'observaciones' está en el dataframe
    if 'Observaciones' in plantilla_df.columns:
        # Aplica una función lambda para actualizar la columna
        plantilla_df['Observaciones'] = plantilla_df['Observaciones'].apply(lambda x: '*' if pd.isnull(x) or x.strip() == '' else x)
    else:
        print("El dataframe no contiene una columna llamada 'observaciones'.")
    return plantilla_df

# =============================================================================
# Llenado de campo Operación
# =============================================================================

def llenado_operación(plantilla_df):
    # Verifica si la columna 'observaciones' está en el dataframe
    if 'Operación' in plantilla_df.columns:
        # Aplica una función lambda para actualizar la columna
        plantilla_df['Operación'] = plantilla_df['Operación'].apply(lambda x: 'S' if pd.isnull(x) or x.strip() == '' else x)
    else:
        print("El dataframe no contiene una columna llamada 'Operación'.")
    return plantilla_df

# =============================================================================
# Llenado de campo tipo de inventario
# =============================================================================

def llenado_tipo_inventario(plantilla_df):
    # Verifica si la columna 'observaciones' está en el dataframe
    if 'Tipo inventario' in plantilla_df.columns:
        # Aplica una función lambda para actualizar la columna
        plantilla_df['Tipo inventario'] = plantilla_df['Tipo inventario'].apply(lambda x: 'INVTR' if pd.isnull(x) or x.strip() == '' else x)
    else:
        print("El dataframe no contiene una columna llamada 'Operación'.")
    return plantilla_df

# =============================================================================
# Llenado de campo Salinidad
# =============================================================================

def llenado_salinidad(plantilla_df):
    # Verifica si la columna 'observaciones' está en el dataframe
    if 'Salinidad' in plantilla_df.columns:
        # Aplica una función lambda para actualizar la columna
        plantilla_df['Salinidad'] = plantilla_df['Salinidad'].apply(lambda x: 'N' if pd.isnull(x) or x.strip() == '' else x)
    else:
        print("La salinidad debe ser 'S' o 'N', para cens es siempre N")
    return plantilla_df
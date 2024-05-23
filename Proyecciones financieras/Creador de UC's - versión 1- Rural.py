# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:22:58 2024

@author: yaboniav
"""

import pandas as pd
import numpy as np
import math

columnas = ['Nombre del proyecto','Nombre municipio','Prioridad','Tipo proyecto',
            'Nivel de tensión UC','Descripción categoría','Código UC','Descripción UC',
            'Subestación','Código subestación','Código línea','Código transformador',
            'MVA Primario / kVar','MVA Secundario','MVA Terciario','Tensión Primario',
            'Tensión Secundario','Tensión Terciario','Valor unitario UC','Número de conductores',
            'Cantidad de UC','Valor total','Fracción de Costo','Año entrada operación',
            'Mes entrada operación','Porcentaje Uso','RPP','Código UC reemplazada',
            'Cantidad de UC reemplazadas','IUA remplazado','Responsable Gestión','Responsable Ejecución',
            'Observaciones CREG','Columna1','Columna2','Columna3','Columna4','Columna5','KM','UN','priorización','tipo de proyecto'
            ]
df_pf = pd.DataFrame(columns=columnas)


df_uc_creg = pd.read_excel('D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//2. Insumos Exp - Rep//1. Reposiciones para habilitar enlaces//Inputs//UCs CREG 015.xlsx')

df_cod_sub = pd.read_excel('D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//2. Insumos Exp - Rep//1. Reposiciones para habilitar enlaces//Inputs//Codigos Subestaciones.xlsx')

# =============================================================================
# 
# =============================================================================

# Asegúrate de tener el archivo correcto y la ruta al archivo aquí
ruta_archivo = 'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//2. Insumos Exp - Rep//1. Reposiciones para habilitar enlaces//Proyectos UC.xlsx'

# Cargar el archivo Excel en un DataFrame
data_base = pd.read_excel(ruta_archivo)

# Agregar las columnas adicionales requeridas
data_base['Unidades constructivas'] = None
data_base['Cantidad'] = None
data_base['Proyecto'] = None
data_base['Tipo'] = None
data_base['Nivel'] = None

# Generar las filas duplicadas según la categoría con la información correspondiente
nuevas_filas = []

# Definir las unidades constructivas y cantidades para cada categoría
unidades_constructivas_auto = [
    ('N2EQ35',1,'Automatización de redes','Tipo IV','n'),
    ('N1T1',1,'Automatización de redes','Tipo IV','n'),
    ('N2EQ14',6,'Automatización de redes','Tipo IV','n'),
    ('N2EQ14',2,'Automatización de redes','Tipo IV','n'),
    ('N2EQ13',2,'Automatización de redes','Tipo IV','n'),
    ('N2EQ9',3,'Automatización de redes','Tipo IV','n'),
    ('N2EQ9',2,'Automatización de redes','Tipo IV','n'),
    ('N2EQ200ESP',1,'Automatización de redes','Tipo IV','n'),
    ('N2L137',1,'Automatización de redes','Tipo IV','n'),
    ('N2L71',1,'Automatización de redes','Tipo IV','n')]

unidades_constructivas_exp = [
    ('N2L84', 'red', 'Expansión redes de distribución CENS','Tipo IV','n'),
    ('N2L136', 'red', 'Expansión redes de distribución CENS','Tipo IV','n'),
    ('N2L73', 'sus', 'Expansión redes de distribución CENS','Tipo IV','n'),
    ('N2L74', 'ret', 'Expansión redes de distribución CENS','Tipo IV','n'),
    ('N2L137', 'tie', 'Expansión redes de distribución CENS','Tipo IV','n')]

unidades_constructivas_rep = [
    ('N2L84', 'red', 'Reposición redes de distribución CENS','Tipo III','n'),
    ('N2L136', 'red', 'Reposición redes de distribución CENS','Tipo III','n'),
    ('N2L73', 'sus', 'Reposición redes de distribución CENS','Tipo III','n'),
    ('N2L74', 'ret', 'Reposición redes de distribución CENS','Tipo III','n'),
    ('N2L137', 'tie', 'Reposición redes de distribución CENS','Tipo III','n')]

unidades_constructivas_regu = [
    ('N2EQ22',3, 'Instalación de reguladores media tensión','Tipo IV','n'),
    ('N2L71',6, 'Instalación de reguladores media tensión','Tipo IV','n'),
    ('N2EQ13',2, 'Instalación de reguladores media tensión','Tipo IV','n'),
    ('N1T1',1, 'Instalación de reguladores media tensión','Tipo IV','n'),
    ('N2EQ9',9, 'Instalación de reguladores media tensión','Tipo IV','n'),
    ('N2EQ9',11, 'Instalación de reguladores media tensión','Tipo IV','n'),
    ('N2EQ14',11, 'Instalación de reguladores media tensión','Tipo IV','n'),
    ('N2L137',4, 'Instalación de reguladores media tensión','Tipo IV','n'),
    ('N2EQ200ESP',2, 'Instalación de reguladores media tensión','Tipo IV','n')]

for index, row in data_base.iterrows():
    if row['CATEGORIA'] == 'Automatización de Redes (Reconectadores)':
        for uc, cantidad, proyecto, tipo, Nivel in unidades_constructivas_auto:
            nueva_fila = row.copy()
            nueva_fila['Unidades constructivas'] = uc
            nueva_fila['Cantidad'] = cantidad*row['CANT_REC']
            nueva_fila['Proyecto'] = proyecto
            nueva_fila['Tipo'] = tipo
            if row['NT'] == 'II': 
                nueva_fila['Nivel']='N.T.2'
            if row['NT'] == 'III': 
                nueva_fila['Nivel']='N.T.3'
            nuevas_filas.append(nueva_fila)
    
    elif row['CATEGORIA'] == 'Reguladores de Tensión':
        for uc, cantidad, proyecto, tipo, Nivel in unidades_constructivas_regu:
            nueva_fila = row.copy()
            nueva_fila['Unidades constructivas'] = uc
            nueva_fila['Cantidad'] = cantidad
            nueva_fila['Proyecto'] = proyecto
            nueva_fila['Tipo'] = tipo
            if row['NT'] == 'II': 
                nueva_fila['Nivel']='N.T.2'
            if row['NT'] == 'III': 
                nueva_fila['Nivel']='N.T.3'
            nuevas_filas.append(nueva_fila)
            
    elif row['CATEGORIA'] == 'Expansión de Red (Enlace)':
        for uc, formula, proyecto, tipo, Nivel in unidades_constructivas_exp:
            nueva_fila = row.copy()
            nueva_fila['Unidades constructivas'] = uc
            
            if 'red' in formula:
                nueva_fila['Cantidad'] = row['DIST_KM']
                
            elif 'sus' in formula:
                nueva_fila['Cantidad'] = math.ceil(row['DIST_KM']/0.13*0.7)
                
            elif 'ret' in formula:
                nueva_fila['Cantidad'] = math.ceil(row['DIST_KM']/0.13*0.3)
                
            elif 'tie' in formula:
                nueva_fila['Cantidad'] = math.ceil(row['DIST_KM']/0.13*0.7)+math.ceil(row['DIST_KM']/0.13*0.3)
                
            nueva_fila['Proyecto'] = proyecto
            nueva_fila['Tipo'] = tipo
            if row['NT'] == 'II': 
                nueva_fila['Nivel']='N.T.2'
            if row['NT'] == 'III': 
                nueva_fila['Nivel']='N.T.3'
            
            nuevas_filas.append(nueva_fila)
            
    elif row['CATEGORIA'] == 'Reposiciones de red':
        for uc, formula, proyecto, tipo, Nivel in unidades_constructivas_rep:
            nueva_fila = row.copy()
            nueva_fila['Unidades constructivas'] = uc
            
            if 'red' in formula:
                nueva_fila['Cantidad'] = row['DIST_KM']
                
            elif 'sus' in formula:
                nueva_fila['Cantidad'] = math.ceil(row['DIST_KM']/0.13*0.7)
                
            elif 'ret' in formula:
                nueva_fila['Cantidad'] = math.ceil(row['DIST_KM']/0.13*0.3)
                
            elif 'tie' in formula:
                nueva_fila['Cantidad'] = math.ceil(row['DIST_KM']/0.13*0.7)+math.ceil(row['DIST_KM']/0.13*0.3)
                
            nueva_fila['Proyecto'] = proyecto
            nueva_fila['Tipo'] = tipo
            if row['NT'] == 'II': 
                nueva_fila['Nivel']='N.T.2'
            if row['NT'] == 'III': 
                nueva_fila['Nivel']='N.T.3'
            
            nuevas_filas.append(nueva_fila)
            

# Convertir la lista de nuevas filas en un DataFrame
nuevas_filas_df = pd.DataFrame(nuevas_filas)

# Guardar el DataFrame final en un nuevo archivo Excel
#ruta_archivo_final = '/mnt/data/Libro1_corregido_final.xlsx'
#data_base_final.to_excel(ruta_archivo_final, index=False)

#ruta_archivo_final

# =============================================================================
# 
# =============================================================================
df_uc_reg = pd.DataFrame(nuevas_filas)


df_pf['Nombre del proyecto'] = df_uc_reg['Proyecto']
df_pf['Nombre municipio'] = df_uc_reg['REGIONAL']
df_pf['Prioridad'] = df_uc_reg['SEGMENTACION ']
df_pf['Tipo proyecto'] = df_uc_reg['Tipo']
df_pf['Código UC'] = df_uc_reg['Unidades constructivas']
df_pf['Cantidad de UC'] = df_uc_reg['Cantidad']
df_pf['Año entrada operación'] = df_uc_reg['FPO_Reg']
df_pf['Columna1'] = df_uc_reg['PROYECTO_PADRE2']
df_pf['Columna2'] = df_uc_reg['PROYECTO_SECUNDARIO']
df_pf['Columna3'] = df_uc_reg['UBICACIÓN']
df_pf['Columna4'] = df_uc_reg['NE_1']
df_pf['Columna5'] = df_uc_reg['NE_2']
df_pf['Código línea'] = df_uc_reg['Alimentador']
mapeos = {  'Nivel de tensión UC': 'Nivel de tensión UC',
            'Descripción categoría': 'Descripción categoría',
            'Descripción UC': 'Descripción UC',
            'Valor unitario UC':'Valor instalación [$ dic 2017]',
            }
for columna_destino, columna_origen in mapeos.items():
    mapeo_actual = dict(zip(df_uc_creg['Código UC'], df_uc_creg[columna_origen]))
    df_pf[columna_destino] = df_pf['Código UC'].map(mapeo_actual)
    

df_pf['Valor total'] = df_pf['Cantidad de UC'] * df_pf['Valor unitario UC']

for index, row in df_pf.iterrows():
    if row['Descripción UC'].startswith("km"):
        df_pf.at[index, 'KM'] = row['Cantidad de UC']
    else:  # Asegúrate de que el 'else' esté correctamente alineado con su 'if' correspondiente.
        df_pf.at[index, 'KM'] = 0

    if row['Descripción UC'].startswith("Reconectador") or row['Descripción UC'].startswith("Regulador"):
        df_pf.at[index, 'UN'] = row['Cantidad de UC']
    else:  # Este 'else' se corresponde con el segundo 'if'.
        df_pf.at[index, 'UN'] = 0
        
#FINAL df_pf

'''for index, row in df_pf.iterrows():
    if row['Nivel de tensión UC'] == "N.T.2" and row['Descripción UC'].startswith("km"):
        row['Número de conductores'] = 3

for index, row in df_pf.iterrows():
    if row['Nivel de tensión UC'] == "N.T.2" and row['Descripción UC'].startswith("km"):
        df_pf.at[index, 'Valor total'] = row['Valor unitario UC'] * row['Cantidad de UC']*row['Número de conductores']/3
    else:
        df_pf.at[index, 'Valor total'] = row['Valor unitario UC'] * row['Cantidad de UC']
'''

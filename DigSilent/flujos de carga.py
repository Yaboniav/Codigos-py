# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:10:09 2024

@author: Yaboniav
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import time
start_time = time.time()  #inicia contador de tiempo
from pathlib import Path
from datetime import datetime, timedelta
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import folium
from folium.plugins import HeatMap
from folium import FeatureGroup
from geopy.point import Point
import simplekml
import random
import hashlib
import statistics
import os
os.environ["PATH"]=r"C:\Program Files\DIgSILENT\PowerFactory 2023 SP5"+os.environ["PATH"]
import sys
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2023 SP5\Python\3.11") 
import powerfactory as pf
app=pf.GetApplication()
app.Show()
user=app.GetCurrentUser()
project=app.ActivateProject('20221103_ModeloElectrico_LP_CENS_Ocaña') # modelo de Factibilidades
prj=app.GetActiveProject()
ldf=app.GetFromStudyCase("ComLdf")
end_time = time.time() #finaliza contador de tiempo
execution_time = round(end_time - start_time, 1) #resta los momentos
print(f"Tiempo de Apertura de DigSilent: {execution_time} segundos")
# =============================================================================
# COMPILAR DE AQUI EN ADELANTE una vez activada la aplicacion DigSilent
# CTRL + shift + fin  ---> F9
# =============================================================================
start_time = time.time()  #inicia contador de tiempo
alt_ejec = "3. PLAYAC2 asume PLAYAC4"
horas_run = 24
carpeta = "D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/01_Estudios/15_Visita a Regionales/00_ESTUDIOS/04_Mejoramiento Calidad del Servicio OCALA_PLAYA"
ubicacion = carpeta + "/" + alt_ejec
alimentadores_impactados = ['OCALA_PLAYA','CONSAL_TEORA','PLAYAC1','PLAYAC2','PLAYAC3','PLAYAC5','OCAGONZALES']  #
transformadores_potencia_impactados = ['TS28-OCAÑA-47MVA_NTR','TS_LA_PLAYA_5MVA','TS26-CONVENCION-7MVA']   #
ruta = Path(carpeta)
if not ruta.is_dir():
  ruta.mkdir(parents=True, exist_ok=True)
ubicacion = carpeta + "/" + alt_ejec
ruta_1 = Path(ubicacion)
if not ruta_1.is_dir():
  ruta_1.mkdir(parents=True, exist_ok=True)
# CARGA DE OBJETOS DEL DIGSILENT
data_tensiones = []
data_cargas = []
data_lineas = []
data_tr_bi = []
data_tr_tri = []
nodos = app.GetCalcRelevantObjects('*.ElmTerm')
cargas = app.GetCalcRelevantObjects('*.ElmLod')
lineas = app.GetCalcRelevantObjects('*.ElmLne')
trafos_bi = app.GetCalcRelevantObjects('*.ElmTr2')
trafos_tri = app.GetCalcRelevantObjects('*.ElmTr3')
# =============================================================================
# FLUJO DE POTENCIA HORARIA
# =============================================================================
for flujo_potencia in range(horas_run):
  studytime = app.GetFromStudyCase('SetTime')
  tiempo = flujo_potencia * 1000000
  tiempo_str = str(tiempo)
  studytime.cTime = tiempo_str
  ldf.Execute()  
  print(flujo_potencia + 1 , " - Time:", datetime.now().time().strftime("%HH:%MM:%SS"))
  # =============================================================================
  # TENSIONES EN NODOS
  # =============================================================================
  for nodo in nodos:
    energizado = nodo.GetAttribute('e:ciEnergized')
    fuera_servicio = nodo.GetAttribute('e:outserv')
    if energizado == 1 and fuera_servicio == 0: #solo se tiene en cuenta lo activado y energizado
      hora = str(flujo_potencia) + ':00'
      nombre_nodo = nodo.GetAttribute('loc_name')
      tension_nominal = nodo.GetAttribute('e:uknom')
      tension_real = nodo.GetAttribute('m:U1l')
      fases = nodo.GetAttribute('b:nphase')
      feeder = str(nodo.GetAttribute('e:cpFeed')) 
      lat = nodo.GetAttribute('e:GPSlat')
      lon = nodo.GetAttribute('e:GPSlon')
      datos_ten = {'HORA': hora,'NOMBRE_NE': nombre_nodo,'TEN_NOM': tension_nominal,
                   'TEN_REAL': tension_real,'FASES': fases,'FEEDER': feeder,'LAT': lat, 'LONG': lon }
      data_tensiones.append(datos_ten)
  # =============================================================================
  # CARGAS TRANSFORMADORES DISTRIBUCION
  # =============================================================================
  for carga in cargas:
    energizado = carga.GetAttribute('e:ciEnergized')
    fuera_servicio = carga.GetAttribute('e:outserv')
    if energizado == 1 and fuera_servicio == 0:  #solo se tiene en cuenta lo activado y energizado
      hora = str(flujo_potencia) + ':00'
      nombre_carga = carga.GetAttribute('loc_name')
      ne_conectado = str(carga.GetAttribute('e:bus1'))
      carga_P = carga.GetAttribute('m:Psum:bus1')
      feeder = str(carga.GetAttribute('e:cpFeed')) 
      datos_cargas = {'HORA': hora,'NOMBRE_CARGA': nombre_carga,'NE_CARGA': ne_conectado,
                      'CARGA_MVA': carga_P,'FEEDER': feeder}
      data_cargas.append(datos_cargas)
  # =============================================================================
  # CARGABILIDAD DE LAS LINEAS
  # =============================================================================
  for linea in lineas:
    energizado = linea.GetAttribute('e:ciEnergized')
    fuera_servicio = linea.GetAttribute('e:outserv')
    if energizado == 1 and fuera_servicio == 0:  #solo se tiene en cuenta lo activado y energizado
      hora = str(flujo_potencia) + ':00'
      nombre_linea = linea.GetAttribute('loc_name')
      distancia = linea.GetAttribute('b:dline')
      ne_conectado_1 = str(linea.GetAttribute('e:bus1'))
      ne_conectado_2 = str(linea.GetAttribute('e:bus2'))
      I_kA_NOM = linea.GetAttribute('t:sline')
      I_kA_REAL = linea.GetAttribute('m:I:bus1')
      V_kV_REAL = linea.GetAttribute('m:U1l:bus1')
      perdidas = linea.GetAttribute('c:Losses')
      feeder = str(linea.GetAttribute('e:cpFeed'))
      datos_lineas = {'HORA': hora,'NOMBRE_LINEA': nombre_linea,'LONGITUD': distancia,
                      'NE_1': ne_conectado_1,'NE_2': ne_conectado_2, 'I_kA_NOM': I_kA_NOM,
                      'I_kA_REAL': I_kA_REAL,'V_kV_REAL': V_kV_REAL,'P_LOSS': perdidas,'FEEDER': feeder}
      data_lineas.append(datos_lineas)
  # =============================================================================
  # TRANSFORMADOR BI DEVANADOS
  # =============================================================================
  for tr_bi in trafos_bi:
    energizado = tr_bi.GetAttribute('e:ciEnergized')
    fuera_servicio = tr_bi.GetAttribute('e:outserv')
    if energizado == 1 and fuera_servicio == 0:  #solo se tiene en cuenta lo activado y energizado
      hora = str(flujo_potencia) + ':00'
      nombre = tr_bi.GetAttribute('loc_name')
      tap= tr_bi.GetAttribute('e:nntap')
      capacidad = tr_bi.GetAttribute('e:Snom')
      cargabilidad_hv = tr_bi.GetAttribute('m:Ssum:bushv')
      cargabilidad_lv = tr_bi.GetAttribute('m:Ssum:buslv')
      feeder = str(tr_bi.GetAttribute('e:cpFeed'))
      datos_tr_bi = {'HORA': hora,'NOMBRE_TR': nombre,'TAP': tap, 'S_NOM': capacidad, 
                      'S_REAL_HV': cargabilidad_hv, 'S_REAL_LV': cargabilidad_lv,'FEEDER': feeder}
      data_tr_bi.append(datos_tr_bi)      
  # =============================================================================
  # TRANSFORMADOR TRI DEVANADOS
  # =============================================================================
  for tr_tri in trafos_tri:
    energizado = tr_tri.GetAttribute('e:ciEnergized')
    fuera_servicio = tr_tri.GetAttribute('e:outserv')
    if energizado == 1 and fuera_servicio == 0:  #solo se tiene en cuenta lo activado y energizado
      hora = str(flujo_potencia) + ':00'
      nombre = tr_tri.GetAttribute('loc_name')
      tap= tr_tri.GetAttribute('e:n3tap_h')
      capacidad = tr_tri.GetAttribute('t:strn3_h')
      cargabilidad_hv = tr_tri.GetAttribute('m:Ssum:bushv')
      cargabilidad_lv = tr_tri.GetAttribute('m:Ssum:buslv')
      feeder = str(tr_tri.GetAttribute('e:cpFeed'))
      datos_tr_tri = {'HORA': hora,'NOMBRE_TR': nombre,'TAP': tap, 'S_NOM': capacidad, 
                      'S_REAL_HV': cargabilidad_hv, 'S_REAL_LV': cargabilidad_lv,'FEEDER': feeder}
      data_tr_tri.append(datos_tr_tri)
# =============================================================================
# MANEJO DE DATAFRAMES
# =============================================================================
# TENSIONES
print ("Consolidando y Ajustando tabla de TENSIONES", datetime.now().time().strftime("%HH:%MM:%SS"))
df_tensiones = pd.DataFrame(data_tensiones)
df_tensiones = df_tensiones[df_tensiones['NOMBRE_NE'].str.startswith('N_')] # se filtran solo los N_
df_tensiones = df_tensiones[df_tensiones['FASES'] > 1] # se filtran solo dejando FF y FFF
df_tensiones['FEEDER'] = df_tensiones['FEEDER'].str.extract(r'IntFeeder\\(.+?)\.ElmFeeder<\/l3>') # se renombra Feeder
df_tensiones['TEN_NOM'] = round(df_tensiones['TEN_NOM'],3).astype(float)
df_tensiones['TEN_REAL'] = round(df_tensiones['TEN_REAL'],3).astype(float)
df_tensiones['TEN_PU'] = np.where(df_tensiones['TEN_NOM'] == 13.8,
                                      df_tensiones['TEN_REAL'] / 13.2, 
                                      df_tensiones['TEN_REAL'] / df_tensiones['TEN_NOM'])
df_tensiones['TEN_PU'] = round(df_tensiones['TEN_PU'],3).astype(float)
df_tensiones['TEN_PU'] = round(df_tensiones['TEN_PU'],3).astype(float)
df_tensiones  = df_tensiones[df_tensiones['FEEDER'].isin(alimentadores_impactados)]
df_tensiones.to_excel( ubicacion + "/01_Nodos.xlsx", index=False)
# LINEAS
print ("Consolidando y Ajustando tabla de LINEAS", datetime.now().time().strftime("%HH:%MM:%SS"))
df_lineas = pd.DataFrame(data_lineas)
df_lineas = df_lineas[df_lineas['NOMBRE_LINEA'].str.startswith('L_')] # se filtran solo los L_
df_lineas['NE_1'] = df_lineas['NE_1'].str.extract(r'.ElmNet\\(.*?)\.ElmTerm')
df_lineas['NE_2'] = df_lineas['NE_2'].str.extract(r'.ElmNet\\(.*?)\.ElmTerm')
df_lineas['FEEDER'] = df_lineas['FEEDER'].str.extract(r'IntFeeder\\(.+?)\.ElmFeeder')
df_lineas['P_LOSS'] = df_lineas['P_LOSS'].abs()
df_lineas['P_LOSS'] = df_lineas['P_LOSS'] / 1000
df_lineas['CARGABILIDAD'] = df_lineas['I_kA_REAL'] / df_lineas['I_kA_NOM']
df_lineas  = df_lineas[df_lineas['FEEDER'].isin(alimentadores_impactados)]
df_lineas.to_excel(ubicacion + "/02_Lineas.xlsx", index=False)
# CARGAS
print ("Consolidando y Ajustando tabla de CARGAS", datetime.now().time().strftime("%HH:%MM:%SS"))
df_cargas = pd.DataFrame(data_cargas)
df_cargas = df_cargas[df_cargas['NOMBRE_CARGA'].str.startswith('C_')] # se filtran solo los C_
df_cargas['NE_CARGA'] = df_cargas['NE_CARGA'].str.extract(r'.ElmNet\\(.*?)\.ElmTerm')
df_cargas['FEEDER'] = df_cargas['FEEDER'].str.extract(r'IntFeeder\\(.+?)\.ElmFeeder')
df_cargas  = df_cargas[df_cargas['FEEDER'].isin(alimentadores_impactados)]
df_cargas.to_excel(ubicacion + "/03_Cargas.xlsx", index=False) # Exporte de Excel
# TRANFORMADORES BIDEVANADOS
print ("Consolidando y Ajustando tabla de TRAFOS BIDEVANADOS", datetime.now().time().strftime("%HH:%MM:%SS"))
df_tr_bi = pd.DataFrame(data_tr_bi)
df_tr_bi = df_tr_bi[df_tr_bi['NOMBRE_TR'].str.startswith('TS')] # se filtran solo los TS
df_tr_bi['FEEDER'] = df_tr_bi['FEEDER'].str.extract(r'IntFeeder\\(.+?)\.ElmFeeder')
df_tr_bi['CARGABILIDAD'] = df_tr_bi['S_REAL_HV'] / df_tr_bi['S_NOM']
df_tr_bi['S_LOSS_TR'] = df_tr_bi['S_REAL_HV'] - df_tr_bi['S_REAL_LV']
df_tr_bi  = df_tr_bi[df_tr_bi['NOMBRE_TR'].isin(transformadores_potencia_impactados)]
df_tr_bi.to_excel(ubicacion + "/04_TR_bi.xlsx", index=False)
# TRANFORMADORES TRIDEVANADOS
print ("Consolidando y Ajustando tabla de TRAFOS TRIDEVANADOS", datetime.now().time().strftime("%HH:%MM:%SS"))
df_tr_tri = pd.DataFrame(data_tr_tri)
df_tr_tri = df_tr_tri[df_tr_tri['NOMBRE_TR'].str.startswith('TI')] # se filtran solo los TI
df_tr_tri['FEEDER'] = df_tr_tri['FEEDER'].str.extract(r'IntFeeder\\(.+?)\.ElmFeeder')
df_tr_tri['CARGABILIDAD'] = df_tr_tri['S_REAL_HV'] / df_tr_tri['S_NOM']
df_tr_tri['S_LOSS_TR'] = df_tr_tri['S_REAL_HV'] - df_tr_tri['S_REAL_LV']
df_tr_tri = df_tr_tri[df_tr_tri['NOMBRE_TR'].isin(transformadores_potencia_impactados)]
df_tr_tri.to_excel(ubicacion + "/05_TR_tri.xlsx", index=False)
# =============================================================================
# crear mapa de folium para FEEDER, tensiones de lineas y cargabilidades de lineas
# =============================================================================
# tensiones
df_NE = df_tensiones.copy()
min_TEN_PU = df_NE['TEN_PU'].min()
HMT = df_NE[df_NE['TEN_PU'] == min_TEN_PU]['HORA'].iloc[0]  # hora de mínima tensión
df_NE = df_NE[df_NE['HORA'] == HMT]
# asignación de tensiones a líneas
df_RED_ten = df_lineas[df_lineas['FEEDER'].isin(alimentadores_impactados)].copy()
df_RED_ten = df_RED_ten.drop(['I_kA_REAL', 'I_kA_NOM', 'V_kV_REAL', 'P_LOSS', 'CARGABILIDAD'], axis=1)
df_RED_ten = df_RED_ten.merge(df_NE[['NOMBRE_NE', 'LAT', 'LONG', 'TEN_PU']], left_on='NE_1', right_on='NOMBRE_NE', how='left', suffixes=('', '_1'))
df_RED_ten = df_RED_ten.merge(df_NE[['NOMBRE_NE', 'LAT', 'LONG', 'TEN_PU']], left_on='NE_2', right_on='NOMBRE_NE', how='left', suffixes=('', '_2'))
df_RED_ten.rename(columns={'LAT': 'LAT1', 'LONG': 'LONG1', 'LAT_2': 'LAT2', 'LONG_2': 'LONG2', 'TEN_PU': 'TEN_PU1', 'TEN_PU_2': 'TEN_PU2'}, inplace=True)
df_RED_ten.drop(columns=['NOMBRE_NE', 'NOMBRE_NE_2'], inplace=True, errors='ignore')
df_RED_ten = df_RED_ten.drop_duplicates(subset='NOMBRE_LINEA')
df_RED_ten = df_RED_ten.dropna(subset=['LAT1', 'LONG1', 'LAT2', 'LONG2'])
df_RED_ten['TEN_PU'] = np.mean([df_RED_ten['TEN_PU1'], df_RED_ten['TEN_PU2']], axis=0)
df_RED_ten = df_RED_ten.drop(['HORA','TEN_PU1', 'TEN_PU2'], axis=1)
df_RED_ten['NE_1'] = df_RED_ten['NE_1'].str.replace("N_", "", regex=True)
df_RED_ten['NE_2'] = df_RED_ten['NE_2'].str.replace("N_", "", regex=True)
df_RED_ten['NOMBRE_LINEA'] = df_RED_ten['NOMBRE_LINEA'].str.replace("L_", "", regex=True)
# datos de cargabilidades de lineas
df_RED_load = df_lineas[df_lineas['FEEDER'].isin(alimentadores_impactados)].copy()
max_DEMANDA = df_RED_load['CARGABILIDAD'].max()
HMD = df_RED_load[df_RED_load['CARGABILIDAD'] == max_DEMANDA]['HORA'].iloc[0]
df_RED_load = df_RED_load[df_RED_load['HORA'] == HMD]
df_RED_load = df_RED_load.merge(df_NE[['NOMBRE_NE', 'LAT', 'LONG']], left_on='NE_1', right_on='NOMBRE_NE', how='left', suffixes=('', '_1'))
df_RED_load = df_RED_load.merge(df_NE[['NOMBRE_NE', 'LAT', 'LONG']], left_on='NE_2', right_on='NOMBRE_NE', how='left', suffixes=('', '_2'))
df_RED_load.rename(columns={'LAT': 'LAT1', 'LONG': 'LONG1', 'LAT_2': 'LAT2', 'LONG_2': 'LONG2'}, inplace=True)
df_RED_load.drop(columns=['NOMBRE_NE', 'NOMBRE_NE_2'], inplace=True, errors='ignore')
df_RED_load = df_RED_load.drop_duplicates(subset='NOMBRE_LINEA')
df_RED_load = df_RED_load.dropna(subset=['LAT1', 'LONG1', 'LAT2', 'LONG2'])
df_RED_load.drop('HORA', axis=1, inplace=True)
df_RED_load['NE_1'] = df_RED_load['NE_1'].str.replace("N_", "", regex=True)
df_RED_load['NE_2'] = df_RED_load['NE_2'].str.replace("N_", "", regex=True)
df_RED_load['NOMBRE_LINEA'] = df_RED_load['NOMBRE_LINEA'].str.replace("L_", "", regex=True)
# Creación del mapa
mapa = folium.Map(location=[df_RED_ten['LAT1'].mean(), df_RED_ten['LONG1'].mean()], zoom_start=10)
# Función para elegir color por tensión
def elige_color_TENSIONES(tension):
    if tension > 1.1:
        return 'red'
    elif 0.95 <= tension <= 1.1:
        return 'black'
    elif 0.9 <= tension <= 0.95:
        return 'blue'
    else:
        return 'red'
# Función para elegir color por cargabilidad
def elige_color_CARGABILIDAD(cargabilidad):
    if cargabilidad > 0.7:
        return 'red'
    elif 0.4 <= cargabilidad <= 0.7:
        return 'blue'
    else:
        return 'black'
# Función para elegir color por FEEDER
alimentadores_unicos = sorted(df_RED_load['FEEDER'].unique())
# Lista de colores predefinidos
colores = ['#ff00ff', '#2a73cc', '#7ed957','#fc7323']
def elige_color_FEEDER_html(feeder):
    # Encuentra el índice del alimentador en la lista de alimentadores únicos
    try:
        index = alimentadores_unicos.index(feeder)
        # Selecciona un color de la lista de colores usando el índice del alimentador
        color = colores[index % len(colores)]  # Usa módulo para evitar errores de índice fuera de rango
    except ValueError:
        # En caso de que el alimentador no esté en la lista, asigna un color por defecto
        color = '#000000FF'  # Negro como color por defecto
    return color 
# Creación de capas para cada FEEDER
feeders_unicos = df_RED_ten['FEEDER'].unique()
for feeder in feeders_unicos:
    capa_feeder = folium.FeatureGroup(name=f'{feeder}', show=True)
    df_filtrado = df_RED_ten[df_RED_ten['FEEDER'] == feeder]  
    for _, fila in df_filtrado.iterrows():
        punto_inicio = [fila['LAT1'], fila['LONG1']]
        punto_fin = [fila['LAT2'], fila['LONG2']]
        descripcion = f"{fila['NOMBRE_LINEA']}  {fila['FEEDER']}  {fila['TEN_PU']}p.u."
        color_linea = elige_color_FEEDER_html(feeder)  # Opcional: Podrías querer un color fijo por FEEDER
        linea = folium.PolyLine(locations=[punto_inicio, punto_fin], color=color_linea, weight=4)
        linea.add_child(folium.Popup(descripcion))
        capa_feeder.add_child(linea) 
    mapa.add_child(capa_feeder)   
# Capa de mapa de tensiones   
capa_tensiones = folium.FeatureGroup(name='Tensiones', show=False)
for _, fila in df_RED_ten.iterrows():
    punto_inicio = [fila['LAT1'], fila['LONG1']]
    punto_fin = [fila['LAT2'], fila['LONG2']]
    descripcion = f"{fila['NOMBRE_LINEA']} {fila['FEEDER']}  {fila['TEN_PU']}p.u." 
    linea = folium.PolyLine(locations=[punto_inicio, punto_fin], color=elige_color_TENSIONES(fila['TEN_PU']), weight=4)
    linea.add_child(folium.Popup(descripcion))
    capa_tensiones.add_child(linea)
mapa.add_child(capa_tensiones)    
# Capa de mapa de Cargabilidad
capa_cargabilidad = folium.FeatureGroup(name='Cargabilidad', show=False)
for _, fila in df_RED_load.iterrows():
    punto_inicio = [fila['LAT1'], fila['LONG1']]
    punto_fin = [fila['LAT2'], fila['LONG2']]
    cargabilidad_redondeada = round(fila['CARGABILIDAD'], 3) * 100
    descripcion = f"{fila['NOMBRE_LINEA']}  {fila['FEEDER']}  {cargabilidad_redondeada}%"
    linea = folium.PolyLine(locations=[punto_inicio, punto_fin], color=elige_color_CARGABILIDAD(fila['CARGABILIDAD']), weight=4)
    linea.add_child(folium.Popup(descripcion))
    capa_cargabilidad.add_child(linea)    
mapa.add_child(capa_cargabilidad)
# Añadir control de capas y guardar el mapa
folium.LayerControl().add_to(mapa)
mapa.save(ubicacion + "/" + '06_Mapa_Lineas.html')
# =============================================================================
# crear grafico de perfiles de tension por alimentador
# =============================================================================
alimentadores = df_RED_ten['FEEDER'].unique()
for alimentador in alimentadores:
    df_alimentador = df_RED_ten[df_RED_ten['FEEDER'] == alimentador]
    df_alimentador = df_alimentador.sort_values(by='TEN_PU', ascending=False)
    fig = px.line(df_alimentador, x='NOMBRE_LINEA', y='TEN_PU', title=f'Perfiles de Tensión en {alimentador} a las {HMT} - hora de mínima tensión')
    fig.add_hline(y=1.1, line_dash="dash", line_color="black", annotation_text="Lim max")
    fig.add_hline(y=0.9, line_dash="dash", line_color="black", annotation_text="Lim min")
    if df_alimentador['TEN_PU'].min() < 0.9:
        fig.add_hline(y=df_alimentador['TEN_PU'].min(), line_dash="dash", line_color="red", annotation_text="Tensión min")
    else:
        fig.add_hline(y=df_alimentador['TEN_PU'].min(), line_dash="dash", line_color="green", annotation_text="Tensión min")
    fig.update_layout(yaxis_title="Tensión p.u.")
    # Guardar la figura como un archivo HTML
    nombre_archivo = f'07_Perfiles_Tensión_{alimentador}.html'
    ruta_archivo = ubicacion + "/" + nombre_archivo
    fig.write_html(ruta_archivo)
# =============================================================================
# Crear gráficos de demanda por alimentador
# =============================================================================
for alimentador in alimentadores_impactados:
    # Filtrar el DataFrame por alimentador
    df_DEMANDA_ALIMENTADOR = df_lineas[df_lineas['FEEDER'] == alimentador].copy()
    max_DEMANDA_ALIMENTADOR = df_DEMANDA_ALIMENTADOR['I_kA_REAL'].max()
    LMD = df_DEMANDA_ALIMENTADOR[df_DEMANDA_ALIMENTADOR['I_kA_REAL'] == max_DEMANDA_ALIMENTADOR]['NOMBRE_LINEA'].iloc[0]
    df_DEMANDA_ALIMENTADOR = df_DEMANDA_ALIMENTADOR[df_DEMANDA_ALIMENTADOR['NOMBRE_LINEA'] == LMD]
    df_DEMANDA_ALIMENTADOR["S_MVA"] = df_DEMANDA_ALIMENTADOR["I_kA_REAL"] * df_DEMANDA_ALIMENTADOR["V_kV_REAL"] * 1.732051
    ALIMENT = df_DEMANDA_ALIMENTADOR['FEEDER'].iloc[0]
    fig = px.line(df_DEMANDA_ALIMENTADOR, x='HORA', y='S_MVA', title=f'Demanda horaria en MVA del alimentador {ALIMENT}')
    fig.update_traces(line=dict(shape='spline'))
    fig.update_layout(yaxis_title="S - MVA")
    fig.write_html(ubicacion + "/" + f'08_Demanda_Alimentador_{ALIMENT}.html')
# =============================================================================
# crear grafico de cargabilidades de lineas
# =============================================================================
for alimentador in alimentadores_impactados:
    df_RED_load_alimentador = df_RED_load[df_RED_load['FEEDER'] == alimentador].copy()
    df_RED_load_alimentador = df_RED_load_alimentador.sort_values(by='CARGABILIDAD', ascending=False)
    df_RED_load_alimentador['CARGABILIDAD'] = df_RED_load_alimentador['CARGABILIDAD'] * 100
    fig = px.line(df_RED_load_alimentador, x='NOMBRE_LINEA', y='CARGABILIDAD', title=f'Cargabilidad de Líneas del alimentador {alimentador} a las {HMD} - hora de máxima demanda')
    if df_RED_load_alimentador['CARGABILIDAD'].max() >= 90:
        fig.add_hline(y=100, line_dash="dash", line_color="black", annotation_text="Load 100%")
    fig.add_hline(y=df_RED_load_alimentador['CARGABILIDAD'].max(), line_dash="dash", line_color="red", annotation_text="Load max")
    fig.update_layout(yaxis_title="Cargabilidad %", yaxis=dict(range=[0, df_RED_load_alimentador['CARGABILIDAD'].max()]))
    fig.write_html(ubicacion + "/" + f'09_Cargabilidad_lineas_{alimentador}.html')
# =============================================================================
# grafico para transformadores de potencia
# =============================================================================
df_TR = df_tr_bi.copy()
df_TR = df_TR[df_TR['NOMBRE_TR'].isin(transformadores_potencia_impactados)]
df_TR['CARGABILIDAD'] = df_TR['CARGABILIDAD'] * 100
fig = px.line(df_TR, x='HORA', y='CARGABILIDAD', color='NOMBRE_TR',
              title='Cargabilidad de Transformadores de Potencia Impactados',
              labels={'CARGABILIDAD': 'Cargabilidad en %', 'HORA': 'Hora'})
if df_TR['CARGABILIDAD'].max() >= 0.85:
    fig.add_hline(y=df_TR['CARGABILIDAD'].max(), line_dash="dash", line_color="red", annotation_text="Load max")
else:
    fig.add_hline(y=df_TR['CARGABILIDAD'].min(), line_dash="dash", line_color="green", annotation_text="Load max")
fig.update_layout(yaxis_title="Cargabilidad en % ")
fig.write_html(ubicacion + "/" + '10_Transformadores_de_Potencia.html')
# =============================================================================
# Perdidas del Alimentador por FEEDER
# =============================================================================
for alimentador in alimentadores_impactados:
    # Filtrar el DataFrame por alimentador
    df_ALIM_LOSS = df_lineas[df_lineas['FEEDER'] == alimentador].copy()
    perdidas_energia = df_ALIM_LOSS["P_LOSS"].sum()
    max_DEMANDA_ALIMENTADOR = df_ALIM_LOSS['I_kA_REAL'].max()
    LMD = df_ALIM_LOSS[df_ALIM_LOSS['I_kA_REAL'] == max_DEMANDA_ALIMENTADOR]['NOMBRE_LINEA'].iloc[0]
    df_ALIM_LOSS = df_ALIM_LOSS[df_ALIM_LOSS['NOMBRE_LINEA'] == LMD]
    df_ALIM_LOSS["S_MVA"] =df_ALIM_LOSS["I_kA_REAL"] * df_ALIM_LOSS["V_kV_REAL"] * 1.732051
    energia_total = df_ALIM_LOSS["S_MVA"].sum()
    Porcentaje_loss = round(perdidas_energia / energia_total, 3)
    energia_neta = energia_total - perdidas_energia
    data = pd.DataFrame({'Categoría': ['Energía Neta MWh/día', 'Pérdidas Energía MWh/día'],
                         'Valor': [energia_neta, perdidas_energia]})
    fig = px.pie(data, values='Valor', names='Categoría', title=f'Pérdidas Técnicas de Energía (MWh/día) - Alimentador {alimentador}')
    fig.update_traces(textinfo='percent+label', insidetextfont={'size': 15}, outsidetextfont={'size': 15})
    fig.write_html(ubicacion + "/" + f'11_Pérdidas_de_Energía_{alimentador}.html')
# =============================================================================
# Generacion de KMZ
# =============================================================================
df_KMZ = df_RED_ten
df_KMZ = df_KMZ.merge(df_RED_load[['NOMBRE_LINEA', 'CARGABILIDAD']], on='NOMBRE_LINEA', how='left', suffixes=('', 'CARGABILIDAD'))
alimentadores_impactados = df_KMZ['FEEDER'].unique()
colores_kmz = ['#FFC0CBFF', '#FFC0CBFF',
               '#FF5733FF', '#FFD700FF', 
               '#4169E1FF', '#FF4500FF', 
               '#FF1493FF','#FFA07AFF', '#FF6347FF' ]
for alimentador in alimentadores_impactados:
    kml_red = simplekml.Kml()
    random.shuffle(colores_kmz)
    color_alimentador = colores_kmz.pop()
    for _, row in df_KMZ[df_KMZ['FEEDER'] == alimentador].iterrows():
        nombre_linea = str(row["NOMBRE_LINEA"])
        estilo_linea = simplekml.Style()
        estilo_linea.linestyle.color = color_alimentador
        estilo_linea.linestyle.width = 3
        linea = kml_red.newlinestring(name=nombre_linea)
        linea.style = estilo_linea
        linea.coords = [(row['LONG1'], row['LAT1']), (row['LONG2'], row['LAT2'])]
        longitud_redondeada = round(row['LONGITUD'], 3) * 1000
        porc_load = round(row['CARGABILIDAD'] * 100, 5)
        description = f"NE_1: {row['NE_1']}\nNE_2:  {row['NE_2']}\nDistancia: {longitud_redondeada} metros\nAlimentador: {row['FEEDER']}\nTensión PU: {row['TEN_PU']}\nCargabilidad: {porc_load}%"
        linea.description = description
    nombre_archivo = f"12_{alimentador}.kmz"
    ruta_archivo = ubicacion + "/" + nombre_archivo
    kml_red.save(str(ruta_archivo))


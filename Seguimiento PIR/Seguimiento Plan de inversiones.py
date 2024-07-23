# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:30:17 2023

@author: yaboniav
"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
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

from menu import seleccionar_opcion_desde_menu

if __name__ == "__main__":
    equipo_trabajo = seleccionar_opcion_desde_menu()
    print(f"La opción seleccionada fue: {equipo_trabajo}")
    # Ahora puedes usar la variable opcion_final como desees.
  
#--------------Creación de data frame con todos los campos ------------------# 

global_data = pd.read_csv('D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/campos a reportar.csv',sep=';',decimal='.')

plantilla = global_data.copy()
plantilla = plantilla[['Nombre del Campo']]
plantilla = plantilla.transpose()
plantilla = plantilla.set_axis(plantilla.iloc[0], axis='columns')
plantilla = plantilla[1:]

cols_to_convert = [
    'Capacidad', 'INVR Cop', 'INVR Mill', "Descripción UC's",
    'Categoria', 'BRAR', 'CR_rep', 'CRA_rep', 'AR', 'k', 'ActivoReconocido', 'Altitud',
    'Área', 'Área especial', 'AreaReconocida', 'FactorSecundario', 'FactorTerciario',
    'Latitud', 'Longitud', 'Nivel alta', 'Nivel baja 1', 'Nivel baja 2', 'Nivel baja 3',
    'Potencia baja 1', 'Potencia baja 2', 'Potencia baja 3', 'Valor catastral', 'CR',
    'PU', 'FU', 'Psn', 'Valor Regulatorio Aprobado', 'Relación Beneficio Costo',
    'Valor de Ejecución Real del Proyecto ($)', 'Valor de Ejecución Regulatorio',
    'BRAEN_RP', 'INVTR_RP', 'IREC_RP', 'BRAFO', 'RCBIAFO', 'RCNAFO', 'BRT', 'Capacidad_rep','Cantidad','Capacidad [MVA]','Capacidad [MVA]_rep','km de conductor'
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

    folder_path = (f"D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/2024/4. Seguimiento/3. inputs - informes spard/{equipo_trabajo}")
    plantilla_equipo = read_excel_from_directory(folder_path)

#------------------------VALIDADOR DE LAS PLANTILLAS--------------------------#

from script_validador import validador

if __name__ == "__main__":
    # Llamar a la función con el DataFrame creado
    df_corregido, df_resultados = validador(plantilla_equipo)
    # Guardar el DataFrame de errores en un archivo Excel
    df_resultados = df_resultados[df_resultados["Descripción del Error"] != "Sin errores"]
    nombre_archivo = f"{equipo_trabajo} errores.xlsx"
    ruta_errores = "D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/BD_seguimiento/2. errores plantillas seguimiento"
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

# Copia las columnas compartidas de df_corregido a plantilla
plantilla[shared_columns] = df_corregido[shared_columns]

from llenado_plantilla import seleccionar_equipo_ejecutor
from llenado_plantilla import mapear_subgerencia
from llenado_plantilla import calcular_CR
from llenado_plantilla import copiar_FU_PU
from llenado_plantilla import llenar_FTR
from llenado_plantilla import calcular_IREC
from llenado_plantilla import calcular_invr
from llenado_plantilla import categoria_df
from llenado_plantilla import descripcion_uc_in_df
from llenado_plantilla import descripcion_uc_out_df
from llenado_plantilla import calculo_BRAR
from llenado_plantilla import diligencia_auto
from llenado_plantilla import info_subestaciones
from llenado_plantilla import area_especial
from llenado_plantilla import llenado_observaciones
from llenado_plantilla import llenado_operación
from llenado_plantilla import llenado_tipo_inventario
from llenado_plantilla import llenado_salinidad
if __name__ == "__main__":

    # Llamada a la función y asignación del resultado a una variable
    equipo_ejecutor_seleccionado = seleccionar_equipo_ejecutor()
    
    # Llenado del campo Equipo Ejecutor
    plantilla["Equipo Ejecutor"] = equipo_ejecutor_seleccionado
    # Llenado del campo subgerencia Ejecutora
    plantilla["Subgerencia Ejecutora"] = mapear_subgerencia(equipo_ejecutor_seleccionado)
    # Llenado del campo CR
    plantilla = calcular_CR(plantilla)
    #Llenado de los campos FU y PU
    plantilla = copiar_FU_PU(plantilla)
    #Llenado de la variable FTR - cobertura
    plantilla = llenar_FTR(plantilla)
    #Llenado de la variable IREC
    plantilla = calcular_IREC(plantilla)
    #Llenado de la variable INVR
    plantilla = calcular_invr(plantilla)
    #llenado de las variables Categoría y Descripción de Categoría
    plantilla = categoria_df(plantilla)
    #llenado de las variables Descripción de UC's
    plantilla = descripcion_uc_in_df(plantilla)
    #llenado de las variables Descripción de Ucs dadas de baja
    plantilla = descripcion_uc_out_df(plantilla)
    # Calculo de la variable BRAR
    plantilla = calculo_BRAR(plantilla)
    # llenado automatico de campos 0 o 1, S o N
    plantilla = diligencia_auto(plantilla)
    # Llenado de data con respecto a información de subestaciones
    plantilla = info_subestaciones(plantilla)
    # Llenado de data con respecto al área especial de las UC's
    plantilla = area_especial(plantilla)
    # llenado de Observaciones en caso de que el campo este vacio
    plantilla = llenado_observaciones(plantilla)
    # LLenado de campo Operación con S.
    plantilla = llenado_operación(plantilla)
    # Llenado del campo Tipo inventario
    plantilla = llenado_tipo_inventario(plantilla)
    # Llenado del campo Salinidad
    plantilla = llenado_salinidad(plantilla)
# =============================================================================
# FIN DE LLENADO DE PLANTILLA
# =============================================================================

    
"""
Guardado de plantilla
"""
direccion = f"D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/2024/4. Seguimiento/4. outputs - Archivos seguimiento/1. Plantillas individuales/{equipo_trabajo}.csv"
plantilla.to_csv(direccion, sep=';', index=False, encoding='utf-8-sig')    
tipo_columna1 = plantilla['Número de conductores'].dtype
#subestaciones = pd.read_csv(ruta_csv, encoding="ISO-8859-1",sep=';',decimal='.', dtype={"IU": str})


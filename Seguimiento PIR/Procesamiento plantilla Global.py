# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 14:11:23 2024

@author: yaboniav
"""

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


#----------------Ubicación del archivo-----------#


folder_path = (f"D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/2024/4. Seguimiento/1. Archivos Excel/3. Consolidado final/Consolidado PIR 2023_versión final.xlsx")
  
#--------------Creación de data frame con todos los campos ------------------# 

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

plantilla = pd.read_excel(folder_path, engine='openpyxl', sheet_name=None, dtype=columns_to_str)
plantilla = pd.concat(plantilla.values(), ignore_index=True)
for sheet_name, df in plantilla.items():
    print(f"Tipos de dato para la hoja: {sheet_name} - ", df.dtypes)
#plantilla[col] = plantilla[col].astype(float)


#-----------------------------------------------------------------------------#


#from llenado_plantilla import seleccionar_equipo_ejecutor

from llenado_plantilla_global import calcular_CR
from llenado_plantilla_global import copiar_FU_PU
from llenado_plantilla_global import llenar_FTR
from llenado_plantilla_global import calcular_IREC
from llenado_plantilla_global import calcular_invr
from llenado_plantilla_global import categoria_df
from llenado_plantilla_global import descripcion_uc_in_df
from llenado_plantilla_global import descripcion_uc_out_df
from llenado_plantilla_global import calculo_BRAR
from llenado_plantilla_global import diligencia_auto
from llenado_plantilla_global import info_subestaciones
from llenado_plantilla_global import area_especial
from llenado_plantilla_global import llenado_observaciones
from llenado_plantilla_global import llenado_operación
from llenado_plantilla_global import llenado_tipo_inventario
from llenado_plantilla_global import llenado_salinidad
if __name__ == "__main__":

    # Llamada a la función y asignación del resultado a una variable
    #equipo_ejecutor_seleccionado = seleccionar_equipo_ejecutor()
    
    # Llenado del campo Equipo Ejecutor
    #plantilla["Equipo Ejecutor"] = equipo_ejecutor_seleccionado
    # Llenado del campo subgerencia Ejecutora
    #plantilla["Subgerencia Ejecutora"] = mapear_subgerencia(equipo_ejecutor_seleccionado)
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
    #plantilla = info_subestaciones(plantilla)
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
direccion = f"D:/OneDrive - Grupo EPM/1. PLANEACIÓN DE INFRAESTRUCTURA/04_PIR/3_Ejecutado/2024/4. Seguimiento/1. Archivos Excel/3. Consolidado final/Consolidado_def.csv"
plantilla.to_csv(direccion, sep=';', index=False, encoding='utf-8-sig')    

#subestaciones = pd.read_csv(ruta_csv, encoding="ISO-8859-1",sep=';',decimal='.', dtype={"IU": str})


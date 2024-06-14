# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:15:10 2024

@author: yaboniav
"""

import requests
import pandas as pd
from io import StringIO
# =============================================================================
# redes desde el Gitech
# =============================================================================
url_lineas = "https://sig.cens.com.co/cens.sig/api/Application/Exportar?layerName=LineaAereaMT&filter=XPOS1%20%3E%3D0"
response = requests.get(url_lineas) # en responder se demora 16 segundos
data = StringIO(response.text)
df_lineas_gitech = pd.read_csv(data, sep=';')
df_lineas_gitech["PHASES_TIPO"] = df_lineas_gitech["PHASES"]
columnas = ["CODE", "PHASES","PHASES_TIPO", "FPARENT", "XPOS1", "YPOS1",
    "XPOS2", "YPOS2", "ELNODE1", "ELNODE2", "CONDUCTOR",
    "LENGTH", "KVNOM", "OWNER", "POBLACION"]
df_lineas_gitech = df_lineas_gitech[columnas]
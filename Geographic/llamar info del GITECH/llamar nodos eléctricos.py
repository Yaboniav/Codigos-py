# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:16:35 2024

@author: yaboniav
"""

import pandas as pd
import requests
from io import StringIO
# =============================================================================
# redes desde el Gitech
# =============================================================================
url_nodoE = "https://sig.cens.com.co/cens.sig/api/Application/Exportar?layerName=NodosElectricosMT&filter=XPOS%20%3E%3D0"

#url_nodoE="C//Users//yaboniav//Downloads//
response = requests.get(url_nodoE) # en responder se demora 16 segundos
data = StringIO(response.text)
df_nodoE_gitech = pd.read_csv(data, sep=';')

columnas = ["CODE", "FPARENT", "XPOS", "YPOS"]
df_nodoE_gitech = df_nodoE_gitech[columnas]

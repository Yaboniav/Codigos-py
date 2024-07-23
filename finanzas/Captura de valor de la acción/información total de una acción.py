# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 01:15:39 2024

@author: yaboniav
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Listado de acciones con sus respectivos símbolos

PDD_Intel = yf.Ticker("INTC")
PDD_Intel=PDD_Intel.info
PDD_Intel #mostramos lo que tiene la variable


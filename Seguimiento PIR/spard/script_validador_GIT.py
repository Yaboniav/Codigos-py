# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 13:00:03 2023

@author: yaboniav
"""

import pandas as pd
import datetime
def validador(plantilla):
    """
    Valida y corrige varias columnas del DataFrame 'plantilla'. 

    :param plantilla: DataFrame de entrada.
    :return: DataFrame corregido y DataFrame con índices y descripción del error o "Sin errores".
        """
#FASES
    # Cargamos el DataFrame con el "Cod Dane" desde la ruta especificada D:\validador\1. información basica - redes - trafos - municipios
    df_dane = pd.read_excel(r'D:/validador/1. información basica - redes - trafos - municipios/cod - regionales.xlsx', engine='openpyxl')
    df_municipio = pd.read_excel(r'D:/validador/1. información basica - redes - trafos - municipios/cod - municipios.xlsx', engine='openpyxl')
    df_UCs = pd.read_excel(r'D:/validador/1. información basica - redes - trafos - municipios/UCs.xlsx', engine='openpyxl')
    subestaciones = pd.read_csv("D:/validador/1. información basica - redes - trafos - municipios/subestaciones.csv", encoding="ISO-8859-1",sep=';',decimal='.', dtype={"IU": str})
    lineas = pd.read_excel("D:/validador/1. información basica - redes - trafos - municipios/líneas.xlsx", engine='openpyxl', dtype={"IUS inicial": str, "IUS final": str}) 
    cod_dane_values = set(df_dane['Cod Dane'])  # Conjunto de valores de "Cod Dane" del archivo Excel para optimizar la búsqueda
    municipio_values = set(df_municipio['MUNICIPIOS'])  # Conjunto de valores de "MUNICIPIOS" para optimizar la búsqueda
    municipio_values_dane = set(df_municipio['CODIGO'])  # Conjunto de valores de "CODIGO" para optimizar la búsqueda
    UCs_values = set(df_UCs['Código UC'])  # Conjunto de valores de "código UC" para optimizar la búsqueda
    resultados = []
    replacements = {1: "I", 2: "II", 3: "III", 4: "IV"}
    """ 
    Arreglo de datos cuando el campo de la columna Unidad Constructiva 
    es DESMANTELADO
    """
    mask = plantilla['Unidad Constructiva'] == "DESMANTELADO"
    
    plantilla.loc[mask, 'Fracción costo'] = 100
    plantilla.loc[mask, 'Porcentaje uso'] = 100
    plantilla.loc[mask, 'Número de conductores'] = 0
    plantilla.loc[mask, 'Cantidad'] = 1
    plantilla.loc[mask, 'RPP'] = 0
    plantilla.loc[mask, 'Concepto UPME'] = 'N'
    plantilla.loc[mask, 'Código FID'] = plantilla.index.astype(str) + plantilla['Número de Fila'].astype(str)
    plantilla.loc[mask, 'Sobrepuesto'] = 'N'
    # Crea una serie booleana para identificar valores duplicados en 'Código FID    
    duplicados_fid = plantilla["Código FID"].duplicated(keep=False)

    for idx, row in plantilla.iterrows():
        descripcion_error = []

        # Validar y corregir 'Año entrada operación'
        if pd.isna(row['Año entrada operación']) or not isinstance(row['Año entrada operación'], (int, float)) or row['Año entrada operación'] != 2023:
            descripcion_error.append("Error en 'Año entrada operación'")
            plantilla.at[idx, 'Año entrada operación'] = 2023
        
        # Validar 'ID proyecto'
        id_proyecto = row['Código proyecto']
        if not isinstance(id_proyecto, str) or not id_proyecto.isalnum() or len(id_proyecto) >= 20:
            descripcion_error.append("Error en 'Código proyecto'")
            
        # Validar 'Nombre de Banco de Proyectos'
        if pd.isna(row['Nombre del proyecto']) or row['Nombre del proyecto'].strip() == '':
            descripcion_error.append("Error en 'Nombre del proyecto'")

        # Validar y corregir 'Tipo Inversión'
        tipo_inversion = row['Tipo inversión']
        if tipo_inversion in replacements:
            plantilla.at[idx, 'Tipo inversión'] = replacements[tipo_inversion]
        elif tipo_inversion not in ["I", "II", "III", "IV"]:
            descripcion_error.append("Error en 'Tipo inversión'")

        # Validar 'IUL'
        iul = row['IUL']
        if pd.isna(iul) or not isinstance(iul, str) or len(iul) != 4:
            descripcion_error.append("Error en 'IUL'")
            
        # Validar 'Nivel de Tensión'
        nivel_tension = row['Nivel']
        if not isinstance(nivel_tension, int) or nivel_tension not in [0, 1, 2, 3, 4]:
            descripcion_error.append("Error en 'Nivel de Tensión'")
        
        # Validar que "Nombre de la Plantilla" y "Nombre de la Plantilla 2" sean iguales
        if row["Nombre de la Plantilla"] != row["Nombre de la Plantilla 2"]:
            descripcion_error.append("Error: Nombre de la Plantilla")

        # Validar que "Cod DANE municipio" en plantilla esté en "Cod Dane" del archivo Excel para validar el dane del municipio
        if row["Cod DANE municipio"] not in municipio_values_dane:
            descripcion_error.append("Error el código dane del municipio")
            
        # Validar que "Municipio" en plantilla esté en "MUNICIPIOS" del archivo Excel
        if row["Municipio"] not in municipio_values:
            descripcion_error.append("Error: El Municipio no existe")

        # Validar que "Unidad Constructiva " en plantilla esté en "Codigo UC" del archivo Excel
        if row["Unidad Constructiva"] not in UCs_values:
            descripcion_error.append("Error: La UC no existe")

        # Validar que "Cod Dane" en plantilla esté en "MUNICIPIOS" del archivo Excel para validar el dane de la regional
        if row["Cod Regional"] not in cod_dane_values:
            descripcion_error.append("Error: El código dane de la regional no existe")
            
        # Extraer el número de fila desde el DataFrame plantilla
        numero_fila = row['Número de Fila']

        # Validar 'Número de conductores'
        numero_conductores = row['Número de conductores']
        if pd.isna(numero_conductores) or numero_conductores not in [0, 1, 2, 3, 4]:
            descripcion_error.append("Error en 'Número de conductores'")
        
        # Validar 'Fracción costo'
        fraccion_costo = row['Fracción costo']
        if pd.isna(fraccion_costo) or not (0 <= fraccion_costo <= 100):
            descripcion_error.append("Error en 'Fracción costo': Debe ser un valor entre 0 y 100.")
        
        # Validar 'Cantidad'
        cantidad_km_unidad = row['Cantidad']           
        if pd.isna(cantidad_km_unidad) or cantidad_km_unidad <= 0:
            descripcion_error.append("Error en 'Cantidad': Debe ser mayor a cero.")
        # Validar que "Código FID" no tenga valores duplicados
        if duplicados_fid[idx]:
            descripcion_error.append("Error en 'Código FID': Valor duplicado.")
            
        # Validar que el campo "DESCRIPCION" no tenga valores vacíos
        descripcion = row['DESCRIPCION']
        if pd.isna(descripcion) or descripcion.strip() == '':
            descripcion_error.append("Error en 'DESCRIPCION': Campo vacío.")
            
        # Validar "Codigo UC_rep" según "Tipo inversión"
        tipo_inversion = row['Tipo inversión']
        codigo_uc_rep = row['Codigo UC_rep']
        
        if tipo_inversion in ["I", "III"]:
            if pd.isna(codigo_uc_rep) or codigo_uc_rep.strip() == '':
                descripcion_error.append("Error: Si 'Tipo inversión' es '{}' el campo 'Codigo UC_rep' no puede estar vacío.".format(tipo_inversion))
                # Validar que "código de UC rep" en plantilla esté en "Codigo UC" del archivo Excel
                if row["Codigo UC_rep"] not in UCs_values:
                    descripcion_error.append("Error: La UC_rep no existe")
                # Validar que "DESCRIPCION_rep" no esté vacío
                descripcion_rep = row['DESCRIPCION_rep']
                if pd.isna(descripcion_rep) or descripcion_rep.strip() == '':
                    descripcion_error.append("Error: El campo 'DESCRIPCION_rep' no puede estar vacío.")
                # Validar que "Cantidad_rep" sea mayor a cero
                cantidad_rep = row['Cantidad_rep']
                # Validar que "Código FID_rep" no esté vacío
                descripcion_rep = row['Código FID_rep']
                # Validar que "DESCRIPCION_rep" no este vacio
                if pd.isna(descripcion_rep) or descripcion_rep.strip() == '':
                    descripcion_error.append("Error: El campo 'DESCRIPCION_rep' no puede estar vacío.")
                # Validar que "cantidad_rep" sea mayor que cero
                if not isinstance(cantidad_rep, (int, float)) or cantidad_rep <= 0:
                    descripcion_error.append("Error: El campo 'Cantidad_rep' debe ser mayor a cero.")
                # Validar que "FASES_rep" contenga los valores 0, 1, 2, 3, o 4
                fases_rep = row['Número de conductores_rep']
                if not isinstance(fases_rep, int) or fases_rep not in [0, 1, 2, 3, 4]:
                    descripcion_error.append("Error: El campo 'FASES_rep' debe tener uno de los valores [0, 1, 2, 3, 4].")
                # Validar que "Año entrada operación_rep" esté entre 1900 y el año actual
                año_actual = datetime.datetime.now().year
                año_entrada_rep = row['Año entrada operación_rep']
                if not isinstance(año_entrada_rep, int) or not (1900 <= año_entrada_rep <= año_actual):
                    descripcion_error.append(f"Error: El campo 'Año entrada operación_rep' debe estar entre 1900 y {año_actual}.")
                # validar que el valor sea 1 o 0
                if row["Rpp_rep"] not in [0, 1]:
                    descripcion_error.append("Error: 'Rpp_rep' debe ser 1 o 0")
                # Validar que el campo marcado corresponda al año en curso
                current_year = datetime.datetime.now().year
                if row["Año salida operación"] != current_year:
                    descripcion_error.append(f"Error: 'Año salida operación' debe ser {current_year}")
        elif tipo_inversion in ["II", "IV"]:
            if not pd.isna(codigo_uc_rep) and codigo_uc_rep.strip() != '':
                descripcion_error.append("Error: Si 'Tipo inversión' es '{}' el campo 'Codigo UC_rep' debe estar vacío.".format(tipo_inversion))
            # Validar que "Codigo UC_rep" esté vacío
            if not pd.isna(row["Codigo UC_rep"]):
                descripcion_error.append("Error: 'Codigo UC_rep' no debe tener valor")
            # Validar que "DESCRIPCION_rep" esté vacío
            if not pd.isna(row["DESCRIPCION_rep"]):
                descripcion_error.append("Error: 'DESCRIPCION_rep' no debe tener valor")
            # Validar que "Cantidad_rep" esté vacío
            if not pd.isna(row["Cantidad_rep"]):
                descripcion_error.append("Error: 'Cantidad_rep' no debe tener valor")
            # Validar que "Código FID_rep" esté vacío
            if not pd.isna(row["Código FID_rep"]):
                descripcion_error.append("Error: 'Código FID_rep' no debe tener valor")
            # Validar que "Número de conductores_rep" esté vacío
            if not pd.isna(row["Número de conductores_rep"]):
                descripcion_error.append("Error: 'Número de conductores_rep' no debe tener valor")
            # Validar que "Año entrada operación_rep" esté vacío
            if not pd.isna(row["Año entrada operación_rep"]):
                descripcion_error.append("Error: 'Año entrada operación_rep' no debe tener valor") 
       
        # validar que el valor sea 1 o 0
        if row["RPP"] not in [0, 1]:
            descripcion_error.append("Error: 'RPP' debe ser 1 o 0")
            
        # Validar que el campo se encuentre dentro del listado de subestaciones el cual corresponde a un archivo en csv en la columna US            
        if row["IUS"] not in subestaciones["IU"].tolist():
            descripcion_error.append("Error: 'IUS' no se encuentra en la lista de subestaciones")

        # Validar que el campo se encuentre dentro del archivo en excel en la columna "código de línea"
        if row["Código línea"] not in lineas["Código línea"].tolist():
            descripcion_error.append("Error: 'Código línea' no se encuentra en la lista de líneas")
        
        # validar que el campo no este vacio   
        if pd.isna(row["Concepto UPME"]):
            descripcion_error.append("Error: 'Concepto UPME' no debe estar vacío")
        
        # validar que el campo se encuentre dentro del archivo en excel en la columna "IU"
        if row["IUS final"] not in subestaciones["IU"].tolist():
            if row["IUS final"] not in ["0"]:
                descripcion_error.append("Error: 'IUS final' no se encuentra en la lista de subestaciones")
        
        # validar que el campo se encuentre dentro del archivo en excel en la columna "IU"
        if row["IUS inicial"] not in subestaciones["IU"].tolist():
            descripcion_error.append("Error: 'IUS inicial' no se encuentra en la lista de subestaciones")
            
        # validar que el campo no este vacio y tenga unicamente los caracteres S o N    
        if not row["PIEC"] or row["PIEC"] not in ["S", "N"]:
            descripcion_error.append("Error: 'PIEC' debe ser 'S' o 'N'")
            
        # validar que sea un numero mayor de 0 y menor o igual a 100
        if not (0 < row["Porcentaje uso"] <= 100):
            descripcion_error.append("Error: 'Porcentaje uso' debe ser mayor a 0 y menor o igual a 100")
        
        # validar que el campo no este vacio y tenga unicamente los caracteres S o N
        if not row["Sobrepuesto"] or row["Sobrepuesto"] not in ["S", "N"]:
            descripcion_error.append("Error: 'Sobrepuesto' debe ser 'S' o 'N'")
        
        # validar que el campo no este vacio y tenga unicamente los caracteres S o N
        if not row["STR construcción"] or row["STR construcción"] not in ["S", "N"]:
            descripcion_error.append("Error: 'STR construcción' debe ser 'S' o 'N'")
        
        # Validar "Tensión de operación" con respecto a "Nivel"
        nivel = row["Nivel"]
        tension = row["Tensión de operación"]
        uc = row["Unidad Constructiva"]
        if uc in ["N4L93", "N4L94", "N4L52"]:
            if tension != 0:
                descripcion_error.append("Error: 'Tensión de operación' debe ser 0 para 'Unidad Constructiva' N4L93, N4L94, N4L52")
        elif nivel == 2:
            if not (1 <= tension < 20):
                descripcion_error.append("Error: Para 'Nivel' 2, 'Tensión de operación' debe estar entre 1 y 20")
        elif nivel == 3:
            if not (30 <= tension < 57.5):
                descripcion_error.append("Error: Para 'Nivel' 3, 'Tensión de operación' debe estar entre 30 y 57.5")
        elif nivel == 4:
            if not (57.5 <= tension < 220):
                descripcion_error.append("Error: Para 'Nivel' 4, 'Tensión de operación' debe estar entre 57.5 y 220")
        
        # validar que el campo no este vacio y sus valores sean 1 o 0
        if row["Activo Construido y en Operación"] not in [0, 1]:
            descripcion_error.append("Error: 'Activo Construido y en Operación' debe ser 0 o 1")
        # validar que este campo no este vacio y sus valores deben ser 1, 2, 3, 4, 5
        if row["Tipo de Proyecto"] not in [1, 2, 3, 4, 5] or pd.isna(row["Tipo de Proyecto"]):
            descripcion_error.append("Error: 'Tipo de Proyecto' debe ser uno de los siguientes valores: 1, 2, 3, 4, 5")

        # Agregar resultados, incluyendo el número de fila
        if descripcion_error:
            resultados.append((numero_fila, row["Nombre de la Plantilla 2"], row["Hoja archivo"], ", ".join(descripcion_error)))
        else:
            resultados.append((numero_fila, row["Nombre de la Plantilla 2"], row["Hoja archivo"], "Sin errores"))

    # Incluye el número de fila en el DataFrame de resultados
    df_resultados = pd.DataFrame(resultados, columns=["Número de Fila", "Nombre de la Plantilla 2", "Hoja archivo", "Descripción del Error"])
    return plantilla, df_resultados
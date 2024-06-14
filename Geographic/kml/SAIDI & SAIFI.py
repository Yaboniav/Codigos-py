import pandas as pd
import os
from pyxlsb import open_workbook as open_xlsb

def read_xlsb(file_path, sheet_name, headers=None):
    with open_xlsb(file_path) as wb:
        with wb.get_sheet(sheet_name) as sheet:
            if headers is None:
                headers = [item.v for item in next(sheet.rows())]  # Leer la primera fila como encabezados
            data = [[item.v for item in row] for row in sheet.rows()]
            # Solo los primeros 100 registros
            return pd.DataFrame(data[:100], columns=headers)

# Establecer el directorio donde se encuentran los archivos Excel
path = 'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//3. Calidad del servicio//1. DB//2020'

# Nombre de la hoja que deseas cargar
sheet_name = "Exportar Hoja de Trabajo"

all_dfs = []
headers = None  # Inicializar encabezados como None

for filename in os.listdir(path):
    file_path = os.path.join(path, filename)

    try:
        if filename.endswith(('.xlsx', '.xls')):
            if headers is None:
                df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                headers = df.columns.tolist()
                # Añadir la columna del nombre del archivo
                df['Source File'] = filename
            else:
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1, names=headers, engine='openpyxl')
                df['Source File'] = filename
            # Solo los primeros 100 registros
            df = df.head(100)
        elif filename.endswith('.xlsb'):
            df = read_xlsb(file_path, sheet_name, headers)
            if headers is None:
                headers = df.columns.tolist()
            df['Source File'] = filename
        else:
            continue

        all_dfs.append(df)
        print(f"El archivo {filename} fue cargado exitosamente!")

    except Exception as e:
        print(f"Error al cargar el archivo {filename}. Detalle del error: {str(e)}")
        
final_df = pd.concat(all_dfs, ignore_index=True)

# Eliminar comas y saltos de línea en todas las columnas
for col in final_df.columns:
    if final_df[col].dtype == 'object':
        final_df[col] = final_df[col].str.replace(',', '').str.replace('\n', '')

csv_filename = "D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//3. Calidad del servicio//2. compilado Calidad//2020.csv"
final_df.to_csv(csv_filename, sep=';', decimal='.', index=False, encoding='utf-8-sig')
print(f"¡El DataFrame se ha guardado exitosamente en {csv_filename}!")
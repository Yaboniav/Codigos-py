import pandas as pd
import os
from pyxlsb import open_workbook as open_xlsb

# Crear el DataFrame vacío con los nuevos encabezados específicos
headers = [
    "FDD_CODIGOEVENTO", "FDD_FINICIAL", "FDD_FFINAL", "FDD_DURACION", "FDD_CODIGOELEMENTO",
    "LONGITUD", "LATITUD", "BREAKER", "USUARIOS_UI", "FDD_UIXTI", "FPARENT",
    "MUND_DESCRIPCION", "MUND_REGIONAL", "FDD_CAUSA", "DETALLE_CAUSA", "FDD_CAUSA_CREG",
    "FDD_CAUSA_SSPD", "FDD_EXCLUSION", "FDD_TIPOCARGA", "FDD_CONTINUIDAD", "FDD_USUARIOAP",
    "FDD_AJUSTADO", "FDD_TIPOAJUSTE", "FDD_RADICADO", "FDD_APROBADO", "OBJETIVO_INI",
    "DESCRIPCION_CAUSA_CREG"
]

df_finish = pd.DataFrame(columns=headers)

def read_xlsb(file_path, sheet_name, cols):
    with open_xlsb(file_path) as wb:
        with wb.get_sheet(sheet_name) as sheet:
            data = []
            for i, row in enumerate(sheet.rows()):
                if i == 0:
                    file_headers = [item.v for item in row]
                    header_mapping = {file_headers.index(h): h for h in cols if h in file_headers}
                else:
                    row_data = [item.v for item in row]
                    data.append([row_data[j] for j in header_mapping.keys()])
            return pd.DataFrame(data, columns=header_mapping.values())

def get_month_from_filename(filename):
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    month_number = filename[:2]  # Extraer los primeros dos caracteres
    if month_number.isdigit():
        return months[int(month_number) - 1]
    return 'Mes Desconocido'

path = 'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//3. Calidad del servicio//1. DB//2019'
sheet_name = "Exportar Hoja de Trabajo"

for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    try:
        if filename.endswith('.xlsb'):
            df = read_xlsb(file_path, sheet_name, headers)
        elif filename.endswith(('.xlsx', '.xls')):
            df_temp = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', nrows=1)
            file_headers = df_temp.columns.tolist()
            header_mapping = {file_headers.index(h): h for h in headers if h in file_headers}
            df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1, engine='openpyxl', usecols=header_mapping.keys())
            df.columns = header_mapping.values()
        df['NOMBRE DEL LIBRO'] = os.path.splitext(filename)[0]
        df_finish = pd.concat([df_finish, df], ignore_index=True)
        print(f"El archivo {filename} fue cargado exitosamente!")
    except Exception as e:
        print(f"Error al cargar el archivo {filename}. Detalle del error: {str(e)}")

# 1. Después de concatenar todos los archivos, asignar el mes basado en 'NOMBRE DEL LIBRO'
df_finish['NOMBRE_MES'] = df_finish['NOMBRE DEL LIBRO'].apply(get_month_from_filename)

# 2. Agregar una columna adicional llamada UI_MES con los mismos datos de USUARIOS_UI
df_finish['UI_MES'] = df_finish['USUARIOS_UI']

# 3. Cambiar el título de la columna USUARIOS_UI por USUARIOS_TAFO
df_finish.rename(columns={'USUARIOS_UI': 'USUARIOS_TAFO'}, inplace=True)

# 4. Agregar la columna del año

df_finish['AÑO'] = 2019

# 5. Cambiar el título de la columna USUARIOS_UI por USUARIOS_TAFO
df_finish.rename(columns={'USUARIOS_UI': 'USUARIOS_TAFO'}, inplace=True)

# 6. Obtener Descripción de causas CREG


ruta_causas_creg = 'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//3. Calidad del servicio//causas CREG.xlsx'
df_causaCREG = pd.read_excel(ruta_causas_creg)

df_finish = df_finish.merge(df_causaCREG, left_on='FDD_CAUSA_CREG', right_on='FDC_CAUSA_015', how='left')

df_finish.drop(columns=['FDC_CAUSA_015'], inplace=True)  # Omitir esta línea si deseas mantener la columna original
df_finish.drop(columns=['DESCRIPCION_CAUSA_CREG'], inplace=True)  # Omitir esta línea si deseas mantener la columna original
df_finish.rename(columns={'FDC_DESCRIPCION': 'DESCRIPCION_CAUSA_CREG'}, inplace=True)
# Guardar el DataFrame final
csv_filename = "D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//3. Calidad del servicio//2. compilado Calidad//2019.csv"
df_finish.to_csv(csv_filename, sep=';', decimal='.', index=False, encoding='utf-8-sig')
print(f"¡El DataFrame se ha guardado exitosamente en {csv_filename}!")
import pandas as pd
import osmnx as ox
import networkx as nx
import folium
import pyproj
import simplekml
from openpyxl import load_workbook
from pyproj import Proj, Transformer

# 1. Leer los datos de Excel y CSV
df_reposiciones = pd.read_excel('D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//2. Insumos Exp - Rep//1. Reposiciones para habilitar enlaces//Nodos Eléctricos.xlsx', engine='openpyxl')
df_nodosE = pd.read_csv('D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//2. Insumos Exp - Rep//1. Reposiciones para habilitar enlaces//MVELNODE.csv', sep=';')
columnas = ["CODE", "FPARENT", "XPOS", "YPOS"]
df_nodosE = df_nodosE[columnas]

# función de conversión de coordenadas
def convertir_a_coordenadas_decimales(dataframe, x_col, y_col):
    proj_custom = "+proj=tmerc +lat_0=4.596200416666666 +lon_0=-74.07750791666666 +k=1 +x_0=1000000 +y_0=1000000 +ellps=GRS80 +units=m +no_defs"
    proj_latlon = "EPSG:4326"
    transformer = Transformer.from_crs(proj_custom, proj_latlon)
    x = dataframe[x_col]
    y = dataframe[y_col]
    lat, lon = transformer.transform(x, y)
    dataframe[x_col] = lat
    dataframe[y_col] = lon
    return dataframe
df_nodosE = convertir_a_coordenadas_decimales(df_nodosE, 'XPOS', 'YPOS')

# Asignar coordenadas a df_reposiciones
df_nodosE.rename(columns={'XPOS': 'LAT', 'YPOS': 'LON'}, inplace=True)
df_reposiciones = df_reposiciones.merge(df_nodosE[['CODE', 'LAT', 'LON', 'FPARENT']], left_on='Nodo Inicial', right_on='CODE', how='left').rename(columns={'LAT': 'LAT_Inicial', 'LON': 'LON_Inicial', 'FPARENT': 'Alimentador'})
df_reposiciones = df_reposiciones.merge(df_nodosE[['CODE', 'LAT', 'LON']], left_on='Nodo final', right_on='CODE', how='left').rename(columns={'LAT': 'LAT_final', 'LON': 'LON_final'})
df_reposiciones = df_reposiciones.drop(columns=['CODE_x', 'CODE_y'])

# Crear archivo KML
kml = simplekml.Kml()
folders = {}

def calculate_and_add_route_to_kml(lat1, lon1, lat2, lon2, alimentador, item, nodo_inicial, nodo_final):
    route_length = None  # Asegúrate de inicializar estas variables fuera del try
    route_map = None
    try:
        G = ox.graph_from_point((lat1, lon1), dist=3000, network_type='walk')
        orig_node = ox.distance.nearest_nodes(G, lon1, lat1)
        dest_node = ox.distance.nearest_nodes(G, lon2, lat2)
        route = nx.shortest_path(G, orig_node, dest_node, weight='length')
        route_length = nx.shortest_path_length(G, orig_node, dest_node, weight='length') / 1000

        # Añadir la ruta al KML
        route_name = f"{item} {alimentador}"
        #description = f"Alimentador: {alimentador}, Nodo Inicial: {nodo_inicial}, Nodo Final: {nodo_final}, Longitud de Ruta: {route_length} km"
        description = f"Alimentador: {alimentador}<br>Nodo Inicial: {nodo_inicial}<br>Nodo Final: {nodo_final}<br>Longitud de Ruta: {route_length} km"
        coords = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in route]
        if alimentador not in folders:
            folders[alimentador] = kml.newfolder(name=alimentador)
        linestring = folders[alimentador].newlinestring(name=route_name, description=description, coords=coords)
        #linestring = kml.newlinestring(name="Route", coords=coords)
        route_map = folium.Map(location=[lat1, lon1], zoom_start=13)
        folium.PolyLine([(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]).add_to(route_map)
        
        
    except Exception as e:
        print(f"Error during route calculation: {e}")
    return route_length, route_map
# =============================================================================
# # Ejemplo de uso
#lat1, lon1 = 6.25184, -75.56359  # Ejemplo de coordenadas en Medellín, Colombia
#lat2, lon2 = 6.255, -75.564  # Otro punto en Medellín
#calculate_and_add_route_to_kml(lat1, lon1, lat2, lon2)
# =============================================================================

# Calcular las rutas y añadirlas al KML
#df_reposiciones = df_reposiciones.iloc[:10]
df_reposiciones['Route Length (km)'] = df_reposiciones.apply(lambda row: calculate_and_add_route_to_kml(row['LAT_Inicial'], row['LON_Inicial'], row['LAT_final'], row['LON_final'], row['Alimentador'], row['item'], row['Nodo Inicial'], row['Nodo final'])[0], axis=1)

# Guardar los resultados y crear archivo KML

ruta_salida = f'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//2. Insumos Exp - Rep//1. Reposiciones para habilitar enlaces//ruta_salida.xlsx'
ruta_kml = f'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//2. Insumos Exp - Rep//1. Reposiciones para habilitar enlaces//kml//rutas.kml'
df_reposiciones.to_excel(ruta_salida, index=False)
kml.save(ruta_kml)
# Crear un archivo HTML
for index, row in df_reposiciones.iterrows():
    route_map = calculate_and_add_route_to_kml(row['LAT_Inicial'], row['LON_Inicial'], row['LAT_final'], row['LON_final'], row['Alimentador'], row['item'], row['Nodo Inicial'], row['Nodo final'])[1]
    if route_map:  # Comprueba si route_map no es None
        # Usar el valor de la columna 'Nodo Inicial' como nombre de archivo
        filename = f'D://OneDrive - Grupo EPM//3. CENS//0. PIE - PIR - PF//2. Insumos Exp - Rep//1. Reposiciones para habilitar enlaces//Html//{row["Nodo Inicial"]}.html'
        route_map.save(filename)  # Guardar como HTML
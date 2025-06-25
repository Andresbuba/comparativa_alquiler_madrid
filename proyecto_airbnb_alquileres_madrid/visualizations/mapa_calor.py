import folium 
import folium.map
from folium.plugins import HeatMap
import os

def generar_mapa_de_calor(df):
    """
    Crea un mapa de calor basado en rentabilidad relativa si hay columnas 'lat' y 'lon'.
    """
    print('\n Mapa de calor')

    if 'lat' not in df.columns or 'lon' not in df.columns:
        print('EL dataframe no contiene cordenadas')
        return

    df = df.dropna(subset=['lat', 'lon', 'rentabilidad_relativa'])

    m = folium.Map(location=[40.4168, -3.7038], zoom_start=11)
    heat_data = [[row['lat'], row['lon'], row['rentabilidad_relativa']] for _, row in df.iterrows()]
    HeatMap(heat_data).add_to(m)
    m.save('visualizations/outputs/mapa_calor.html')
    print("Mapa guardado como mapa_calor.html")

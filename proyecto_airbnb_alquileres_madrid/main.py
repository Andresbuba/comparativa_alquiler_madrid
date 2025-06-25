from scripts.unir_datasets import unir_y_calcular_rentabilidad
from scripts.exportar_resultado import exportar_resultado
from visualizations.graficos import generar_graficos
from visualizations.mapa_calor import generar_mapa_de_calor
from scripts.limpiar_airbnb import limpiar_y_agrupar_airbnb
from scripts.limpiar_convencional import limpiar_datos_convencional
from scripts.load_data import cargar_datos
import pandas as pd

# ==========================
#   CARGA DE DATOS
# ==========================
df_airbnb_raw, df_alquiler_raw = cargar_datos()

df_airbnb_raw.columns = df_airbnb_raw.columns.str.strip()
df_alquiler_raw.columns = df_alquiler_raw.columns.str.strip()

# ==========================
#   LIMPIEZA Y TRANSFORMACIÓN
# ==========================
df_airbnb = limpiar_y_agrupar_airbnb(df_airbnb_raw)
df_alquiler = limpiar_datos_convencional(df_alquiler_raw)

# ==========================
#   COMPARACIÓN DE LOCALIZACIONES
# ==========================
print("\n[COMPARACIÓN] Localizaciones comunes:")
coincidencias = set(df_airbnb['localizacion']) & set(df_alquiler['localizacion'])
print(sorted(coincidencias))

# ==========================
#   UNIÓN Y RENTABILIDAD
# ==========================
df_final = unir_y_calcular_rentabilidad(df_airbnb, df_alquiler)

# ==========================
#   ENRIQUECIMIENTO CON COORDENADAS
# ==========================
print("\n[ENRIQUECIMIENTO CON COORDENADAS]")

if 'latitude' in df_airbnb_raw.columns and 'longitude' in df_airbnb_raw.columns:
    df_coords = df_airbnb_raw[['neighbourhood_cleansed', 'latitude', 'longitude']].copy()
    df_coords['localizacion'] = df_coords['neighbourhood_cleansed'].str.lower().str.strip()
    df_coords = df_coords.groupby('localizacion').agg({'latitude': 'mean', 'longitude': 'mean'}).reset_index()
    df_coords.columns = ['localizacion', 'lat', 'lon']

    # Asegura que 'localizacion' esté normalizada en df_final
    df_final['localizacion'] = df_final['localizacion'].str.lower().str.strip()

    # Elimina columnas previas para evitar sufijos
    df_final = df_final.drop(columns=[col for col in df_final.columns if col in ['lat', 'lon']], errors='ignore')

    # Realiza el merge limpio
    df_final = pd.merge(df_final, df_coords, on='localizacion', how='left')

    print("\n[DEPURACIÓN] Columnas tras el merge:", df_final.columns.tolist())

    if 'lat' in df_final.columns and 'lon' in df_final.columns:
        print("\n[DEPURACIÓN] Primeras filas con coordenadas:")
        print(df_final[['localizacion', 'lat', 'lon']].dropna().head())
    else:
        print("[ERROR] No se añadieron las columnas lat y lon.")
else:
    print("[ERROR] El dataset de Airbnb no contiene columnas de coordenadas.")

# ==========================
#   EXPORTACIÓN DE DATOS
# ==========================
exportar_resultado(df_final)

# ==========================
#   VISUALIZACIONES
# ==========================
generar_graficos(df_final)
generar_mapa_de_calor(df_final)

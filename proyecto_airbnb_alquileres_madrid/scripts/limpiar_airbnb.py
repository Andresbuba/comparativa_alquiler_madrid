import pandas as pd

def limpiar_y_agrupar_airbnb(df_airbnb):
    """
    Limpia y transforma datos de Airbnb:
    - Filtra columnas necesarias
    - Limpia precios
    - Convierte a metros
    - Agrupa por barrio
    """
    print("\n[LIMPIEZA Y AGRUPACIÓN AIRBNB]")

    columnas = ['neighbourhood_cleansed', 'price']
    if 'square_feet' in df_airbnb.columns:
        columnas.append('square_feet')

    df = df_airbnb[columnas].copy()
    df = df.dropna(subset=['neighbourhood_cleansed', 'price'])

    df['price'] = df['price'].replace('[\\$,]', '', regex=True).astype(float)
    df['square_meters'] = df.get('square_feet', 0) * 0.092903

    agrupado = df.groupby('neighbourhood_cleansed').agg({
        'price': 'mean',
        'square_meters': 'mean'
    }).reset_index()

    agrupado['precio_m2_airbnb'] = agrupado['price'] / agrupado['square_meters']
    # Crear columna 'localizacion' para empatar con el dataset convencional
    agrupado['localizacion'] = agrupado['neighbourhood_cleansed'].str.lower().str.strip()
    return agrupado

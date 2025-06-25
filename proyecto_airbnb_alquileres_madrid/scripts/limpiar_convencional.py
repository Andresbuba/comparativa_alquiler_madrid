import pandas as pd

def limpiar_datos_convencional(df_alquiler):
    'Limpia datos del alquiler convencional'

    print('Limpieza alquiler convencional')

    df = df_alquiler.copy()
    df['localizacion']=df['localizacion'].str.lower().str.strip()
    df['precio_m2_convencional'] = pd.to_numeric(df['precio_m2_convencional'], errors='coerce')
    df = df.dropna(subset=['precio_m2_convencional'])
    return df
import pandas as pd
import os


def cargar_datos():
    """
    Carga y valida los archivos listings.csv y alquiler_convencional_madrid.csv
    """
    print('\n Cargar datos')
    ruta_airbnb = 'data/raw/listings.csv'
    ruta_convencional = 'data/raw/alquiler_convencional_madrid.csv'

    if not os.path.exists(ruta_airbnb):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_airbnb}")
    if not os.path.exists(ruta_convencional):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_convencional}")

    # Carga sin transformar
    df_airbnb_raw = pd.read_csv(ruta_airbnb)
    df_alquiler_raw = pd.read_csv(ruta_convencional)

    # Limpia espacios en columnas (por si acaso)
    df_airbnb_raw.columns = df_airbnb_raw.columns.str.strip()
    df_alquiler_raw.columns = df_alquiler_raw.columns.str.strip()

    # Muestra forma para depuración
    print(f"\n[CARGA DE DATOS]")
    print(f"Airbnb cargado: {df_airbnb_raw.shape}")
    print(f"Alquiler convencional cargado: {df_alquiler_raw.shape}")

    return df_airbnb_raw, df_alquiler_raw
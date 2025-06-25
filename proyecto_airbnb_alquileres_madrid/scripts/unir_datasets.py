import pandas as pd

def unir_y_calcular_rentabilidad(df_airbnb_grouped, df_convencional):
    """
    Une datasets y calcula rentabilidad relativa entre Airbnb y alquiler tradicional.
    """
    print("\n[UNIÓN Y RENTABILIDAD]")

    df_airbnb_grouped['localizacion']= df_airbnb_grouped['neighbourhood_cleansed'].str.lower().str.strip()
    df = pd.merge(df_airbnb_grouped, df_convencional, on='localizacion', how='inner')

    df['rentabilidad_relativa'] = (
        (df['precio_m2_airbnb'] - df['precio_m2_convencional'] )/ df['precio_m2_convencional']
    )
    return df
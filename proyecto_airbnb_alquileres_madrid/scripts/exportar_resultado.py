import os

def exportar_resultado(df):
    '''
    Exporta los resultados analizados en un archivo csv
    '''

    print('\n Exportacion')

    os.makedirs('data/processed', exist_ok=True)
    ruta_salida = 'data/processed/datos_rentabilidad.csv'
    df.to_csv(ruta_salida, index=False)
    print(f'\n Archivo guardado {ruta_salida}')
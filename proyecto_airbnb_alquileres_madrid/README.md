Proyecto Análisis de Rentabilidad Airbnb vs Alquiler Convencional en Madrid

Este proyecto tiene como objetivo analizar y comparar la rentabilidad de los alquileres de viviendas turísticas en Airbnb frente a los alquileres convencionales en la Comunidad de Madrid. El análisis se realiza a partir de datasets obtenidos de fuentes abiertas en el caso de airbnb y en el caso de los alquileres convencionales son aproximados, tambien se visualizan los resultados mediante gráficos y un mapa de calor.

proyecto_airbnb_alquileres_madrid/
|│
|├── data/
| |
| ├── raw/ # Datos originales
| | |
| | ├── listings.csv # Datos de Airbnb
| | ├── alquiler_convencional.csv # Datos de alquiler convencional
| | └── coords_madrid.csv # Coordenadas de barrios
| |
| └── processed/ # Datos procesados (exportados)
| └── datos_rentabilidad.csv
|
|├── scripts/
| |
| ├── load_data.py # Carga de datos
| ├── limpiar_airbnb.py # Limpieza de Airbnb
| ├── limpiar_convencional.py # Limpieza de alquiler convencional
| ├── unir_datasets.py # Cálculo de rentabilidad
| └── exportar_resultado.py # Exportación a CSV
|
|├── visualizations/
| |
| ├── graficos.py # Gráficos de barras
| ├── mapa_calor.py # Mapa de calor (Folium)
| └── outputs/ # Resultados visuales
|
└── main.py # Script principal

---REQUISITOS---

Pandas

Seaborn

Matplotlib

Folium

---EJECUCION DEL PROYECTO---

Archivo principal:

main.py

Ejecuta esto:

Carga y limpia los datos.

Calcula la rentabilidad.

Exporta el resultado a data/processed/datos_rentabilidad.csv

Genera:

Un gráfico de barras comparando precios por m2.

Un gráfico de barras con rentabilidad relativa.

Un mapa de calor en visualizations/outputs/mapa_calor.html

---EXPLICACION PASO POR PASO DEL ARCHIVO main.py---

from scripts.unir_datasets import unir_y_calcular_rentabilidad
from scripts.exportar_resultado import exportar_resultado
from visualizations.graficos import generar_graficos
from visualizations.mapa_calor import generar_mapa_de_calor
from scripts.limpiar_airbnb import limpiar_y_agrupar_airbnb
from scripts.limpiar_convencional import limpiar_datos_convencional
from scripts.load_data import cargar_datos
import pandas as pd

IMPORTACIONES: Se cargan funciones externas necesarias para limpiar, unir, visualizar y exportar datos.

df_airbnb_raw, df_alquiler_raw = cargar_datos()
df_airbnb_raw.columns = df_airbnb_raw.columns.str.strip()
df_alquiler_raw.columns = df_alquiler_raw.columns.str.strip()

(cargar_datos(): lee listings.csv y alquiler_convencional.csv.
.str.strip(): elimina espacios en los nombres de columnas por si vinieran mal formateados.)

df_airbnb = limpiar_y_agrupar_airbnb(df_airbnb_raw)
df_alquiler = limpiar_datos_convencional(df_alquiler_raw)

(Se aplican funciones de limpieza personalizadas:
Airbnb: agrega por barrio y calcula medias.
Convencional: filtra y estandariza precios.)

coincidencias = set(df_airbnb['localizacion']) & set(df_alquiler['localizacion'])
print(sorted(coincidencias))

(Se imprimen las coincidencias de de ambos datasets)

df_final = unir_y_calcular_rentabilidad(df_airbnb, df_alquiler)

(Se unen ambos datasets por barrio y se calcula la rentabilidad relativa:
rentabilidad = (precio_m2_airbnb / precio_m2_convencional))'

Enriquecimiento de coordenadas lat/lon
Este bloque busca añadir coordenadas promedio por barrio desde las columnas de Airbnb
Se normaliza el nombre de barrio.
Se agrupan latitudes y longitudes por nombre de barrio (localizacion).
Se hace merge con el df_final para agregar lat y lon.

if 'latitude' in df_airbnb_raw.columns and 'longitude' in df_airbnb_raw.columns:
(Comprueba que el dataset df_airbnb_raw contiene las columnas latitude y longitude.)

df_coords = df_airbnb_raw[['neighbourhood_cleansed', 'latitude', 'longitude']].copy()
( Crea una copia del DataFrame con solo las columnas necesarias para generar las coordenadas: el barrio (neighbourhood_cleansed), la latitud y la longitud.)

df_coords['localizacion'] = df_coords['neighbourhood_cleansed'].str.lower().str.strip()
(Crea una columna con los nombres de la localizacion en minusculas y sin espacios)

df_coords = df_coords.groupby('localizacion').agg({'latitude': 'mean', 'longitude': 'mean'}).reset_index()
(Agrupa los datos por barrio y crea una media de latitud y longitud de cada uno)

df_coords.columns = ['localizacion', 'lat', 'lon']
(Renombra las columnas para que tengan nombres mas claros)

df_final['localizacion'] = df_final['localizacion'].str.lower().str.strip()
df_coords['localizacion'] = df_coords['localizacion'].str.lower().str.strip()
(Asegura que ambas tablas df_final y df_coords tengan la columna localizacion estandar antes del merge)

df_final = pd.merge(df_final, df_coords, on='localizacion', how='left')
(Une ambos DataFrame aa df_final por columna localizacion y añadiento las columnas lat y lon)

if 'lat' in df_final.columns and 'lon' in df_final.columns:
print("[DEPURACIÓN] Coordenadas añadidas:")
print(df_final[['localizacion', 'lat', 'lon']].dropna().head())
( Comprueba que el merge ha funcionado y que las coordenadas están presentes. Imprime una muestra por consola.)

    else:
        print("[ERROR] No se añadieron las columnas lat y lon.")

else:
print("[ERROR] El dataset de Airbnb no contiene columnas de coordenadas.")
(Muestra errores claros si no se añaden las columnas lat y lon, o si faltan desde el principio.)

exportar_resultado(df_final)

(Se guarda el archivo final en data/processed/datos_rentabilidad.csv)

generar_graficos(df_final)
generar_mapa_de_calor(df_final)

Se generan dos graficos de barras(graficos.py) y un mapa de calor con Folium (mapa_calor.py)

RESULTADO FINAL:

Archivo CSV con datos finales.

Gráficos PNG con comparativas de precios y rentabilidad.

Un mapa de calor HTML geolocalizado por barrio.

Autor: Andrés Sánchez fernández(Proyecto Máster Conquer Blocks)

import matplotlib.pyplot as plt
import seaborn as sns
import os 
from matplotlib.ticker import FuncFormatter

def generar_graficos(df):
    """
    Crea dos gráficos:
    1. Comparativa de precio por m²
    2. Rentabilidad relativa
    """

    print('\n Creando graficos...')



    os.makedirs('visualizations/outputs', exist_ok=True)
    df = df.sort_values(by='rentabilidad_relativa', ascending=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(x='localizacion', y='precio_m2_airbnb', data=df, label='Airbnb', color='skyblue')
    sns.barplot(x='localizacion', y='precio_m2_convencional', data=df, label='Convencional', color='salmon', alpha=0.7)
    plt.xticks(rotation=90)
    plt.legend()
    euro_formatter = FuncFormatter(lambda x, pos: f'{x:.0f} €')
    plt.ylabel('Precio por metro cuadrado')
    plt.gca().yaxis.set_major_formatter(euro_formatter)
    plt.tight_layout()
    plt.savefig('visualizations/outputs/comparativa_precios_m2.png')
    plt.show()
    plt.close()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='localizacion', y='rentabilidad_relativa', data=df, palette='viridis')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('visualizations/outputs/rentabilidad_relativa.png')
    plt.show
    plt.close()

    print(" Gráficos guardados.")

    
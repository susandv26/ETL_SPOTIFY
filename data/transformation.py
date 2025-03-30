# data/transformation.py
import pandas as pd

def convertir_columna_a_minuscula(df, columna):
    if columna in df.columns:
        df[columna] = df[columna].astype(str).str.lower()
    return df

def convertir_columna_a_mayuscula(df, columna):
    if columna in df.columns:
        df[columna] = df[columna].astype(str).str.upper()
    return df

def extraer_parte_fecha(df, columna, parte):
    if columna in df.columns:
        df[columna] = pd.to_datetime(df[columna], errors='coerce')
        if parte == 'mes':
            df[columna] = df[columna].dt.month
        elif parte == 'dia':
            df[columna] = df[columna].dt.day
        elif parte == 'anio':
            df[columna] = df[columna].dt.year
        elif parte == 'hora':
            df[columna] = df[columna].dt.hour
    return df

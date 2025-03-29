# Función para convertir valores de un campo a minúscula
def convertir_a_minuscula(df):
    return df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Función para convertir valores de un campo a mayúscula
def convertir_a_mayuscula(df):
    return df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# Función para extraer partes de una fecha/hora
def extraer_fecha(df):
    for column in df.columns:
        if pd.to_datetime(df[column], errors='coerce').notnull().any():
            df[column] = pd.to_datetime(df[column], errors='coerce').dt.date
    return df
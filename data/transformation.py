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

def concatenar_columnas(df):
    print("\nSeleccione columnas para concatenar (separadas por coma, ej: 1,2):")
    for i, col in enumerate(df.columns):
        print(f"{i}. {col}")

    seleccion = input("Ingrese los números: ")
    try:
        indices = [int(i.strip()) for i in seleccion.split(",")]
        columnas = [df.columns[i] for i in indices if 0 <= i < len(df.columns)]
    except Exception as e:
        print(f"❌ Entrada inválida: {e}")
        return df

    if len(columnas) < 2:
        print("⚠️ Debe seleccionar al menos dos columnas.")
        return df

    delimitador = input("Ingrese el delimitador entre campos (ENTER para usar espacio): ")
    if delimitador.strip() == "":
        delimitador = " "

    nuevo_nombre = input("Nombre para la nueva columna concatenada (ENTER para usar por defecto): ")
    if not nuevo_nombre.strip():
        nuevo_nombre = "_".join(columnas) + "_concat"

    # Concatenar columnas con delimitador
    df[nuevo_nombre] = df[columnas].astype(str).agg(delimitador.join, axis=1)

    eliminar = input("¿Desea eliminar las columnas originales? (si/no): ").strip().lower()
    if eliminar == 'si':
        df.drop(columns=columnas, inplace=True)

    print(f"✅ Campos {columnas} concatenados en '{nuevo_nombre}' con delimitador '{delimitador}'")
    return df
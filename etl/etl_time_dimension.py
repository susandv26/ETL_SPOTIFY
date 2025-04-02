import pandas as pd

def generar_dim_tiempo(df, columna_fecha):
    if columna_fecha not in df.columns:
        print("❌ Columna no encontrada.")
        return pd.DataFrame()

    print("\n📅 Formato de la fecha (ejemplo: %d/%m/%Y, %Y-%m-%d, etc.)")
    formato = input("Ingrese el formato de la fecha: ").strip()

    try:
        df[columna_fecha] = pd.to_datetime(df[columna_fecha], format=formato, errors='coerce')
    except Exception as e:
        print("❌ Error al interpretar la fecha con el formato proporcionado:")
        print(e)
        return pd.DataFrame()

    # Eliminar valores nulos si el formateo falló
    df = df.dropna(subset=[columna_fecha])

    df_tiempo = pd.DataFrame()
    df_tiempo["id_tiempo"] = df[columna_fecha].dt.date
    df_tiempo["anio"] = df[columna_fecha].dt.year
    df_tiempo["mes"] = df[columna_fecha].dt.month
    df_tiempo["semana"] = df[columna_fecha].dt.isocalendar().week
    df_tiempo["trimestre"] = df[columna_fecha].dt.quarter
    df_tiempo["cuatrimestre"] = ((df[columna_fecha].dt.month - 1) // 4) + 1
    df_tiempo["dia_semana"] = df[columna_fecha].dt.day_name()

    # Eliminar fechas duplicadas
    df_tiempo = df_tiempo.drop_duplicates(subset=["id_tiempo"])

    return df_tiempo
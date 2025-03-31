import pandas as pd

def agrupar_hechos_reproducciones(df):
    if not all(col in df.columns for col in ["id_usuario", "id_cancion", "id_tiempo"]):
        print("❌ Faltan columnas necesarias para agrupar hechos de reproducciones.")
        return pd.DataFrame()

    agrupado = df.groupby(["id_usuario", "id_cancion", "id_tiempo"]).agg({
        "duracion_reproduccion_segundos": "sum"
    }).rename(columns={"duracion_reproduccion_segundos": "duracion_total"}).reset_index()

    agrupado["cantidad_reproducciones"] = df.groupby(
        ["id_usuario", "id_cancion", "id_tiempo"]
    ).size().values

    df_final = agrupado.rename(columns={
        "duracion_total": "duracion_reproduccion_segundos"
    })

    return df_final
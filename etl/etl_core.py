from config.database_config import conexion_oltp_sqlalchemy, conexion_olap_sqlalchemy
from data.extraction import extraer_datos
from etl.etl_time_dimension import generar_dim_tiempo
from etl.utils import mostrar_preview, aplicar_transformacion, asignar_columnas, evitar_duplicados, seleccionar_columna
import pandas as pd
from datetime import datetime
import os

def ejecutar_etl(consulta_sql, tabla_destino):
    # Extraer
    conexion_oltp_sql = conexion_oltp_sqlalchemy()
    df_origen = extraer_datos(conexion_oltp_sql, consulta_sql)
    if df_origen.empty:
        print("❌ No se extrajeron datos.")
        return
    mostrar_preview(df_origen, "Datos extraídos:")

    # Transformar
    df_transformado = aplicar_transformacion(df_origen)
    mostrar_preview(df_transformado, "Datos transformados:")

    # Conectar a OLAP
    engine_olap = conexion_olap_sqlalchemy()
    if engine_olap is None:
        print("❌ No se pudo conectar a la base de datos OLAP.")
        return

    # Si es Dim_Tiempo, tratamos diferente
    if tabla_destino == "Dim_Tiempo":
        columna_fecha = seleccionar_columna(df_transformado)
        df_dim_tiempo = generar_dim_tiempo(df_transformado, columna_fecha)

        if df_dim_tiempo.empty:
            print("❌ No se generaron registros para Dim_Tiempo.")
            return

        try:
            df_existente = pd.read_sql("SELECT id_tiempo FROM Dim_Tiempo", engine_olap)
            df_a_insertar = df_dim_tiempo[~df_dim_tiempo["id_tiempo"].isin(df_existente["id_tiempo"])]
        except:
            df_a_insertar = df_dim_tiempo

        if df_a_insertar.empty:
            print("✅ No hay nuevas fechas para insertar en Dim_Tiempo.")
        else:
            df_a_insertar.to_sql("Dim_Tiempo", engine_olap, if_exists='append', index=False)
            print(f"✅ {len(df_a_insertar)} nuevas fechas insertadas en Dim_Tiempo.")
        return

    # Asignación de columnas
    asignaciones = asignar_columnas(df_transformado, engine_olap, tabla_destino)
    if not asignaciones:
        print("❌ No se realizó ninguna asignación. Proceso cancelado.")
        return

    try:
        df_a_insertar = df_transformado[list(asignaciones.values())]
        df_a_insertar.columns = list(asignaciones.keys())
    except Exception as e:
        print("❌ Error al reorganizar las columnas asignadas:")
        print(e)
        return

    # Agrupar HECHOS_REPRODUCCIONES
    if tabla_destino.upper() == "HECHOS_REPRODUCCIONES":
        dimensiones = {"id_usuario", "id_cancion", "id_tiempo"}
        if dimensiones.issubset(df_a_insertar.columns):
            print("📊 Agrupando datos para HECHOS_REPRODUCCIONES...")
            df_a_insertar["cantidad_reproducciones"] = 1
            df_a_insertar = (
                df_a_insertar
                .groupby(["id_usuario", "id_cancion", "id_tiempo"], as_index=False)
                .agg({
                    "duracion_reproduccion_segundos": "sum",
                    "cantidad_reproducciones": "count"
                })
            )
            mostrar_preview(df_a_insertar, "✅ Datos agregados para tabla de hechos")

            # Verificar duplicados por clave compuesta
            try:
                df_existente = pd.read_sql(
                    "SELECT id_usuario, id_cancion, id_tiempo FROM HECHOS_REPRODUCCIONES", engine_olap
                )
                antes = len(df_a_insertar)
                df_union = df_a_insertar.merge(
                    df_existente,
                    on=["id_usuario", "id_cancion", "id_tiempo"],
                    how="left",
                    indicator=True
                )

                df_duplicados = df_union.query("_merge == 'both'").drop(columns=["_merge"])
                if not df_duplicados.empty:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    log_path = f"logs/duplicados_hechos_{timestamp}.csv"
                    os.makedirs("logs", exist_ok=True)
                    df_duplicados.to_csv(log_path, index=False)
                    print(f"📝 {len(df_duplicados)} duplicados guardados en: {log_path}")

                df_a_insertar = df_union.query("_merge == 'left_only'").drop(columns=["_merge"])
                despues = len(df_a_insertar)
                print(f"🧼 Filtrados {antes - despues} registros duplicados por clave compuesta.")

            except Exception as e:
                print("⚠️ No se pudo verificar duplicados por clave compuesta:")
                print(e)
        else:
            print("⚠️ Faltan columnas necesarias para agrupar HECHOS_REPRODUCCIONES.")
            return

    # Verificar duplicados por columna clave (no para tabla de hechos)
    try:
        df_destino = pd.read_sql(f"SELECT * FROM {tabla_destino}", engine_olap)
        col_clave = df_destino.columns[0]
        if col_clave in df_a_insertar.columns:
            df_a_insertar = evitar_duplicados(df_a_insertar, df_destino[[col_clave]], col_clave)
    except Exception as e:
        print("⚠️ No se pudo verificar duplicados:")
        print(e)

    # Cargar
    if df_a_insertar.empty:
        print("✅ No hay nuevos registros para cargar.")
    else:
        try:
            df_a_insertar.to_sql(tabla_destino, engine_olap, if_exists='append', index=False)
            print(f"✅ {len(df_a_insertar)} registros nuevos insertados en {tabla_destino}.")
        except Exception as e:
            os.makedirs("logs", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = f"logs/error_insercion_{tabla_destino}_{timestamp}.log"
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(str(e))
            print("❌ Error durante la inserción. Revisa el log para más detalles.")

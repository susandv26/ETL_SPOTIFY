# etl/etl_cli.py

from config.database_config import conexion_oltp_sqlalchemy, conexion_olap_sqlalchemy
from data.extraction import extraer_datos
from sqlalchemy import inspect
import pandas as pd

def listar_tablas(conexion_engine):
    inspector = inspect(conexion_engine)
    return inspector.get_table_names(schema='dbo')

def mostrar_preview(df, mensaje="Vista previa de datos:"):
    print(f"\n{mensaje}")
    print(df.head())

def seleccionar_tabla(tablas, tipo):
    print(f"\nTablas disponibles en {tipo}:")
    for i, tabla in enumerate(tablas):
        print(f"{i}. {tabla}")
    while True:
        seleccion = input(f"Seleccione la tabla de {tipo} (número): ")
        if seleccion.isdigit():
            seleccion = int(seleccion)
            if 0 <= seleccion < len(tablas):
                return tablas[seleccion]
        print("Selección inválida. Intente de nuevo.")

def seleccionar_columna(df):
    print("\nSeleccione una columna:")
    for i, col in enumerate(df.columns):
        print(f"{i}. {col}")
    while True:
        sel = input("Número de columna: ")
        if sel.isdigit():
            idx = int(sel)
            if 0 <= idx < len(df.columns):
                return df.columns[idx]
        print("Selección inválida.")

def seleccionar_transformacion():
    print("\nOpciones de transformación:")
    print("1. Minúscula")
    print("2. Mayúscula")
    print("3. Extraer fecha")
    print("4. Concatenar campos")
    print("5. Ninguna (continuar)")
    while True:
        op = input("Seleccione una opción: ")
        if op in ('1', '2', '3', '4', '5'):
            return int(op)
        print("Opción inválida.")

def aplicar_transformacion(df):
    while True:
        op = seleccionar_transformacion()
        if op == 5:
            break
        columna = seleccionar_columna(df)

        if op == 1:
            from data.transformation import convertir_columna_a_minuscula
            df = convertir_columna_a_minuscula(df, columna)

        elif op == 2:
            from data.transformation import convertir_columna_a_mayuscula
            df = convertir_columna_a_mayuscula(df, columna)

        elif op == 3:
            print("\n📅 Formato de la fecha (ejemplo: %d/%m/%Y, %Y-%m-%d, etc.)")
            print("Consulta formatos válidos aquí: https://strftime.org")
            formato = input("Ingrese el formato de la fecha: ").strip()
            try:
                df[columna] = pd.to_datetime(df[columna], format=formato, errors='coerce')
                df = df.dropna(subset=[columna])
            except Exception as e:
                print("❌ Error al convertir la fecha:")
                print(e)
                continue
        elif op == 4:
            from data.transformation import concatenar_columnas
            df = concatenar_columnas(df)
        mostrar_preview(df, f"Transformación aplicada a columna '{columna}'")

    return df

def generar_dim_tiempo(df, columna_fecha):
    import pandas as pd

    if columna_fecha not in df.columns:
        print("❌ Columna no encontrada.")
        return pd.DataFrame()

    print("\n📅 Formato de la fecha (ejemplo: %d/%m/%Y, %Y-%m-%d, etc.)")
    print("Consulta formatos válidos aquí: https://strftime.org")
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



def evitar_duplicados(df_origen, df_destino):
    if df_destino.empty:
        return df_origen
    col_clave = df_destino.columns[0]  # Usamos la primera como clave
    nuevos = df_origen[~df_origen[col_clave].isin(df_destino[col_clave])]
    return nuevos

def asignar_columnas(df_origen, engine_olap, tabla_destino):
    inspector = inspect(engine_olap)
    columnas_info = inspector.get_columns(tabla_destino)
    columnas_destino = [col['name'] for col in columnas_info]
    columnas_origen = list(df_origen.columns)

    print("\nColumnas origen disponibles:")
    for i, col in enumerate(columnas_origen):
        print(f"{i}. {col}")

    asignaciones = {}

    for col in columnas_info:
        col_dest = col['name']
        es_autoincrement = col.get('autoincrement', False)

        if es_autoincrement:
            print(f"🚫 La columna '{col_dest}' es autoincrementable y será ignorada.")
            continue

        print(f"\n🧭 Columna destino: {col_dest}")
        seleccion = input("Ingrese el número de la columna origen (o ENTER para omitir): ")
        if seleccion.strip() == "":
            print(f"⏭️ Columna '{col_dest}' será omitida.")
            continue
        elif seleccion.isdigit():
            idx = int(seleccion)
            if 0 <= idx < len(columnas_origen):
                asignaciones[col_dest] = columnas_origen[idx]
                print(f"✅ Asignado: {col_dest} ← {columnas_origen[idx]}")
            else:
                print("⚠️ Número fuera de rango. Se omite esta columna.")
        else:
            print("⚠️ Entrada inválida. Se omite esta columna.")

    return asignaciones


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

    # Reorganizar DataFrame: origen → destino
    try:
        df_a_insertar = df_transformado[list(asignaciones.values())]
        df_a_insertar.columns = list(asignaciones.keys())
    except Exception as e:
        print("❌ Error al reorganizar las columnas asignadas:")
        print(e)
        return

    # Agrupar para tabla de hechos HECHOS_REPRODUCCIONES
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
        else:
            print("⚠️ Faltan columnas necesarias para agrupar HECHOS_REPRODUCCIONES.")
            return

    # Evitar duplicados (opcional para tabla de hechos)
    try:
        df_destino = pd.read_sql(f"SELECT * FROM {tabla_destino}", engine_olap)
        col_clave = df_destino.columns[0]
        if col_clave in df_a_insertar.columns:
            df_a_insertar = evitar_duplicados(df_a_insertar, df_destino[[col_clave]])
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
            print("❌ Error al insertar los datos:")
            print(e)

def main():
    print("🚀 ETL SPOTIFY - Menú Principal")
    engine_oltp = conexion_oltp_sqlalchemy()
    engine_olap = conexion_olap_sqlalchemy()

    while True:
        print("\nMenú:")
        print("1. Seleccionar tabla de origen")
        print("2. Ingresar consulta SQL personalizada")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            tablas = listar_tablas(engine_oltp)
            tabla_origen = seleccionar_tabla(tablas, "OLTP")
            consulta = f"SELECT * FROM {tabla_origen}"
        elif opcion == '2':
            print("Ingrese la consulta SQL (escriba END en una línea nueva para finalizar):")
            lineas = []
            while True:
                linea = input()
                if linea.strip().upper() == "END":
                    break
                lineas.append(linea)
            consulta = "\n".join(lineas)
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida.")
            continue

        tablas_destino = listar_tablas(engine_olap)
        tabla_destino = seleccionar_tabla(tablas_destino, "OLAP")
        ejecutar_etl(consulta, tabla_destino)
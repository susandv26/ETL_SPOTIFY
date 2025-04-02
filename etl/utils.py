from sqlalchemy import inspect
import os
import pandas as pd
from datetime import datetime


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
        seleccion = input(f"Seleccione la tabla de {tipo} (número o :quit para salir): ").strip().lower()
        if seleccion in [":quit", ":exit"]:
            print("👋 Saliendo del menú actual...")
            exit()
        if seleccion.isdigit():
            seleccion = int(seleccion)
            if 0 <= seleccion < len(tablas):
                return tablas[seleccion]
        print("❌ Selección inválida. Intente de nuevo.")


def seleccionar_columna(df):
    print("\nSeleccione una columna:")
    for i, col in enumerate(df.columns):
        print(f"{i}. {col}")
    while True:
        sel = input("Número de columna (o :quit para salir): ").strip().lower()
        if sel in [":quit", ":exit"]:
            print("👋 Saliendo del menú actual...")
            exit()
        if sel.isdigit():
            idx = int(sel)
            if 0 <= idx < len(df.columns):
                return df.columns[idx]
        print("❌ Selección inválida. Intente de nuevo.")


def evitar_duplicados(df_origen, df_destino, clave):
    try:
        df_destino = df_destino.dropna(subset=[clave])
        df_origen = df_origen.dropna(subset=[clave])
        nuevos = df_origen[~df_origen[clave].isin(df_destino[clave])]
        omitidos = df_origen[df_origen[clave].isin(df_destino[clave])]

        if not omitidos.empty:
            os.makedirs("logs", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            omitidos.to_csv(f"logs/omitidos_{clave}_{timestamp}.csv", index=False)
            print(f"📁 {len(omitidos)} duplicados omitidos guardados en logs/omitidos_{clave}_{timestamp}.csv")

        return nuevos

    except Exception as e:
        print("⚠️ Error al verificar duplicados:", e)
        return df_origen
    
    
def aplicar_transformacion(df):
    from etl.utils import seleccionar_transformacion, seleccionar_columna
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


def seleccionar_transformacion():
    print("\nOpciones de transformación:")
    print("1. Convertir el valor del campo a minúscula ")
    print("2. Convertir el valor del campo a Mayuscula")
    print("3. Extraer fecha")
    print("4. Concatenar el valor del campo con otro valor ")
    print("5. Ninguna (continuar)")
    while True:
        op = input("Seleccione una opción (o :quit para salir): ").strip().lower()
        if op in [":quit", ":exit"]:
            print("👋 Saliendo del menú actual...")
            exit()
        if op in ('1', '2', '3', '4', '5'):
            return int(op)
        print("❌ Opción inválida.")
        
        
        
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


def asignar_columnas(df_origen, engine_olap, tabla_destino):
    inspector = inspect(engine_olap)
    columnas_info = inspector.get_columns(tabla_destino)
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

        while True:
            print(f"\n🧭 Columna destino: {col_dest}")
            seleccion = input("Ingrese el número de la columna origen (o ENTER para omitir): ").strip().lower()

            if seleccion in [":quit", ":exit"]:
                print("👋 Saliendo del menú actual...")
                exit()

            if seleccion == "":
                print(f"⏭️ Columna '{col_dest}' será omitida.")
                break

            if seleccion.isdigit():
                idx = int(seleccion)
                if 0 <= idx < len(columnas_origen):
                    asignaciones[col_dest] = columnas_origen[idx]
                    print(f"✅ Asignado: {col_dest} ← {columnas_origen[idx]}")
                    break  # ✅ Salir del bucle si es válido
                else:
                    print("⚠️ Número fuera de rango.")
            else:
                print("⚠️ Entrada inválida. Ingrese un número válido o ENTER para omitir.")

    return asignaciones
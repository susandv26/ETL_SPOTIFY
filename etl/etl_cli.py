# etl/etl_cli.py

from config.database_config import conexion_oltp, conexion_olap_sqlalchemy
from data.extraction import extraer_datos
from data.transformation import convertir_a_minuscula, convertir_a_mayuscula, extraer_fecha  # Se extenderá
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

def seleccionar_transformacion():
    print("\nOpciones de transformación:")
    print("1. Minúscula")
    print("2. Mayúscula")
    print("3. Extraer fecha")
    print("4. Ninguna (continuar)")
    while True:
        op = input("Seleccione una opción: ")
        if op in ('1', '2', '3', '4'):
            return int(op)
        print("Opción inválida.")

def aplicar_transformacion(df, opcion):
    if opcion == 1:
        return convertir_a_minuscula(df)
    elif opcion == 2:
        return convertir_a_mayuscula(df)
    elif opcion == 3:
        return extraer_fecha(df)
    return df

def evitar_duplicados(df_origen, df_destino):
    if df_destino.empty:
        return df_origen
    col_clave = df_destino.columns[0]  # Usamos la primera como clave
    nuevos = df_origen[~df_origen[col_clave].isin(df_destino[col_clave])]
    return nuevos

def ejecutar_etl(consulta_sql, tabla_destino):
    # Extraer
    conexion_oltp_sql = conexion_oltp()
    df_origen = extraer_datos(conexion_oltp_sql, consulta_sql)
    if df_origen.empty:
        print("❌ No se extrajeron datos.")
        return
    mostrar_preview(df_origen, "Datos extraídos:")

    # Transformar
    opcion = seleccionar_transformacion()
    df_transformado = aplicar_transformacion(df_origen, opcion)
    mostrar_preview(df_transformado, "Datos transformados:")

    # Cargar
    engine_olap = conexion_olap_sqlalchemy()
    try:
        df_destino = pd.read_sql(f"SELECT * FROM {tabla_destino}", engine_olap)
    except:
        print("⚠️ La tabla destino no existe o no es accesible.")
        return

    df_a_insertar = evitar_duplicados(df_transformado, df_destino)

    if df_a_insertar.empty:
        print("✅ No hay nuevos registros para cargar.")
    else:
        df_a_insertar.to_sql(tabla_destino, engine_olap, if_exists='append', index=False)
        print(f"✅ {len(df_a_insertar)} registros nuevos insertados en {tabla_destino}.")

def main():
    print("🚀 ETL SPOTIFY - Menú Principal")
    engine_oltp = conexion_oltp()
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
from config.database_config import conexion_oltp_sqlalchemy, conexion_olap_sqlalchemy
from etl.utils import listar_tablas, seleccionar_tabla
from etl.etl_core import ejecutar_etl

def main():
    print("🚀 ETL SPOTIFY - Menú Principal")
    engine_oltp = conexion_oltp_sqlalchemy()
    engine_olap = conexion_olap_sqlalchemy()

    while True:
        print("\nMenú:")
        print("1. Seleccionar tabla de origen")
        print("2. Ingresar consulta SQL personalizada")
        print("3. Salir")
        
        opcion = input("Seleccione una opción (o escriba :quit para salir): ").strip().lower()

        if opcion in ['3', ':quit', ':exit']:
            print("👋 Saliendo del programa.")
            break

        elif opcion == '1':
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

        else:
            print("⚠️ Opción inválida. Intente de nuevo.")
            continue

        tablas_destino = listar_tablas(engine_olap)
        tabla_destino = seleccionar_tabla(tablas_destino, "OLAP")
        ejecutar_etl(consulta, tabla_destino)
from etl.etl_pipeline import etl_pipeline

# 🔧 Función para permitir pegar consultas multilínea
def leer_consulta_multilinea():
    print("🔍 Escribe o pega tu consulta SQL. Escribe 'END' en una nueva línea para terminar:")
    lineas = []
    while True:
        linea = input()
        if linea.strip().upper() == 'END':
            break
        lineas.append(linea)
    return "\n".join(lineas)

def main():
    # Leer consulta multilínea desde terminal
    consulta_sql = leer_consulta_multilinea()

    # Seleccionar la transformación
    try:
        operacion = int(input("Seleccione la operación de transformación (1: Minúscula, 2: Mayúscula, 3: Extraer Fecha): "))
    except ValueError:
        print("⚠️ Opción inválida. Debe ser un número.")
        return

    # Tabla destino
    tabla_destino = input("Ingrese la tabla de destino en OLAP: ")
    
    # Ejecutar el proceso ETL
    etl_pipeline(consulta_sql, operacion, tabla_destino)

if __name__ == "__main__":
    main()

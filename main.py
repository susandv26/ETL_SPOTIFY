from etl.etl_pipeline import etl_pipeline

def main():
    consulta_sql = input("Ingrese la consulta SQL para obtener los datos origen: ")
    operacion = int(input("Seleccione la operación de transformación (1: Minúscula, 2: Mayúscula, 3: Extraer Fecha): "))
    tabla_destino = input("Ingrese la tabla de destino en OLAP: ")
    
    # Ejecutar el proceso ETL
    etl_pipeline(consulta_sql, operacion, tabla_destino)
    
if __name__ == "__main__":
    main()
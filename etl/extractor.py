from data.extraction import extraer_datos_oltp

# Función para extraer datos desde OLTP
def extract_data(consulta_sql):
    print("Extrayendo datos...")
    return extraer_datos_oltp(consulta_sql)
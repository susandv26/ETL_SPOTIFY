
from etl.extractor import extract_data
from etl.transformer import transform_data
from etl.loader import load_data

def etl_pipeline(consulta_sql, operacion, tabla_destino):
    # Extraer datos
    datos = extract_data(consulta_sql)

    # Transformar datos
    datos_transformados = transform_data(datos, operacion)

    # Cargar datos en OLAP
    load_data(datos_transformados, tabla_destino)
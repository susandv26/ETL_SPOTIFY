
import pandas as pd
from config.database_config import conexion_oltp_sqlalchemy

# Función para ejecutar consulta y extraer datos desde OLTP
def extraer_datos(conexion, consulta_sql):
    try:
        return pd.read_sql(consulta_sql, conexion)
    except Exception as e:
        print("Error al extraer los datos de OLTP:")
        print(e)
        return pd.DataFrame()

# Función de extracción utilizando las conexiones configuradas
def extraer_datos_oltp(consulta_sql):
    conexion = conexion_oltp_sqlalchemy()
    if conexion:
        # Extraer datos de OLTP usando la consulta
        return extraer_datos(conexion, consulta_sql)
    return pd.DataFrame()
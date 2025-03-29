
import pandas as pd
from config.database_config import conexion_olap_sqlalchemy

# Función para cargar los datos transformados en OLAP
def load_data(df, tabla_destino):
    try:
        # Conectar a OLAP
        conexion = conexion_olap_sqlalchemy()
        if conexion:
            # Cargar datos en la tabla de destino
            df.to_sql(tabla_destino, con=conexion, if_exists='replace', index=False, schema='dbo')
            print(f"Datos cargados correctamente en la tabla {tabla_destino}")
        else:
            print("No se pudo conectar a OLAP")
    except Exception as e:
        print("Error al cargar los datos en OLAP:")
        print(e)
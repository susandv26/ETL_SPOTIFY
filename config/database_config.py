import pyodbc
from sqlalchemy import create_engine
import urllib

# Función para obtener la conexión a la base de datos OLTP
def conexion_oltp_sqlalchemy():
    server = 'localhost'
    database = 'BD_SPOTIFY'
    usuario = 'sa'
    password = '123'

    try:
        params = urllib.parse.quote_plus(
            f"DRIVER=ODBC Driver 17 for SQL Server;"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={usuario};"
            f"PWD={password};"
            f"Trusted_Connection=no;"
        )
        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={params}",
            fast_executemany=True
        )
        print("Conexión exitosa a la base de datos OLTP con SQLAlchemy")
        return engine
    except Exception as e:
        print("Error al conectar a la base de datos OLTP con SQLAlchemy:")
        print(e)
        return None

# Función para conectar a OLAP
def conexion_olap_sqlalchemy():
    server = 'localhost'
    database = 'DW_SPOTIFY'
    usuario = 'sa'
    password = '123'

    try:
        params = urllib.parse.quote_plus(
            f"DRIVER=ODBC Driver 17 for SQL Server;"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={usuario};"
            f"PWD={password};"
            f"Trusted_Connection=no;"
        )
        engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={params}",
            fast_executemany=True
        )
        print("Conexión exitosa a la base de datos OLAP con SQLAlchemy")
        return engine
    except Exception as e:
        print("Error al conectar a la base de datos OLAP con SQLAlchemy:")
        print(e)
        return None

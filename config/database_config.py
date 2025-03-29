import pyodbc

# Función para obtener la conexión a la base de datos OLTP
def conexion_oltp():
    server = 'localhost'
    database = 'BD_SPOTIFY'
    usuario = 'sa'
    password = '123'

    try:
        conexion = pyodbc.connect(f'DRIVER={{SQL Server}};'
                                  f'SERVER={server};'
                                  f'DATABASE={database};'
                                  f'UID={usuario};'
                                  f'PWD={password}')
        print("Conexión exitosa a la base de datos OLTP")
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos OLTP:")
        print(e)
        return None

# Función para obtener la conexión a la base de datos OLAP
def conexion_olap():
    server = 'localhost'
    database = 'DW_SPOTIFY1'
    usuario = 'sa'
    password = '123'

    try:
        conexion = pyodbc.connect(f'DRIVER={{SQL Server}};'
                                  f'SERVER={server};'
                                  f'DATABASE={database};'
                                  f'UID={usuario};'
                                  f'PWD={password}')
        print("Conexión exitosa a la base de datos OLAP")
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos OLAP:")
        print(e)
        return None
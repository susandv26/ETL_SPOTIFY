
import pyodbc

# Configuración de la conexión origen
serverOrigen = 'localhost'  # Ejemplo: 'localhost' o '192.168.1.100'
databaseOrigen = 'BD_SPOTIFY'
usuarioOrigen = 'sa'
passwordOrigen = '123'

# Cadena de conexión
try:
    print("Conectando a la base de datos OLTP...")
    # Cadena de conexión
    conexionOrigen = pyodbc.connect(f'DRIVER={{SQL Server}};'
                                    f'SERVER={serverOrigen};'
                                    f'DATABASE={databaseOrigen};'
                                    f'UID={usuarioOrigen};'
                                    f'PWD={passwordOrigen}')
    print("Conexión exitosa")


    # Cerrar la conexión
    cursor.close()
    conexionOrigen.close()

except Exception as e:
    print("Error al conectar a base de dato OLTP:")
    print(e)


# Configuración de la conexión origen
serverDestino = 'localhost'  # Ejemplo: 'localhost' o '192.168.1.100'
databaseDestino = 'DW_SPOTIFY1'
usuarioDestino = 'sa'
passwordDestino = '123'

# Cadena de conexión
try:
    print("Conectando a la base de datos OLAP...")
    # Cadena de conexión
    conexionDestino = pyodbc.connect(f'DRIVER={{SQL Server}};'
                                    f'SERVER={serverDestino};'
                                    f'DATABASE={databaseDestino};'
                                    f'UID={usuarioDestino};'
                                    f'PWD={passwordDestino}')
    print("Conexión exitosa a bases de datos OLAP")

        # Crear cursor y ejecutar consulta origen
    cursor = conexionDestino.cursor()

    # Cerrar la conexión
    cursor.close()
    conexionDestino.close()

except Exception as e:
    print("Error al conectar a base de datos OLAP:")
    print(e)

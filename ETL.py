
import pyodbc

# Configuración de la conexión origen
serverOrigen = 'localhost'  # Ejemplo: 'localhost' o '192.168.1.100'
databaseOrigen = 'BD_SPOTIFY'
usuarioOrigen = 'sa'
passwordOrigen = '123'

# Cadena de conexión
try:
    print("Conectando a la base de datos...")
    # Cadena de conexión
    conexionOrigen = pyodbc.connect(f'DRIVER={{SQL Server}};'
                                    f'SERVER={serverOrigen};'
                                    f'DATABASE={databaseOrigen};'
                                    f'UID={usuarioOrigen};'
                                    f'PWD={passwordOrigen}')
    print("Conexión exitosa")

    # Crear cursor y ejecutar consulta origen
    cursor = conexionOrigen.cursor()
    cursor.execute("SELECT * FROM dbo.Artistas")

    # Obtener y mostrar los datos origen
    filas = cursor.fetchall()
    if filas:
        for fila in filas:
            print(fila)
    else:
        print("No se encontraron registros.")

    # Cerrar la conexión
    cursor.close()
    conexionOrigen.close()

except Exception as e:
    print("Error al conectar a SQL Server:")
    print(e)
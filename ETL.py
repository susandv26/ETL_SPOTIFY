
#print('Hola mundo');

import pyodbc

# Configuración de la conexión origen
serverOrigen = 'localhost'  # Ejemplo: 'localhost' o '192.168.1.100'
databaseOrigen = 'BD_SPOTIFY'
usuarioOrigen = 'sa'
passwordOrigen = '123'

# Cadena de conexión
conexionOrigen = pyodbc.connect(f'DRIVER={{SQL Server}};'
                        f'SERVER={serverOrigen};'
                        f'DATABASE={databaseOrigen};'
                        f'UID={usuarioOrigen};'
                        f'PWD={passwordOrigen}')

# Crear cursor y ejecutar consulta origen
cursor = conexionOrigen.cursor()
cursor.execute("SELECT * FROM dbo.Artistas")

# Obtener y mostrar los datos origen
for fila in cursor.fetchall():
    print(fila)

# Cerrar la conexión
cursor.close()
conexionOrigen.close()

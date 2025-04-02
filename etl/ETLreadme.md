# ETL
                                                            
Este módulo será el núcleo del proceso ETL, extraerá de OLTP, transformará y cargará en la OLAP

___


## Estructura del proyecto

 📂etl
 ┣ 📜etl_cli.py
 ┣ 📜etl_core.py
 ┣ 📜etl_time_dimension.py
 ┣ 📜facts.py
 ┗ 📜utils.py


- ### etl_cli.py
    - Módulo de entrada, es un menú con el que el usuario interactuará.
- ### etl_core.py
    - Módulo principal, desde aquí se maneja la ejecución del ETL.
- ### etl_time_dimension.py
    - Utilizado para la dimensión de tiempo a partir de una fecha.
- ### facts.py
    - Manejará lógica para la carga de la métrica.
- ### utils.py
    - Manejo de las funciones auxiliares reutilizables.

___


## etl_cli.py

### Funciones

- #### Main
```python 
def main():
```
 -  - Ejecuta el menú principal
___


## etl_core.py

### Funciones

- #### ejecutar_etl
```python 
def ejecutar_etl(consulta_sql, tabla_destino):
```
- - Ejecuta el flujo de cualquier proceso del ETL a partir de la consulta SQL personalizada.

    - Parámetro: `consulta_sql` Consulta SQl con los datos a extraer.
    - Parámetro: `tabla_destino` Nombre de la tabla OLAP.

    - Fases:
        1. Extracción: Se conecta a la base y ejecuta la 
        consulta
        ```python 
        conexion_oltp_sql = conexion_oltp_sqlalchemy()
        df_origen = extraer_datos(conexion_oltp_sql, 
        consulta_sql)
        ```
      2. Transformación: Aplica la transformación (llamando 
      funciones auxiliares)
        ```python 
        df_transformado = aplicar_transformacion(df_origen)
        ```

        3. Dim_tiempo: Fase especial para la columna de tiempo, 
        se construye una dimensión temporal para el tratamiento 
        de estos datos
        ```python 
        df_dim_tiempo = generar_dim_tiempo(df_transformado, columna_fecha)
        ```

        4. Asignación de columnas: El usuario asigna columnas 
        de origen con la tabla de destino
        ```python 
        asignaciones = asignar_columnas()
        ```
        
        5. Agrupación para HECHOS_REPRODUCCIONES: Manejo 
        especial para la lógica de la carga tabla hechos, aquí 
        se agregan métricas como duración total y cantidad 
        reproducciones mediante la agrupación de usuario, 
        canción y tiempo.
        ```python 
        df_a_insertar = df_a_insertar.groupby()
        ```



        6. Manejo de duplicados: Aquí verificamos los 
        duplicados por: clave compuesta y columna clave, al 
        final guarda los duplicados en `.csv` dentro de 
        `/../logs`
        ```python 
                //Manda a llamar los datos existentes
                df_existente = pd.read_sql()

                //Guarda el número de registros originales
                antes = len(df_a_insertar)

                //Encuentra duplicados mediante un merge
                df_union = df_a_insertar.merge()

                //Esto funciona de la siguiente manera: 
                //fusiona registros
                //mediante llave compuesta, utilizamos left 
                //para indicar los valores nuevos

                //El indicator añade una columna, 
                //both si existe en ambos
                //lados, y left only para 
                //solo los registros nuevos

                //Guardamos los duplicados tambien para el .csv
                df_duplicados = df_union.query().drop()

                //Insertamos los nuevos
                df_a_insertar = df_union.query().drop()
        ```

        7. Carga OLAP: Carga los datos en la tabla de destino, 
        guardará en un .log si ocurre una excepción
        ```python 
        df_a_insertar.to_sql()
        ```
___

## etl_time_dimension.py

### Funciones

- #### generar_dim_tiempo
```python 
def generar_dim_tiempo(df, columna_fecha)
```
- - Genera un DataFrame con las columnas necesarias para llenar la dimensión tiempo, el usuario indica el formato de la fecha utilizando strftime.
    - Parámetro: `df` DataFrame con los datos.
    - Parámetro: `tabla_destino` Columna con la fecha.
    - Retorna: Nos devuelve el dataframe lleno para la carga de datos, o vacío en caso de errores.

___

## etl_time_dimension.py

### Funciones

- #### generar_dim_tiempo
```python 
def generar_dim_tiempo(df, columna_fecha)
```
- - Genera un DataFrame con las columnas necesarias para llenar la dimensión tiempo, el usuario indica el formato de la fecha utilizando strftime.
    - Parámetro: `df` DataFrame con los datos.
    - Parámetro: `tabla_destino` Columna con la fecha.
    - Retorna: Nos devuelve el dataframe lleno para la carga de datos, o vacío en caso de errores.

___

## facts.py

### Funciones

- #### agrupar_hechos_reproducciones
```python 
def agrupar_hechos_reproducciones(df):
```
 -  - Agrupa el dataframe de reproducciones por: usuario, canción y tiempo generando los datos necesarios para la tabla hechos, también calcula la duración total de las reproducciones.
    - Parámetro: `df` DataFrame con: `id_usuario` `id_cancion` y `id_tiempo`.
    - Retorna: Nos devuelve el dataframe lleno para la carga de datos.

___

## utils.py

### Funciones

- #### listar_tablas
```python 
def listar_tablas(conexion_engine):
```
 -  - Devuelve los nombre de la tablas disponibles.
    - Parámetro: `conexion_engine` Conexión de sqlalchemy.
    - Retorna:`list[str]` con el nombre de las tablas.

- #### mostrar_preview
```python 
def mostrar_preview(df, mensaje="Vista previa de datos:"):
```
 -  - Muestra las primeras filas del dataframe.
    - Parámetro: `df` Dataframe.
    - Parámetro: `mensaje` Texto.

- #### seleccionar_tabla
```python 
def seleccionar_tabla(tablas, tipo):
```
 -  - Permite seleccionar la tabla de la lista numérica.
    - Parámetro: `tablas` Lista de tablas.
    - Parámetro: `tipo` El tipo de base (OLTP o OLAP).
    - Retorna:`str` con el nombre de la tabla.

- #### seleccionar_columna
```python 
def seleccionar_columna(df):
```
 -  - Permite seleccionar la columna de la lista numérica.
    - Parámetro: `df` Dataframe.
    - Retorna:`str` con el nombre de la columna.

- #### evitar_duplicados
```python 
def evitar_duplicados(df_origen, df_destino, clave):
```
 -  - Filtra los registros existentes antes de insertarlos, también guarda en csv los que no fueron insertados.
    - Parámetro: `df_origen` Dataframe con nuevos datos.
    - Parámetro: `df_destino` Dataframe con los registros ya existentes.
    - Parámetro: `clave` La columna id para detectar duplicados.
    - Retorna:`DataFrame` con los registros no duplicados.

- #### seleccionar_transformacion
```python 
def seleccionar_transformacion():
```
 -  - Muestra las opciones de transformación disponibles.
    - Retorna:`int`

- #### aplicar_transformacion
```python 
def aplicar_transformacion(df):
```
 -  - Permite aplicar transformación al DataFrame.
    - Parámetro: `df` Dataframe.
    - Retorna:`DataFrame` con la transformación aplicada.

- #### asignar_columnas
```python 
def asignar_columnas(df_origen, engine_olap, tabla_destino):
```
 -  - Permite asignar columnas de un DF a las columnas de la tabla OLAP ignorando autoincrementales.
    - Parámetro: `df_origen` Dataframe.
    - Parámetro: `engine_olap` Conexion con OLAP.
    - Parámetro: `tabla_destino` Tabla de destino.
    - Retorna:`dict` mapeo de la columna destino a origen.
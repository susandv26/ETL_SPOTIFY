# ETL_SPOTIFY
```
 _____ _____ _       ____  ____   ___ _____ ___ _______   __
| ____|_   _| |     / ___||  _ \ / _ \_   _|_ _|  ___\ \ / /
|  _|   | | | |     \___ \| |_) | | | || |  | || |_   \ V / 
| |___  | | | |___   ___) |  __/| |_| || |  | ||  _|   | |  
|_____| |_| |_____| |____/|_|    \___/ |_| |___|_|     |_|  
```
___
#### Integrantes grupo 4: 
- Alejandra María Briceño           20181003159
- Aura Lidia Gonzalez               20212320086
- Eddy Ariel Cruz Anariba           20151900210
- Josué Esaú Ham Romero             20191001154
- Susan Nicoll del cid valladares   20151001883      
___

### *Este proyecto tiene como finalidad la extracción, transformación y carga (ETL) de una base de datos OLTP hacia un data warehouse OLAP*
___

## Herramientas utilazadas

- #### Python
    - Utilizado como lenguaje de programación base.
- #### SQL Server Management Studio
    - Utilizado para el almacenamiento de las bases de datos.
- #### SQLAlchemy
    - Utilizado para el manejo de las conexiones, nos ayuda a conectar con sql server.
- #### pyodbc
    - Es la capa que utiliza sqlalchemy para conectar python con sql.
- #### urllib.parse
    - Se utiliza para el manejo de las cadenas de conexión.
- #### os
    - Para la creación de archivos, como log, y csv.
- #### Datetime
    - Fechas del sistema
- #### VS
    - Será nuestra estación de trabajo
- #### GitHub
    - Lugar donde estará alojado el proyecto y nos permitirá el trabajo en equipo del código
- #### Markdown
    - Únicamente utilizado para documentación del proyecto
___


## Estructura del proyecto
<pre>
📦ETL_SPOTIFY
┣ 📂config
┃ ┗ 📜database_config.py
┣ 📂data
┃ ┣ 📜extraction.py
┃ ┗ 📜transformation.py
┣ 📂database
┃ ┣ 📜consultaOLAP.sql
┃ ┣ 📜DDLBDOLAP.sql
┃ ┣ 📜DDLBDOLTP.sql
┃ ┗ 📜DMLBDOLTP.sql
┣ 📂etl
┃ ┣ 📜etl_cli.py
┃ ┣ 📜etl_core.py
┃ ┣ 📜etl_time_dimension.py
┃ ┣ 📜facts.py
┃ ┗ 📜utils.py
┣ 📂logs
┣ 📜.gitignore
┣ 📜main.py
┗ 📜requirements.txt
</pre>

- ### config
    - Aquí guardaremos la configuración para la conexión de la base.
- ### data
    - Módulos para la extracción y transformación de los datos, interactúa con la base OLTP.
- ### database
    - Archivos que utilizamos para la creación de la base.
- ### etl
    - Parte principal del proyecto y donde se maneja todo el proceso para el ETL.
- ### logs
    - Se guardarán todos los archivos que genere el ETL, como csv, txt, etc.
- ### main.py
    - Archivo para la ejecucion del proyecto.
- ### requirements.txt
    - Archivo que contendrá las librerías necesarias para la ejecución del proyecto.

___

## Ejecución del proyecto

Para ejecutar el proyecto primero se debe instalar `requirements.txt`

`pip install -r requirements.txt`

Esto nos instala las librerias necesarias para la ejecución del proyecto

Una vez instalados los requerimientos, podemos ejecutar el programa `main.py`

`python main.py`


>[!TIP]
>
>Puede salir del programa escribiendo :quit en la consola.
-- Dimensi�n Tiempo
CREATE TABLE Dim_Tiempo (
    id_tiempo DATE NOT NULL PRIMARY KEY,
    anio INT NOT NULL,
    mes INT NOT NULL,
    semana INT NOT NULL,
    trimestre INT NOT NULL,
    cuatrimestre INT NOT NULL,
    dia_semana NVARCHAR(100) NOT NULL
);

-- Dimensi�n Usuario
CREATE TABLE Dim_Usuario (
    id_usuario INT NOT NULL PRIMARY KEY,
    nombre_usuario NVARCHAR(100) NOT NULL,
    id_plan INT NOT NULL
);

-- Dimensi�n Canci�n
CREATE TABLE Dim_Cancion (
    id_cancion INT NOT NULL PRIMARY KEY,
    id_artista INT NOT NULL,
    id_grupo INT NOT NULL,
    id_genero INT NOT NULL,
    titulo NVARCHAR(100) NOT NULL,
    duracion_segundos INT
);

-- Dimensi�n Artista
CREATE TABLE Dim_Artista (
    id_artista INT NOT NULL PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL
);

-- Dimensi�n Grupo
CREATE TABLE Dim_Grupo (
    id_grupo INT NOT NULL PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL
);

-- Dimensi�n G�nero Musical
CREATE TABLE Dim_Genero_Musical (
    id_genero INT NOT NULL PRIMARY KEY,
    nombre_genero NVARCHAR(400)
);

-- Dimensi�n Lista de Reproducci�n
CREATE TABLE Dim_Lista_Reproduccion (
    id_lista INT NOT NULL PRIMARY KEY,
    nombre_lista NVARCHAR(100) NOT NULL,
    id_usuario INT NOT NULL
);

-- Dimensi�n Plan
CREATE TABLE Dim_Plan (
    id_plan INT NOT NULL PRIMARY KEY,
    nombre_plan NVARCHAR(100) NOT NULL,
    precio DECIMAL(8, 2) NOT NULL
);

-- 3. Crear la tabla de hechos (HECHOS_REPRODUCCIONES)
CREATE TABLE HECHOS_REPRODUCCIONES (
    id_reproduccion INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_cancion INT NOT NULL,
    id_tiempo DATE NOT NULL,
    cantidad_reproducciones INT NOT NULL,
    duracion_reproduccion_segundos INT NOT NULL
    
);

-- 4. Crear las relaciones (Claves For�neas)

-- Relaci�n entre HECHOS_REPRODUCCIONES y las Dimensiones
-- Relaci�n entre HECHOS_REPRODUCCIONES y Dim_Usuario
ALTER TABLE HECHOS_REPRODUCCIONES
ADD CONSTRAINT FK_HECHOS_REPRODUCCIONES_Usuario
FOREIGN KEY (id_usuario)
REFERENCES Dim_Usuario (id_usuario);

-- Relaci�n entre HECHOS_REPRODUCCIONES y Dim_Cancion
ALTER TABLE HECHOS_REPRODUCCIONES
ADD CONSTRAINT FK_HECHOS_REPRODUCCIONES_Cancion
FOREIGN KEY (id_cancion)
REFERENCES Dim_Cancion (id_cancion);

-- Relaci�n entre HECHOS_REPRODUCCIONES y Dim_Tiempo
ALTER TABLE HECHOS_REPRODUCCIONES
ADD CONSTRAINT FK_HECHOS_REPRODUCCIONES_Tiempo
FOREIGN KEY (id_tiempo)
REFERENCES Dim_Tiempo (id_tiempo);

-- Relaci�n entre Dim_Cancion y Dim_Artista
ALTER TABLE Dim_Cancion
ADD CONSTRAINT FK_Dim_Cancion_Artista
FOREIGN KEY (id_artista)
REFERENCES Dim_Artista (id_artista);

-- Relaci�n entre Dim_Cancion y Dim_Grupo
ALTER TABLE Dim_Cancion
ADD CONSTRAINT FK_Dim_Cancion_Grupo
FOREIGN KEY (id_grupo)
REFERENCES Dim_Grupo (id_grupo);

-- Relaci�n entre Dim_Cancion y Dim_Genero_Musical
ALTER TABLE Dim_Cancion
ADD CONSTRAINT FK_Dim_Cancion_Genero
FOREIGN KEY (id_genero)
REFERENCES Dim_Genero_Musical (id_genero);

-- Relaci�n entre Dim_Usuario y Dim_Plan
ALTER TABLE Dim_Usuario
ADD CONSTRAINT FK_Dim_Usuario_Plan
FOREIGN KEY (id_plan)
REFERENCES Dim_Plan (id_plan);

-- Relaci�n entre Dim_Lista_Reproduccion y Dim_Usuario
ALTER TABLE Dim_Lista_Reproduccion
ADD CONSTRAINT FK_Dim_Lista_Reproduccion_Usuario
FOREIGN KEY (id_usuario)
REFERENCES Dim_Usuario (id_usuario);



ALTER TABLE HECHOS_REPRODUCCIONES
ADD CONSTRAINT UQ_usuario_cancion_tiempo
UNIQUE (id_usuario, id_cancion, id_tiempo);
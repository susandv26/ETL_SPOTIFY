-- CREACIÓN DE TABLAS

CREATE TABLE artistas (
    id_artista INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(100),
    fecha_nacimiento DATE
);

CREATE TABLE grupos (
    id_grupo INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    formacion DATE,
    disolucion DATE
);

CREATE TABLE artistas_grupos (
    id_artista INT NOT NULL,
    id_grupo INT NOT NULL,
    PRIMARY KEY (id_artista, id_grupo)
);

CREATE TABLE generos_musicales (
    id_genero INT NOT NULL PRIMARY KEY,
    nombre_genero VARCHAR(400)
);

CREATE TABLE canciones (
    id_cancion INT NOT NULL PRIMARY KEY,
    id_artista INT,
    id_grupo INT,
    id_genero INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    duracion_segundos INT,
    genero VARCHAR(50),
    letra TEXT,
    cantidad_reproducciones INT
);

CREATE TABLE usuarios (
    id_usuario INT NOT NULL PRIMARY KEY,
    id_plan INT,
    nombre_usuario VARCHAR(50) NOT NULL,
    correo VARCHAR(100) UNIQUE,
    fecha_registro DATE
);

CREATE TABLE listas_reproduccion (
    id_lista INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_usuario INT,
    fecha_creacion DATE
);

CREATE TABLE listas_x_canciones (
    id_lista INT NOT NULL,
    id_cancion INT NOT NULL,
    fecha_hora_agregada DATETIME NOT NULL,
    PRIMARY KEY (id_lista, id_cancion)
);

CREATE TABLE favoritos (
    id_usuario INT NOT NULL,
    id_cancion INT NOT NULL,
    PRIMARY KEY (id_usuario, id_cancion)
);

CREATE TABLE estadisticas (
    id_usuario INT NOT NULL,
    id_cancion INT NOT NULL,
    cantidad_reproducciones INT,
    fecha_ultima_reproduccion DATE,
    cantidad_minutos_reproduccion INT,
    PRIMARY KEY (id_usuario, id_cancion)
);

CREATE TABLE reproducciones (
    id_reproduccion INT NOT NULL PRIMARY KEY,
    id_usuario INT,
    id_cancion INT,
    fecha_reproduccion DATE,
    duracion_reproduccion_segundos INT
);

CREATE TABLE planes (
    id_plan INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(8, 2) NOT NULL,
    descripcion VARCHAR(255)
);

CREATE TABLE pagos (
    id_pago INT NOT NULL PRIMARY KEY,
    id_usuario INT,
    id_plan INT,
    fecha_pago DATE
);

CREATE TABLE top_artistas_mensuales (
    id_artista INT,
    id_grupo INT,
    anio INT,
    mes VARCHAR(200),
    cantidad_reproducciones VARCHAR(500),
    posicion INT
);

-- CLAVES FORÁNEAS

-- artistas_grupos
ALTER TABLE artistas_grupos
ADD CONSTRAINT fk_artistas_grupos_artista
    FOREIGN KEY (id_artista) REFERENCES artistas(id_artista);

ALTER TABLE artistas_grupos
ADD CONSTRAINT fk_artistas_grupos_grupo
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo);

-- canciones
ALTER TABLE canciones
ADD CONSTRAINT fk_canciones_artista
    FOREIGN KEY (id_artista) REFERENCES artistas(id_artista);

ALTER TABLE canciones
ADD CONSTRAINT fk_canciones_grupo
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo);

ALTER TABLE canciones
ADD CONSTRAINT fk_canciones_genero
    FOREIGN KEY (id_genero) REFERENCES generos_musicales(id_genero);

-- listas_x_canciones
ALTER TABLE listas_x_canciones
ADD CONSTRAINT fk_listas_canciones_lista
    FOREIGN KEY (id_lista) REFERENCES listas_reproduccion(id_lista);

ALTER TABLE listas_x_canciones
ADD CONSTRAINT fk_listas_canciones_cancion
    FOREIGN KEY (id_cancion) REFERENCES canciones(id_cancion);

-- favoritos
ALTER TABLE favoritos
ADD CONSTRAINT fk_favoritos_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);

ALTER TABLE favoritos
ADD CONSTRAINT fk_favoritos_cancion
    FOREIGN KEY (id_cancion) REFERENCES canciones(id_cancion);

-- estadisticas
ALTER TABLE estadisticas
ADD CONSTRAINT fk_estadisticas_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);

ALTER TABLE estadisticas
ADD CONSTRAINT fk_estadisticas_cancion
    FOREIGN KEY (id_cancion) REFERENCES canciones(id_cancion);

-- reproducciones
ALTER TABLE reproducciones
ADD CONSTRAINT fk_reproducciones_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);

ALTER TABLE reproducciones
ADD CONSTRAINT fk_reproducciones_cancion
    FOREIGN KEY (id_cancion) REFERENCES canciones(id_cancion);

-- pagos
ALTER TABLE pagos
ADD CONSTRAINT fk_pagos_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);

ALTER TABLE pagos
ADD CONSTRAINT fk_pagos_plan
    FOREIGN KEY (id_plan) REFERENCES planes(id_plan);

-- listas_reproduccion
ALTER TABLE listas_reproduccion
ADD CONSTRAINT fk_listas_usuario
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario);

-- usuarios → planes
ALTER TABLE usuarios
ADD CONSTRAINT fk_usuarios_plan
    FOREIGN KEY (id_plan) REFERENCES planes(id_plan);

-- top_artistas_mensuales
ALTER TABLE top_artistas_mensuales
ADD CONSTRAINT fk_top_artistas_artista
    FOREIGN KEY (id_artista) REFERENCES artistas(id_artista);

ALTER TABLE top_artistas_mensuales
ADD CONSTRAINT fk_top_artistas_grupo
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo);

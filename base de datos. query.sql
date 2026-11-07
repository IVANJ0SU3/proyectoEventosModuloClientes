-- Base de datos
CREATE DATABASE SistemaEventos;
GO
USE SistemaEventos;
GO
-- Tabla usuarios
CREATE TABLE usuarios (
    id         INT PRIMARY KEY IDENTITY,
    usuario    VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    pregunta   VARCHAR(200),
    respuesta  VARCHAR(200)
);

-- Tabla clientes
CREATE TABLE clientes (
    id       INT PRIMARY KEY IDENTITY,
    nombre   VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    Dui      VARCHAR(15) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    estado BIT default 1
);

-- Tabla eventos
CREATE TABLE eventos (
    id     INT PRIMARY KEY IDENTITY,
    nombre VARCHAR(100) NOT NULL,
    tipo   VARCHAR(100),
    fecha  DATE,
    lugar  VARCHAR(300),
    estado bit default 1
);
-- Tabla ventas
CREATE TABLE ventas (
    id         INT PRIMARY KEY IDENTITY,
    id_evento  INT FOREIGN KEY REFERENCES eventos(id),
    id_cliente INT FOREIGN KEY REFERENCES clientes(id),
    total      DECIMAL(10,2),
    fecha      DATETIME
);

--Tabla inventario
CREATE TABLE inventario (
    id INT PRIMARY KEY IDENTITY,
    recurso VARCHAR(100) NOT NULL UNIQUE,
    stock INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

-- Datos iniciales de inventario
INSERT INTO inventario (recurso, stock, precio) VALUES
('sillas', 100, 2.00),
('pastel pequeño', 50, 50.00),
('pastel mediano', 50, 100.00),
('pastel grande', 50, 150.00),
('pastel personalizado pequeño', 50, 100.00),
('pastel personalizado mediano', 50, 160.00),
('pastel personalizado grande', 50, 230.00),
('mesas', 55, 28.00),
('globos', 80, 2.00),
('flores', 50, 4.00),
('manteles', 60, 8.00),
('luces', 55, 10.00),
('bocinas', 60, 50.00),
('tarimas', 30, 100.00),
('carpas', 30, 200.00),
('ventiladores', 40, 30.00),
('proyectores', 39, 40.00),
('microfonos', 48, 35.00),
('extensiones de 20m', 40, 25.00),
('extensiones de 35m', 40, 40.00),
('centros de mesa', 80, 25.00),
('cortinas blancas', 40, 25.00),
('cortinas negras', 50, 25.00),
('cortinas de colores', 60, 25.00);

--Tabla asignación
CREATE TABLE asignaciones (
    id            INT PRIMARY KEY IDENTITY,
    nombre_evento VARCHAR(100) NOT NULL,
    recurso       VARCHAR(100) NOT NULL,
    cantidad      INT          NOT NULL
);

GO
create or alter procedure sp_listarEventos 
AS
BEGIN
    select id, nombre, tipo, fecha, lugar from eventos where estado = 1 order by id asc
END;
exec sp_listarEventos
GO
create OR ALTER procedure sp_ModEventos 
    @id INT,
    @nombre varchar(100),
    @tipo varchar(100),
    @fecha date,
    @lugar varchar(300)
AS
BEGIN
    update eventos set nombre = @nombre, 
                tipo = @tipo, fecha = @fecha, 
                lugar = @lugar where id = @id;
END ;

EXEC sp_ModEventos 1,'Pepito', 'Bodas','2096-12-27','El rincon tapatio';
GO

CREATE OR ALTER PROCEDURE sp_InactivarEvento 
    @id INT
AS 
BEGIN
    update eventos set estado = 0 where id = @id;
END ;
EXEC sp_InactivarEvento 1;
GO
CREATE OR ALTER PROCEDURE sp_Buscador
    @busqueda VARCHAR(300)
AS 
BEGIN
    select id, nombre, tipo, fecha, lugar from eventos where (nombre like '%'+@busqueda+'%' 
    or tipo like '%'+@busqueda+'%' or lugar like '%'+@busqueda+'%' 
    or fecha like '%'+@busqueda+'%') AND estado = 1;
END;
exec sp_Buscador 'fer'

GO
create or alter procedure sp_listarClientes 
AS
BEGIN
    select id, nombre, apellido, telefono, Dui, edad from clientes where estado = 1 order by id asc
END;
exec sp_listarClientes
GO
CREATE OR ALTER PROCEDURE sp_BuscadorClientes
    @busqueda VARCHAR(300)
AS 
BEGIN
    select id, nombre, apellido, telefono, Dui, edad from clientes where (nombre like '%'+@busqueda+'%' 
    or apellido like '%'+@busqueda+'%' or telefono like '%'+@busqueda+'%' 
    or Dui like '%'+@busqueda+'%' or edad like '%'+@busqueda+'%') AND estado = 1;
END;
GO
EXEC sp_BuscadorClientes '19'
GO

create OR ALTER procedure sp_ModClientes 
    @id INT,
    @nombre varchar(100),
    @apellido varchar(100),
    @telefono varchar(15),
    @dui varchar(15),
    @edad INT
AS
BEGIN
    update clientes set nombre = @nombre, 
                apellido = @apellido, telefono = @telefono, 
                Dui = @dui, edad = @edad where id = @id;
END ;
GO
CREATE OR ALTER PROCEDURE sp_InactivarCliente 
    @id INT
AS 
BEGIN
    update clientes set estado = 0 where id = @id;
END ;
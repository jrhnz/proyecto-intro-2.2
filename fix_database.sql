-- Script para agregar la columna categoria_id a la tabla productos

-- Primero, verifica la estructura actual
-- DESCRIBE productos;

-- Agregar la columna categoria_id si no existe
ALTER TABLE productos 
ADD COLUMN categoria_id INT DEFAULT 1 
AFTER precio;

-- Agregar la restricción de clave foránea
ALTER TABLE productos
ADD CONSTRAINT fk_productos_categorias 
FOREIGN KEY (categoria_id) REFERENCES categorias(id);

-- Verificar que se agregó correctamente
DESCRIBE productos;

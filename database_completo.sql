-- =============================================
-- SISTEMA DE INVENTARIO DENTAL - SCRIPT COMPLETO
-- =============================================

-- Limpiar todo si existe
DECLARE
    v_count NUMBER;
BEGIN
    -- Eliminar tablas
    SELECT COUNT(*) INTO v_count FROM user_tables WHERE table_name = 'MOVIMIENTOS';
    IF v_count > 0 THEN EXECUTE IMMEDIATE 'DROP TABLE movimientos CASCADE CONSTRAINTS'; END IF;
    
    SELECT COUNT(*) INTO v_count FROM user_tables WHERE table_name = 'PRODUCTOS';
    IF v_count > 0 THEN EXECUTE IMMEDIATE 'DROP TABLE productos CASCADE CONSTRAINTS'; END IF;
    
    SELECT COUNT(*) INTO v_count FROM user_tables WHERE table_name = 'USUARIOS';
    IF v_count > 0 THEN EXECUTE IMMEDIATE 'DROP TABLE usuarios CASCADE CONSTRAINTS'; END IF;

    -- Eliminar secuencias
    SELECT COUNT(*) INTO v_count FROM user_sequences WHERE sequence_name = 'SEQ_MOVIMIENTOS';
    IF v_count > 0 THEN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_movimientos'; END IF;
    
    SELECT COUNT(*) INTO v_count FROM user_sequences WHERE sequence_name = 'SEQ_PRODUCTOS';
    IF v_count > 0 THEN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_productos'; END IF;
    
    SELECT COUNT(*) INTO v_count FROM user_sequences WHERE sequence_name = 'SEQ_USUARIOS';
    IF v_count > 0 THEN EXECUTE IMMEDIATE 'DROP SEQUENCE seq_usuarios'; END IF;
END;
/

-- =============================================
-- CREAR SECUENCIAS
-- =============================================
CREATE SEQUENCE seq_usuarios START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_productos START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_movimientos START WITH 1 INCREMENT BY 1;

-- =============================================
-- CREAR TABLAS
-- =============================================
CREATE TABLE usuarios (
    id_usuario NUMBER PRIMARY KEY,
    username VARCHAR2(50) UNIQUE NOT NULL,
    password VARCHAR2(100) NOT NULL,
    nombre VARCHAR2(100) NOT NULL,
    rol VARCHAR2(20) DEFAULT 'admin'
);

CREATE TABLE productos (
    id_producto NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(200),
    categoria VARCHAR2(50),
    stock_actual NUMBER DEFAULT 0,
    stock_minimo NUMBER DEFAULT 5,
    precio_unitario NUMBER(10,2),
    fecha_creacion DATE DEFAULT SYSDATE
);

CREATE TABLE movimientos (
    id_movimiento NUMBER PRIMARY KEY,
    id_producto NUMBER,
    tipo_movimiento VARCHAR2(10),
    cantidad NUMBER,
    fecha_movimiento DATE DEFAULT SYSDATE,
    hora_movimiento VARCHAR2(8),
    motivo VARCHAR2(200),
    doctor VARCHAR2(100),
    usuario_registro VARCHAR2(50),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- =============================================
-- INSERTAR DATOS DE PRUEBA
-- =============================================
-- Usuario admin
INSERT INTO usuarios (id_usuario, username, password, nombre, rol) 
VALUES (seq_usuarios.NEXTVAL, 'admin', 'admin123', 'Administrador Principal', 'admin');

-- Productos de ejemplo
INSERT INTO productos (id_producto, nombre, descripcion, categoria, stock_actual, stock_minimo, precio_unitario) 
VALUES (seq_productos.NEXTVAL, 'Guantes Latex Talla M', 'Guantes estériles desechables', 'Insumos Médicos', 100, 20, 0.50);

INSERT INTO productos (id_producto, nombre, descripcion, categoria, stock_actual, stock_minimo, precio_unitario) 
VALUES (seq_productos.NEXTVAL, 'Jeringas Desechables 5ml', 'Jeringas estériles para anestesia', 'Material Desechable', 50, 10, 0.30);

INSERT INTO productos (id_producto, nombre, descripcion, categoria, stock_actual, stock_minimo, precio_unitario) 
VALUES (seq_productos.NEXTVAL, 'Composite A2', 'Resina composite color A2', 'Material Dental', 15, 5, 25.00);

INSERT INTO productos (id_producto, nombre, descripcion, categoria, stock_actual, stock_minimo, precio_unitario) 
VALUES (seq_productos.NEXTVAL, 'Anestesia Lidocaína', 'Anestesia local inyectable', 'Farmacia', 30, 10, 8.50);

INSERT INTO productos (id_producto, nombre, descripcion, categoria, stock_actual, stock_minimo, precio_unitario) 
VALUES (seq_productos.NEXTVAL, 'Mascarillas Desechables', 'Mascarillas quirúrgicas', 'Insumos Médicos', 200, 50, 0.25);

COMMIT;

-- =============================================
-- VERIFICAR QUE TODO SE CREÓ
-- =============================================
BEGIN
    DBMS_OUTPUT.PUT_LINE('=== SISTEMA DE INVENTARIO DENTAL ===');
    DBMS_OUTPUT.PUT_LINE('Tablas y datos creados exitosamente');
    DBMS_OUTPUT.PUT_LINE('Usuario para login: admin / admin123');
END;
/

-- Mostrar lo creado
SELECT 'USUARIOS: ' || COUNT(*) FROM usuarios
UNION ALL
SELECT 'PRODUCTOS: ' || COUNT(*) FROM productos
UNION ALL
SELECT 'MOVIMIENTOS: ' || COUNT(*) FROM movimientos;

SELECT * FROM usuarios;
SELECT * FROM productos;
class Producto:
    def __init__(self, id_producto, nombre, descripcion, categoria, stock_actual, stock_minimo, precio_unitario, fecha_creacion=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.precio_unitario = precio_unitario
        self.fecha_creacion = fecha_creacion
    
    @classmethod
    def obtener_todos(cls, db):
        query = "SELECT * FROM productos ORDER BY nombre"
        resultados = db.fetch_all(query)
        productos = []
        if resultados:
            for resultado in resultados:
                productos.append(cls(*resultado))
        return productos
    
    @classmethod
    def buscar_por_id(cls, db, id_producto):
        query = "SELECT * FROM productos WHERE id_producto = :1"
        resultado = db.fetch_one(query, (id_producto,))
        if resultado:
            return cls(*resultado)
        return None
    
    def actualizar_stock(self, db, nueva_cantidad):
        query = "UPDATE productos SET stock_actual = :1 WHERE id_producto = :2"
        db.execute_query(query, (nueva_cantidad, self.id_producto))
        self.stock_actual = nueva_cantidad
    
    def necesita_reabastecimiento(self):
        return self.stock_actual <= self.stock_minimo
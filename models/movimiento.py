from datetime import datetime

class Movimiento:
    def __init__(self, id_movimiento, id_producto, tipo_movimiento, cantidad, fecha_movimiento, hora_movimiento, motivo, doctor, usuario_registro):
        self.id_movimiento = id_movimiento
        self.id_producto = id_producto
        self.tipo_movimiento = tipo_movimiento
        self.cantidad = cantidad
        self.fecha_movimiento = fecha_movimiento
        self.hora_movimiento = hora_movimiento
        self.motivo = motivo
        self.doctor = doctor
        self.usuario_registro = usuario_registro
    
    @classmethod
    def registrar_movimiento(cls, db, id_producto, tipo_movimiento, cantidad, motivo, doctor, usuario_registro):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        
        query = """
        INSERT INTO movimientos (id_movimiento, id_producto, tipo_movimiento, cantidad, 
                               fecha_movimiento, hora_movimiento, motivo, doctor, usuario_registro)
        VALUES (seq_movimientos.NEXTVAL, :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5, :6, :7, :8)
        """
        db.execute_query(query, (
            id_producto, tipo_movimiento, cantidad, fecha_actual, 
            hora_actual, motivo, doctor, usuario_registro
        ))
        return True
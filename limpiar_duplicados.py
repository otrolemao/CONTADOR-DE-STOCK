from database.database import Database

def limpiar_productos_duplicados():
    db = Database()
    
    if not db.connection:
        print("No hay conexion a la base de datos")
        return
    
    try:
        cursor = db.connection.cursor()
        
        print("Buscando productos duplicados...")
        
        query = """
        SELECT nombre, COUNT(*) as cantidad
        FROM productos
        GROUP BY nombre
        HAVING COUNT(*) > 1
        ORDER BY nombre
        """
        
        cursor.execute(query)
        duplicados = cursor.fetchall()
        
        if not duplicados:
            print("No se encontraron productos duplicados")
            return
        
        print(f"Se encontraron {len(duplicados)} productos duplicados:")
        
        for nombre, cantidad in duplicados:
            print(f"\nProducto: {nombre} (Duplicados: {cantidad})")
            
            query_ids = """
            SELECT id_producto, stock_actual, precio_unitario
            FROM productos 
            WHERE nombre = :1
            ORDER BY id_producto
            """
            
            cursor.execute(query_ids, (nombre,))
            productos = cursor.fetchall()
            
            if len(productos) > 1:
                id_a_mantener = productos[0][0]
                stock_total = sum(p[1] for p in productos)
                precio_promedio = sum(p[2] for p in productos) / len(productos)
                
                print(f"  ID a mantener: {id_a_mantener}")
                print(f"  Stock total combinado: {stock_total}")
                print(f"  Precio promedio: ${precio_promedio:.2f}")
                
                query_update = """
                UPDATE productos 
                SET stock_actual = :1, precio_unitario = :2
                WHERE id_producto = :3
                """
                cursor.execute(query_update, (stock_total, precio_promedio, id_a_mantener))
                
                ids_a_eliminar = [str(p[0]) for p in productos[1:]]
                ids_str = ', '.join(ids_a_eliminar)
                
                query_delete_movimientos = f"""
                DELETE FROM movimientos 
                WHERE id_producto IN ({ids_str})
                """
                cursor.execute(query_delete_movimientos)
                
                query_delete_productos = f"""
                DELETE FROM productos 
                WHERE id_producto IN ({ids_str})
                """
                cursor.execute(query_delete_productos)
                
                print(f"  Eliminados IDs: {ids_str}")
        
        db.connection.commit()
        print("\nLimpieza de duplicados completada")
        
    except Exception as e:
        print(f"Error: {e}")
        db.connection.rollback()

if __name__ == "__main__":
    limpiar_productos_duplicados()
    input("\nPresione Enter para salir...")
import oracledb

def encontrar_configuracion():
    configuraciones = [
        {"user": "SYSTEM", "password": "inacap", "dsn": "localhost:1521/XE"},
        {"user": "system", "password": "inacap", "dsn": "localhost:1521/XE"},
        {"user": "sys", "password": "inacap", "dsn": "localhost:1521/XE"},
        {"user": "STOCK DENTAL SQL", "password": "inacap", "dsn": "localhost:1521/XE"},
    ]
    
    for config in configuraciones:
        try:
            print(f"Probando: {config['user']}...")
            connection = oracledb.connect(
                user=config['user'],
                password=config['password'],
                dsn=config['dsn']
            )
            print(f"✅ CONEXIÓN EXITOSA con: {config['user']}")
            
            # Verificar si existen las tablas
            cursor = connection.cursor()
            cursor.execute("SELECT table_name FROM user_tables WHERE table_name IN ('USUARIOS', 'PRODUCTOS', 'MOVIMIENTOS')")
            tablas = cursor.fetchall()
            print(f"Tablas encontradas: {[tabla[0] for tabla in tablas]}")
            
            connection.close()
            return config
        except Exception as e:
            print(f"❌ Falló: {config['user']}")
    
    return None

if __name__ == "__main__":
    config = encontrar_configuracion()
    if config:
        print(f"\n✅ USA ESTO en database.py:")
        print(f'user="{config["user"]}"')
        print(f'password="{config["password"]}"')
        print(f'dsn="{config["dsn"]}"')
    else:
        print("❌ No se pudo conectar")
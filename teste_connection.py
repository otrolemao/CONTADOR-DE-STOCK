import oracledb

def test_connection():
    print("Probando conexiones...")
    
    # Lista de combinaciones a probar
    configuraciones = [
        {"user": "system", "password": "inacap", "dsn": "localhost:1521/XE"},
        {"user": "sys", "password": "inacap", "dsn": "localhost:1521/XE"},
        {"user": "SYSTEM", "password": "inacap", "dsn": "localhost:1521/XE"},
        {"user": "clinica_dental", "password": "inacap", "dsn": "localhost:1521/XE"},
        {"user": "system", "password": "inacap", "dsn": "localhost:1521/xe"},
        {"user": "system", "password": "inacap", "dsn": "localhost:1521/ORCL"},
    ]
    
    for config in configuraciones:
        try:
            print(f"Probando: {config['user']}@{config['dsn']}")
            connection = oracledb.connect(
                user=config['user'],
                password=config['password'],
                dsn=config['dsn']
            )
            print(f"✅ CONEXIÓN EXITOSA con: {config['user']}")
            connection.close()
            return config
        except Exception as e:
            print(f"❌ Falló: {config['user']} - {e}")
    
    print("❌ No se pudo conectar con ninguna configuración")
    return None

if __name__ == "__main__":
    config_correcta = test_connection()
    if config_correcta:
        print(f"\n✅ Usa esta configuración en database.py:")
        print(f"user='{config_correcta['user']}'")
        print(f"password='{config_correcta['password']}'")
        print(f"dsn='{config_correcta['dsn']}'")
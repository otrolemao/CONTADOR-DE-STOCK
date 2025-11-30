import oracledb

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = oracledb.connect(
                user="SYS",          # ← "SYS" en lugar de "SYSTEM"
                password="inacap",   # ← Tu contraseña
                dsn="localhost:1521/XE",
                mode=oracledb.SYSDBA  # ← ¡IMPORTANTE! Agregar este modo
            )
            print("Conexion establecida con Oracle")
        except oracledb.Error as error:
            print(f"Error de conexion: {error}")
    
    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except oracledb.Error as error:
            print(f"Error en consulta: {error}")
            return None
    
    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return None
    
    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchone()
        return None
class Usuario:
    def __init__(self, id_usuario, username, password, nombre, rol):
        self.id_usuario = id_usuario
        self.username = username
        self.password = password
        self.nombre = nombre
        self.rol = rol
    
    @classmethod
    def validar_login(cls, db, username, password):
        query = "SELECT * FROM usuarios WHERE username = :1 AND password = :2"
        resultado = db.fetch_one(query, (username, password))
        if resultado:
            return cls(*resultado)
        return None
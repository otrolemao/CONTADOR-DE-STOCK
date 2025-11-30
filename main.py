from database.database import Database
from gui.main_window import LoginWindow

def main():
    print("Iniciando Sistema de Inventario Dental...")
    
    db = Database()
    
    if db.connection:
        print("Base de datos conectada correctamente")
        login = LoginWindow(db)
        login.run()
    else:
        print("No se pudo conectar a la base de datos")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()
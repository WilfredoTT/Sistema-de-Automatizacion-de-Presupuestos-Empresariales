import sqlite3
import hashlib

def inicializar_db():
    #conexión o creación del archivo de db
    conexion = sqlite3.connect("tedimeca_sistema.db")
    cursor = conexion.cursor()
    
    #creación de tabla de usuarios
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS usuarios (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT UNIQUE NOT NULL,
                       password TEXT NOT NULL,
                       rol TEXT NOT NULL
                   )''')
    
    #creación de usuario default
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        #HASH DE LA CONTRASEÑA
        password_hash = hashlib.sha256("1234".encode()).hexdigest()
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)", ("admin", password_hash, "maestro"))
    
    conexion.commit()
    conexion.close()
    
def validar_usuario(username, password):
    conexion = sqlite3.connect("tedimeca_sistema.db")
    cursor = conexion.cursor()
    
    #conversion de la clave ingresada a hash para comparar
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("SELECT rol FROM usuarios WHERE username=? AND password=?", (username, password_hash))
    
    resultado = cursor.fetchone() 
    conexion.close()
    
    return resultado
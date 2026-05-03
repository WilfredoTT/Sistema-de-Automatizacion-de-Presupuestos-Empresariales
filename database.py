import sqlite3
import hashlib
import uuid

def inicializar_db():
    #conexión o creación del archivo de db
    conexion = sqlite3.connect("tedimeca_sistema.db")
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    #----------TABLA USUARIOS------------------
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS usuarios (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       uuid_acceso TEXT NOT NULL,
                       username TEXT UNIQUE NOT NULL,
                       password TEXT NOT NULL,
                       rol TEXT CHECK (rol IN ('Maestro', 'Supervisor', 'Administrador')) NOT NULL,
                       estado TEXT CHECK (estado IN ('Activo', 'Anulado')) DEFAULT 'Activo'
                   )''')
    
    #creación de usuario default
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        #creación de uuid
        admin_uuid = str(uuid.uuid4())
        #HASH DE LA CONTRASEÑA
        password_hash = hashlib.sha256("1234".encode()).hexdigest()
        cursor.execute("INSERT INTO usuarios (uuid_acceso, username, password, rol) VALUES (?, ?, ?, ?)", (admin_uuid,"admin", password_hash, "Maestro"))
    
    #-------------------------TABLA TASA DE CAMBIO--------------------------------
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS tasa_cambio (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        valor_bs REAL NOT NULL,
                        ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
    #-------------------------TABLA LOGS SISTEMA--------------------------------
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS logs_sistema (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario_id INTEGER,
                        accion TEXT,
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                    )''')
    #-------------------------TABLA TRABAJADORES--------------------------------
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS trabajadores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        uuid_export TEXT UNIQUE NOT NULL,
                        cedula TEXT UNIQUE NOT NULL,
                        nombre_completo TEXT NOT NULL,
                        cargo_base TEXT CHECK (cargo_base IN ('Ayudante_General','Mecanico','Supervisor')) DEFAULT 'Ayudante_General' NOT NULL,
                        telefono TEXT,
                        salario_base_lv REAL DEFAULT 0,
                        salario_base_sd REAL DEFAULT 0,
                        estatus TEXT CHECK (estatus IN ('Activo', 'Inactivo')) DEFAULT 'Activo',
                        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
    #-------------------------TABLA PRESUPUESTOS--------------------------------
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS presupuestos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nro_presupuesto TEXT UNIQUE NOT NULL,
                        nro_solicitud TEXT,
                        fecha DATE DEFAULT (DATETIME('now', 'localtime')),
                        cliente_nombre TEXT NOT NULL,
                        cliente_rif TEXT NOT NULL,                   
                        cliente_direccion TEXT,
                        cliente_telefono TEXT,
                        area_trabajo TEXT,
                        descripcion_breve TEXT,
                        tiempo_ejecucion TEXT,
                        estatus TEXT CHECK (estatus IN ('Borrador', 'Emitido', 'Anulado')) DEFAULT 'Borrador'
                    )''')
    #-------------------------TABLA MANO DE OBRA--------------------------------
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS presupuesto_mano_obra (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_presupuesto INTEGER,
                        descripcion_cargo TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        salario_lv REAL NOT NULL,
                        salario_sd REAL NOT NULL,
                        horas_lv INTEGER NOT NULL,
                        horas_sd INTEGER NOT NULL,
                        fcas_aplicado REAL,
                        total_renglon REAL,      
                        FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id) ON DELETE CASCADE
                    )''')
    #-------------------------TABLA EQUIPOS--------------------------------
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS presupuesto_equipos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_presupuesto INTEGER,
                        descripcion TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        dias INTEGER NOT NULL,
                        depreciacion_dia REAL NOT NULL,
                        total_equipo REAL,
                        FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id) ON DELETE CASCADE
                    )''')
    #-------------------------TABLA EPP--------------------------------
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS presupuesto_epp (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_presupuesto INTEGER,
                        descripcion TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        dias INTEGER NOT NULL,
                        depreciacion_dia REAL NOT NULL,
                        total_epp REAL,
                        FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id) ON DELETE CASCADE
                    )''')
    #-------------------------TABLA ASISTENCIA LABORAL--------------------------------
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS asistencia_laboral (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_presupuesto INTEGER,
                        nombre_trabajador TEXT NOT NULL,
                        fecha DATE NOT NULL,
                        horas_lv_reales INTEGER DEFAULT 0,
                        horas_sd_reales INTEGER DEFAULT 0,
                        observaciones TEXT,
                        FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id) ON DELETE CASCADE
                    )''')
    #-------------------------TABLA RESUMEN--------------------------------
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS presupuesto_resumen (
                        id_presupuesto INTEGER PRIMARY KEY,
                        subtotal_mano_obra REAL,
                        monto_fcas REAL,
                        total_costos_directos REAL,
                        porcentaje_admin REAL,
                        porcentaje_utilidad REAL,
                        total_costo_obra REAL,
                        FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id) ON DELETE CASCADE
                    )''')
    
    conexion.commit()
    conexion.close()
    
def validar_usuario(username, password):
    try:
        conexion = sqlite3.connect("tedimeca_sistema.db")
        cursor = conexion.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Agregamos la condición de que el estado sea 'Activo'
        cursor.execute("""SELECT id, username, rol FROM usuarios 
                        WHERE username=? AND password=? AND estado='Activo'""", 
                    (username, password_hash))
        
        resultado = cursor.fetchone() 
        conexion.close()
        return resultado
    except:
        print("Error al validar usuario")
        return None

def obtener_usuarios():
    query = """
        SELECT id, username, rol, estado FROM usuarios
    """
    try:
        conexion = sqlite3.connect("tedimeca_sistema.db")
        cursor = conexion.cursor()
        cursor.execute(query)
        usuarios = cursor.fetchall()
        conexion.close()
        return [list(u) for u in usuarios]
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def registrar_usuario(username, password, rol):
    try:
        conexion = sqlite3.connect("tedimeca_sistema.db")
        cursor = conexion.cursor()
        user_uuid = str(uuid.uuid4())
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("""INSERT INTO usuarios (uuid_acceso, username, password, rol, estado) 
                          VALUES (?, ?, ?, ?, ?)""", 
                       (user_uuid, username, password_hash, rol, "Activo"))
        
        conexion.commit()
        conexion.close()
        return True, "Usuario registrado correctamente"
    except sqlite3.IntegrityError:
        return False, "El nombre de usuario ya existe"
    except Exception as e:
        return False, str(e)

def anular_usuario_db(id_usuario):
    try:
        conexion = sqlite3.connect("tedimeca_sistema.db")
        cursor = conexion.cursor()
        
        cursor.execute("UPDATE usuarios SET estado = 'Anulado' WHERE id = ?", (id_usuario,))
        conexion.commit()
        
        exito = cursor.rowcount > 0
        conexion.close()
        
        return (True, "Usuario anulado") if exito else (False, "No encontrado")
    except Exception as e:
        return False, str(e)
    
def desanular_usuario_db(id_usuario):
    try:
        
        conexion = sqlite3.connect("tedimeca_sistema.db")
        cursor = conexion.cursor()
        
        cursor.execute("UPDATE usuarios SET estado = 'Activo' WHERE id = ?", (id_usuario,))
        
        conexion.commit()
        conexion.close()
        
        return True, "Usuario restaurado con éxito"
    except Exception as e:
        return False, f"Error al restaurar: {str(e)}"
    
def actualizar_usuario_db(id_usuario, username, password, rol):
    try:
        conexion = sqlite3.connect("tedimeca_sistema.db")
        cursor = conexion.cursor()
        
        # Si el password está vacío, no actualizamos la contraseña
        if password.strip() == "":
            query = "UPDATE usuarios SET username = ?, rol = ? WHERE id = ?"
            params = (username, rol, id_usuario)
        else:
            query = "UPDATE usuarios SET username = ?, password = ?, rol = ? WHERE id = ?"
            params = (username, password, rol, id_usuario)
            
        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
        return True, "Usuario actualizado correctamente"
    except Exception as e:
        return False, f"Error al actualizar: {str(e)}"
import mysql.connector
import Database as db
from tkinter import messagebox

def Destruir_DB(DB):
    CURSOR = DB.cursor()
    CURSOR.execute('DROP DATABASE IF EXISTS bomberos')
    DB.commit()
    CURSOR.close()
    DB.close()

def Eventos_Consultar(DB):
    CURSOR = DB.cursor()

def Personal_Crear(DB, nro_legajo, apellido_nombre, dni, user, password):
    """Crear un nuevo registro de personal"""
    try:
        CURSOR = DB.cursor()
        query = """INSERT INTO personal (nro_legajo, apellido_nombre, dni, user, pass) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (nro_legajo, apellido_nombre, dni, user, password)
        CURSOR.execute(query, values)
        DB.commit()
        CURSOR.close()
        return True, "Personal creado exitosamente"
    except mysql.connector.IntegrityError as e:
        if "PRIMARY" in str(e):
            return False, "El número de legajo ya existe"
        elif "dni" in str(e):
            return False, "El DNI ya existe"
        else:
            return False, f"Error de integridad: {str(e)}"
    except Exception as e:
        return False, f"Error al crear personal: {str(e)}"

def Personal_Leer_Todos(DB):
    """Obtener todos los registros de personal"""
    try:
        CURSOR = DB.cursor()
        CURSOR.execute("SELECT nro_legajo, apellido_nombre, dni, user, pass FROM personal ORDER BY nro_legajo")
        registros = CURSOR.fetchall()
        CURSOR.close()
        return registros
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer personal: {str(e)}")
        return []

def Personal_Leer_Por_Legajo(DB, nro_legajo):
    """Obtener un registro específico por número de legajo"""
    try:
        CURSOR = DB.cursor()
        CURSOR.execute("SELECT nro_legajo, apellido_nombre, dni, user, pass FROM personal WHERE nro_legajo = %s", (nro_legajo,))
        registro = CURSOR.fetchone()
        CURSOR.close()
        return registro
    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar personal: {str(e)}")
        return None

def Personal_Actualizar(DB, nro_legajo, apellido_nombre, dni, user, password):
    """Actualizar un registro de personal existente"""
    try:
        CURSOR = DB.cursor()
        query = """UPDATE personal 
                   SET apellido_nombre = %s, dni = %s, user = %s, pass = %s 
                   WHERE nro_legajo = %s"""
        values = (apellido_nombre, dni, user, password, nro_legajo)
        CURSOR.execute(query, values)
        
        if CURSOR.rowcount == 0:
            CURSOR.close()
            return False, "No se encontró el personal con ese número de legajo"
        
        DB.commit()
        CURSOR.close()
        return True, "Personal actualizado exitosamente"
    except mysql.connector.IntegrityError as e:
        if "dni" in str(e):
            return False, "El DNI ya existe"
        else:
            return False, f"Error de integridad: {str(e)}"
    except Exception as e:
        return False, f"Error al actualizar personal: {str(e)}"

def Personal_Eliminar(DB, nro_legajo):
    """Eliminar un registro de personal"""
    try:
        CURSOR = DB.cursor()
        CURSOR.execute("DELETE FROM personal WHERE nro_legajo = %s", (nro_legajo,))
        
        if CURSOR.rowcount == 0:
            CURSOR.close()
            return False, "No se encontró el personal con ese número de legajo"
        
        DB.commit()
        CURSOR.close()
        return True, "Personal eliminado exitosamente"
    except Exception as e:
        return False, f"Error al eliminar personal: {str(e)}"

def Personal_Buscar(DB, campo, valor):
    """Buscar personal por un campo específico"""
    try:
        CURSOR = DB.cursor()
        if campo == "apellido_nombre":
            query = "SELECT nro_legajo, apellido_nombre, dni, user, pass FROM personal WHERE apellido_nombre LIKE %s ORDER BY nro_legajo"
            CURSOR.execute(query, (f"%{valor}%",))
        elif campo == "dni":
            query = "SELECT nro_legajo, apellido_nombre, dni, user, pass FROM personal WHERE dni = %s ORDER BY nro_legajo"
            CURSOR.execute(query, (valor,))
        elif campo == "nro_legajo":
            query = "SELECT nro_legajo, apellido_nombre, dni, user, pass FROM personal WHERE nro_legajo = %s ORDER BY nro_legajo"
            CURSOR.execute(query, (valor,))
        else:
            return []
        
        registros = CURSOR.fetchall()
        CURSOR.close()
        return registros
    except Exception as e:
        messagebox.showerror("Error", f"Error al buscar personal: {str(e)}")
        return []
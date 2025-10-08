# ====================== IMPORTACIONES ======================
import tkinter as tk
from Axel_Base_de_Datos import Conectar
from Axel_Utilidades import centrar_ventana, mostrar_info_personalizado, mostrar_advertencia_personalizado, mostrar_error_personalizado

# =================== VERIFICACIÓN LEGAJOS ===================

def verificar_legajo_borrado(nro_legajo):
    try:
        conexion = Conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT nro_legajo, apellido_nombre FROM personal WHERE nro_legajo = %s AND borradopersonal = 'N'", (nro_legajo,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error al verificar legajo borrado: {e}")
        return None

def reincorporar_bombero(nro_legajo):
    try:
        conexion = Conectar()
        cursor = conexion.cursor()
        cursor.execute("UPDATE personal SET borradopersonal = 'E' WHERE nro_legajo = %s AND borradopersonal = 'N'", (nro_legajo,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al reincorporar bombero: {e}")
        return False

# ================== ABRIDORES DE VENTANAS ==================

def volver_ventana_principal(self):
    if self.parent:
        self.parent.state("zoomed")
        self.parent.lift()
        self.parent.deiconify()
        # Ocultar la actual después de un pequeño retraso
        self.parent.after(50, lambda: self.withdraw())

def abrir_editor_bombero(self, datos_bombero=None):
    from Axel_Ventana_Editar_Bomberos import VentanaEditorBomberos
    ventana_editor = VentanaEditorBomberos(self, datos_bombero)
    centrar_ventana(ventana_editor)
    ventana_editor.lift()
    ventana_editor.deiconify()

def abrir_ventana_listado_bombero(ventana_actual, ventana_listado_bombero):
    ventana_listado_bombero.state("zoomed")
    ventana_listado_bombero.lift()
    centrar_ventana(ventana_listado_bombero)
    ventana_listado_bombero.deiconify()
    # Ocultar la actual después de un pequeño retraso
    ventana_listado_bombero.after(50, lambda: ventana_actual.withdraw())

def abrir_ventana_listado_cuerpo_bomberos(ventana_actual):
    from Axel_Ventana_Listado_Cuerpo_Bomberos import VentanaListadoCuerpoBomberos
    ventana_listado_cuerpo = VentanaListadoCuerpoBomberos(ventana_actual)
    ventana_listado_cuerpo.state("zoomed")
    ventana_listado_cuerpo.lift()
    centrar_ventana(ventana_listado_cuerpo)
    ventana_listado_cuerpo.deiconify()
    # Ocultar la actual después de un pequeño retraso
    ventana_listado_cuerpo.after(50, lambda: ventana_actual.withdraw())

# ===================== COMPROBACIONES ======================

def comprobar_existencia(numero_legajo):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM bomberos WHERE nro_legajo = %s AND borradopersonal = 'E'", (numero_legajo,))
    existencia = cursor.fetchone() is not None
    cursor.close()
    conexion.close()
    return existencia

# ================= REVISIONES DE ENTRADAS ==================

def registrar_bombero(entradas_personal):
    datos = validar_datos(entradas_personal)
    if not datos:
        return
        
    nro_legajo_int, apellido_nombre, dni_int, contrasena, rango = datos
    
    if comprobar_existencia(nro_legajo_int):
        mostrar_advertencia_personalizado("Error", "El legajo ya existe", None)
        return
    
    if registrar_personal(nro_legajo_int, apellido_nombre, dni_int, contrasena, rango):
        mostrar_info_personalizado("Éxito", "Bombero registrado correctamente", None)
        limpiar_campos(entradas_personal)

def actualizar_bombero(entradas_personal):
    if isinstance(entradas_personal, dict):
        nro_legajo = entradas_personal["nro_legajo"].get()
        apellido = entradas_personal["apellido"].get()
        nombre = entradas_personal["nombre"].get()
        dni = entradas_personal["dni"].get()
        contrasena = entradas_personal["pass"].get()
        rango = entradas_personal["rango"].get()
    else:
        nro_legajo = entradas_personal[0].get()
        apellido = entradas_personal[1].get()
        nombre = entradas_personal[2].get()
        dni = entradas_personal[3].get()
        contrasena = entradas_personal[4].get()
        rango = entradas_personal[5].get()

    if not all([nro_legajo, apellido, nombre, dni, contrasena, rango]):
        mostrar_advertencia_personalizado("Advertencia", "Complete todos los campos.", None)
        return False
    
    apellido_nombre = f"{apellido}, {nombre}"

    # Validar número de legajo
    try:
        nro_legajo_int = int(nro_legajo)
        if nro_legajo_int <= 0:
            mostrar_advertencia_personalizado("Error", "El legajo debe ser mayor a 0", None)
            return False
    except ValueError:
        mostrar_advertencia_personalizado("Error", "Legajo debe ser un número", None)
        return False

    # Validar DNI
    try:
        dni_int = int(dni)
        if dni_int <= 0:
            mostrar_advertencia_personalizado("Error", "El DNI debe ser mayor a 0", None)
            return False
    except ValueError:
        mostrar_advertencia_personalizado("Error", "DNI debe ser un número", None)
        return False
    
    if not comprobar_existencia(nro_legajo_int):
        mostrar_advertencia_personalizado("Advertencia", "El legajo no existe.", None)
        return False
    
    actualizar_personal(nro_legajo_int, apellido_nombre, dni_int, contrasena, rango)
    mostrar_info_personalizado("Éxito", "Bombero actualizado correctamente.", None)
    
    if not isinstance(entradas_personal, dict):
        limpiar_campos(entradas_personal)
    
    return True

# ====================== BASE DE DATOS ======================

def registrar_personal(nro_legajo, apellido_nombre, dni, contrasena, rango):
    conexion = Conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO personal (nro_legajo, apellido_nombre, dni, user, pass, rol) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (nro_legajo, apellido_nombre, dni, nro_legajo, contrasena, rango)
        )
        conexion.commit()
        return True
    except:
        conexion.rollback()
        mostrar_error_personalizado("Error", "Error al registrar bombero", None)
        return False
    finally:
        cursor.close()
        conexion.close()

def actualizar_personal(nro_legajo, apellido_nombre, dni, contrasena, rango):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE personal "
        "SET apellido_nombre = %s, dni = %s, user = %s, pass = %s, rol = %s "
        "WHERE nro_legajo = %s",
        (apellido_nombre, dni, nro_legajo, contrasena, rango, nro_legajo))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_datos_bombero(nro_legajo):
    conexion = Conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal WHERE nro_legajo = %s AND borradopersonal = 'E'", (nro_legajo,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()
    return fila

def borrar_bombero_logico(nro_legajo):
    try:
        conexion = Conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE personal SET borradopersonal = 'N' WHERE nro_legajo = %s AND borradopersonal = 'E'",
            (nro_legajo,)
        )
        filas_afectadas = cursor.rowcount
        conexion.commit()
        cursor.close()
        conexion.close()
        
        if filas_afectadas > 0:
            mostrar_info_personalizado("Éxito", f"Bombero con legajo {nro_legajo} eliminado correctamente.", None)
            return True
        else:
            mostrar_advertencia_personalizado("Advertencia", "No se pudo eliminar el bombero. Puede que ya esté eliminado o no exista.", None)
            return False
            
    except Exception as e:
        mostrar_error_personalizado("Error", f"Error al eliminar bombero: {str(e)}", None)
        return False

# ================= FUNCIONES GENERALES ==================

def validar_datos(entradas_personal):
    try:
        nro_legajo = entradas_personal[0].get().strip()
        apellido = entradas_personal[1].get().strip()
        nombre = entradas_personal[2].get().strip()
        dni = entradas_personal[3].get().strip()
        contrasena = entradas_personal[4].get()
        rango = entradas_personal[5].get()
        
        if not all([nro_legajo, apellido, nombre, dni, contrasena, rango]):
            mostrar_advertencia_personalizado("Advertencia", "Complete todos los campos.", None)
            return None
            
        nro_legajo_int = int(nro_legajo)
        dni_int = int(dni)
        
        if nro_legajo_int <= 0 or dni_int <= 0:
            mostrar_advertencia_personalizado("Error", "Legajo y DNI deben ser mayores a 0", None)
            return None
            
        apellido_nombre = f"{apellido}, {nombre}"
        return nro_legajo_int, apellido_nombre, dni_int, contrasena, rango
        
    except ValueError:
        mostrar_advertencia_personalizado("Error", "Legajo y DNI deben ser números", None)
        return None

def limpiar_campos(entradas_personal):
    for i, entrada in enumerate(entradas_personal):
        if i < 5:
            entrada.delete(0, tk.END)
        else:
            entrada.set("1")

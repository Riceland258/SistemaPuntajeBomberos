# ====================== IMPORTACIONES ======================
import tkinter as tk
from tkinter import messagebox
from Axel_Base_de_Datos import Conectar
from Axel_Utilidades import centrar_ventana

# ================== ABRIDORES DE VENTANAS ==================

def volver_ventana_principal(self):
    if self.parent:
        self.parent.deiconify()
        self.parent.state("zoomed")
        self.parent.lift()
    self.withdraw()

def abrir_editor_bombero(self, datos_bombero=None):
    from Axel_Ventana_Editar_Bomberos import VentanaEditorBomberos
    ventana_editor = VentanaEditorBomberos(self, datos_bombero)
    ventana_editor.deiconify()
    ventana_editor.lift()
    centrar_ventana(ventana_editor)

def abrir_ventana_listado_bombero(ventana_actual, ventana_listado_bombero):
    ventana_listado_bombero.deiconify()
    ventana_listado_bombero.state("zoomed")
    ventana_actual.withdraw()
    ventana_listado_bombero.lift()
    centrar_ventana(ventana_listado_bombero)

def abrir_ventana_listado_cuerpo_bomberos(ventana_actual):
    from Axel_Ventana_Listado_Cuerpo_Bomberos import VentanaListadoCuerpoBomberos
    ventana_listado_cuerpo = VentanaListadoCuerpoBomberos(ventana_actual)
    ventana_listado_cuerpo.deiconify()
    ventana_listado_cuerpo.state("zoomed")
    ventana_actual.withdraw()
    ventana_listado_cuerpo.lift()
    centrar_ventana(ventana_listado_cuerpo)

# ===================== COMPROBACIONES ======================

def comprobar_existencia(numero_legajo):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM personal WHERE nro_legajo = %s", (numero_legajo,))
    existencia = cursor.fetchone() is not None
    cursor.close()
    conexion.close()
    return existencia

# ================= REVISIONES DE ENTRADAS ==================

def registrar_personal_revision(entradas_personal):
    nro_legajo = entradas_personal[0].get()
    apellido = entradas_personal[1].get()
    nombre = entradas_personal[2].get()
    dni = entradas_personal[3].get()
    contrasena = entradas_personal[4].get()
    rango = entradas_personal[5].get()

    if not all([nro_legajo, apellido, nombre, dni, contrasena, rango]):
        messagebox.showwarning("Advertencia", "Faltan datos.")
        return
    
    apellido_nombre = f"{apellido}, {nombre}"

    # Validar número de legajo
    try:
        nro_legajo_int = int(nro_legajo)
        if nro_legajo_int <= 0:
            messagebox.showwarning("Error", "N° Legajo debe ser un número mayor a 0")
            return
    except ValueError:
        messagebox.showwarning("Error", "N° Legajo inválido")
        return

    # Validar DNI
    try:
        dni_int = int(dni)
        if dni_int <= 0:
            messagebox.showwarning("Error", "DNI debe ser un número mayor a 0")
            return
    except ValueError:
        messagebox.showwarning("Error", "DNI inválido")
        return
    
    # Comprobar existencia
    if comprobar_existencia(nro_legajo_int):
        messagebox.showwarning("Advertencia", "El Legajo ingresado ya existe.")
        return
    else:
        registrar_personal(nro_legajo_int, apellido_nombre, dni_int, contrasena, rango)
        messagebox.showinfo("Éxito", "Personal registrado correctamente.")
        # Limpiar las entradas (las primeras 5 son Entry, la última es StringVar)
        for i, entrada in enumerate(entradas_personal):
            if i < 5:  # Entry widgets
                entrada.delete(0, tk.END)
            else:  # StringVar
                entrada.set("3")  # Valor por defecto

def actualizar_personal_revision(entradas_personal):
    # Verificar si es diccionario (VentanaEditorBomberos) o lista (VentanaPersonal)
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
        messagebox.showwarning("Advertencia", "Faltan datos.")
        return False
    
    apellido_nombre = f"{apellido}, {nombre}"

    # Validar número de legajo
    try:
        nro_legajo_int = int(nro_legajo)
        if nro_legajo_int <= 0:
            messagebox.showwarning("Error", "N° Legajo debe ser un número mayor a 0")
            return False
    except ValueError:
        messagebox.showwarning("Error", "N° Legajo inválido")
        return False

    # Validar DNI
    try:
        dni_int = int(dni)
        if dni_int <= 0:
            messagebox.showwarning("Error", "DNI debe ser un número mayor a 0")
            return False
    except ValueError:
        messagebox.showwarning("Error", "DNI inválido")
        return False
    
    # Para actualizar, el legajo debe existir
    if not comprobar_existencia(nro_legajo_int):
        messagebox.showwarning("Advertencia", "El Legajo ingresado no existe.")
        return False
    else:
        actualizar_personal(nro_legajo_int, apellido_nombre, dni_int, contrasena, rango)
        messagebox.showinfo("Éxito", "Personal actualizado correctamente.")
        
        # Solo limpiar campos si no es desde VentanaEditorBomberos
        # (VentanaEditorBomberos maneja su propio refresco)
        if not isinstance(entradas_personal, dict):
            for i, entrada in enumerate(entradas_personal):
                if i < 5: 
                    entrada.delete(0, tk.END)
                else:  # StringVar
                    entrada.set("3")
        
        return True  # Indica que la actualización fue exitosa

# ====================== BASE DE DATOS ======================

def registrar_personal(nro_legajo, apellido_nombre, dni, contrasena, rango):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute(
            "INSERT INTO personal (nro_legajo, apellido_nombre, dni, user, pass, rango) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (nro_legajo, apellido_nombre, dni, nro_legajo, contrasena, rango)
            )
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar_personal(nro_legajo, apellido_nombre, dni, contrasena, rango):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE personal "
        "SET apellido_nombre = %s, dni = %s, user = %s, pass = %s, rango = %s "
        "WHERE nro_legajo = %s",
        (apellido_nombre, dni, nro_legajo, contrasena, rango, nro_legajo))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_datos_bombero(nro_legajo):
    conexion = Conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal WHERE nro_legajo = %s", (nro_legajo,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()
    return fila

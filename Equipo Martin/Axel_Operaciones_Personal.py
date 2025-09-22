# ====================== IMPORTACIONES ======================
import tkinter as tk
from tkinter import messagebox
from Axel_Base_de_Datos import Conectar
from Axel_Utilidades import centrar_ventana

# =========== VENTANA LISTADO CUERPO DE BOMBEROS ============

def buscar(self):
    self.filtro_actual = self.entry_buscar.get().strip()
    self.offset = 0
    self.tree.delete(*self.tree.get_children())
    self.cargar_mas()

def buscar_si_vacio(self):
    if self.entry_buscar.get().strip() == "":
        self.filtro_actual = ""
        self.offset = 0
        self.tree.delete(*self.tree.get_children())
        self.cargar_mas()

def cargar_mas(self):
    conexion = Conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
            "SELECT nro_legajo, apellido_nombre, dni, rango "
            "FROM personal "
            "ORDER BY rango DESC")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()

    if self.filtro_actual:
        filas = [f for f in filas if self.filtro_actual.lower() in str(f["nro_legajo"]).lower()]

    bloque = filas[self.offset:self.offset + self.FILAS_POR_BLOQUE]

    for i, fila in enumerate(bloque):
        tag = "evenrow" if (self.offset + i) % 2 == 0 else "oddrow"
        self.tree.insert("", "end", values=(fila["nro_legajo"], fila["apellido_nombre"], fila["dni"], fila["rango"]), tags=(tag,))

    self.offset += len(bloque)

    if len(bloque) < self.FILAS_POR_BLOQUE:
        self.btn_mas.pack_forget()
    else:
        self.btn_mas.pack(pady=5)

def editar_fila(self):
    seleccion = self.tree.selection()
    if seleccion:
        abrir_editor_bombero(self)
    else:
        messagebox.showwarning("Atención", "Debe seleccionar una fila antes de editar")

def on_double_click(self, event):
    self.editar_fila()

# ================== ABRIDORES DE VENTANAS ==================

def volver_ventana_principal(self):
    if self.parent:
        self.parent.deiconify()
        self.parent.state("zoomed")
        self.parent.lift()
    self.withdraw()

def abrir_ventana_editor_bombero(ventana_busqueda_bombero):
    ventana_busqueda_bombero.deiconify()
    ventana_busqueda_bombero.lift()
    centrar_ventana(ventana_busqueda_bombero)

def abrir_editor_bombero(self):
    from Axel_Ventana_Editar_Bomberos import VentanaEditorBomberos
    ventana_busqueda = VentanaEditorBomberos(self)
    abrir_ventana_editor_bombero(ventana_busqueda)

def abrir_ventana_listado_bombero(ventana_actual, ventana_listado_bombero):
    ventana_listado_bombero.deiconify()
    ventana_listado_bombero.state("zoomed")
    ventana_actual.withdraw()
    ventana_listado_bombero.lift()
    centrar_ventana(ventana_listado_bombero)

def abrir_ventana_listado_cuerpo_bomberos(ventana_actual):
    from Axel_Ventana_Listado_Cuerpo_Bomberos import VentanaListadoCuerpoBomberos
    # Creamos el objeto
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
        for entrada in entradas_personal:
            entrada.delete(0, tk.END)

def actualizar_personal_revision(entradas_personal):
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
    
    # Para actualizar, el legajo debe existir
    if not comprobar_existencia(nro_legajo_int):
        messagebox.showwarning("Advertencia", "El Legajo ingresado no existe.")
        return
    else:
        actualizar_personal(nro_legajo_int, apellido_nombre, dni_int, contrasena, rango)
        messagebox.showinfo("Éxito", "Personal actualizado correctamente.")
        for entrada in entradas_personal:
            entrada.delete(0, tk.END)

# ====================== BASE DE DATOS ======================

def registrar_personal(nro_legajo, apellido_nombre, dni, contrasena, rango):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute(
            "INSERT INTO personal (nro_legajo, apellido_nombre, dni, user, pass, rango) "
            "VALUES (%s, %s, %s, %s, %s)",
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

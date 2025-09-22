# ====================== IMPORTACIONES ======================
import tkinter as tk
from tkinter import messagebox
from Base_de_Datos import Conectar
from Operaciones_Personal import comprobar_existencia
from Utilidades import centrar_ventana

# ================= VENTANA LISTADO CONDUCTA =================

def mostrar_ventana_listado_conducta(self):
    self.deiconify()
    self.recargar_tabla()
    if self.parent:
        self.parent.withdraw()
    self.state("zoomed")
    self.lift()

def abrir_actualizar(self, fila):
    from Ventana_Editar_Conducta import VentanaEditorConducta
    ventana = VentanaEditorConducta(fila["id_conducta"], fila, parent=self, listado=self)
    centrar_ventana(ventana)
    ventana.grab_set()
    ventana.focus()

def recargar_tabla(self):
    self.tree.delete(*self.tree.get_children())
    self.cargar_filas()

def buscar(self):
    self.cargar_filas(filtro=self.entry_buscar.get().strip())

def buscar_si_vacio(self):
    if self.entry_buscar.get().strip() == "":
        self.cargar_filas(filtro="")

def cargar_filas(self, filtro=""):
    self.tree.delete(*self.tree.get_children())

    conexion = Conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT c.id_conducta, c.nro_legajo, c.puntos, c.mes, c.anio, p.apellido_nombre "
        "FROM conducta_personal c "
        "INNER JOIN personal p ON c.nro_legajo = p.nro_legajo "
        "ORDER BY c.nro_legajo DESC LIMIT 100"
    )
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()

    if filtro:
        filas = [f for f in filas if filtro in str(f["nro_legajo"])]

    for i, fila in enumerate(filas):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        self.tree.insert(
            "",
            "end",
            values=(
                fila["nro_legajo"],
                fila["apellido_nombre"],
                fila["puntos"],
                self.MESES[fila["mes"]-1],
                fila["anio"]
            ),
            tags=(tag,),
            iid=fila["id_conducta"]
        )

def editar_fila(self):
    seleccion = self.tree.selection()
    if seleccion:
        iid = seleccion[0]
        item = self.tree.item(iid)
        values = item["values"]
        fila = {
            "nro_legajo": values[0],
            "apellido_nombre": values[1],
            "puntos": values[2],
            "mes": self.MESES.index(values[3]) + 1,
            "anio": values[4],
            "id_conducta": int(iid)
        }
        self.abrir_actualizar(fila)
    else:
        messagebox.showwarning("Atención", "Debe seleccionar una fila antes de actualizar")

# ================== VENTANA EDITOR CONTUCTA ==================

def procesar_actualizacion(self):
            entradas_conducta = [
                self.entrada_legajo,
                self.var_punto,
                self.var_mes,
                self.entrada_anio
            ]
            actualizado = actualizar_conducta_revision(self.id_conducta, entradas_conducta)
            if actualizado:
                if self.listado:
                    self.listado.recargar_tabla()
                self.destroy()

# ===================== ABRIDORES VENTANAS =====================

def cerrar_actualizar_fila(ventana_listado, ventana_actualizar):
    ventana_actualizar.withdraw()

def abrir_puntuar_conducta(ventana_principal, ventana_puntuar):
    ventana_puntuar.deiconify()
    ventana_principal.withdraw()

def volver_ventana_principal_conducta(self):
    if self.parent:
        self.parent.deiconify()
        self.parent.state("zoomed")
        self.withdraw()
        self.parent.lift()

# ===================== COMPROBACIONES =====================

def comprobar_legajo(numero_legajo, mes, año):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM conducta_personal WHERE nro_legajo = %s AND mes = %s AND anio = %s",
                    (numero_legajo, mes, año))
    comprobacion_conducta = cursor.fetchone() is not None
    cursor.close()
    conexion.close()
    return comprobacion_conducta

# ================= REVISIONES DE ENTRADAS ==================

def puntuar_conducta_revision(entradas_conducta):
    numero_legajo = entradas_conducta[0].get()
    punto = entradas_conducta[1].get()
    mes_nombre = entradas_conducta[2].get()
    año = entradas_conducta[3].get()

    # Convertir mes a número
    meses_dict = {"Enero":1,"Febrero":2,"Marzo":3,"Abril":4,"Mayo":5,"Junio":6,
                "Julio":7,"Agosto":8,"Septiembre":9,"Octubre":10,"Noviembre":11,"Diciembre":12}
    mes = meses_dict.get(mes_nombre, 1)

    if not all([numero_legajo, punto, mes, año]):
        messagebox.showwarning("Advertencia", "Faltan datos.")
        return

    # Validar número de legajo
    try:
        numero_legajo_int = int(numero_legajo)
        if numero_legajo_int <= 0:
            messagebox.showwarning("Error", "N° Legajo debe ser un número mayor a 0")
            return
    except ValueError:
        messagebox.showwarning("Error", "N° Legajo inválido")
        return

    # Validar año
    try:
        año_int = int(año)
        if año_int <= 0:
            messagebox.showwarning("Error", "El año debe ser un número mayor a 0")
            return
    except ValueError:
        messagebox.showwarning("Error", "Año inválido")
        return

    # Comprobar existencia
    if comprobar_legajo(numero_legajo_int, mes, año_int):
        messagebox.showwarning("Advertencia", "El Legajo ingresado ya fue \n" \
                                "registrado en el mes y año seleccionado.")
        return
    
    elif not comprobar_existencia(numero_legajo_int):
        messagebox.showwarning("Advertencia", "El Legajo ingresado no existe.")
        return

    else:
        puntuar_conducta(numero_legajo_int, punto, mes, año_int)
        messagebox.showinfo("Éxito", "Puntaje de conducta registrado.")
        return

def actualizar_conducta_revision(id_conducta, entradas_conducta):
    numero_legajo = entradas_conducta[0].get()
    punto = entradas_conducta[1].get()
    mes_nombre = entradas_conducta[2].get()
    año = entradas_conducta[3].get()

    meses_dict = {"Enero":1,"Febrero":2,"Marzo":3,"Abril":4,"Mayo":5,"Junio":6, "Julio":7,"Agosto":8,"Septiembre":9,"Octubre":10,"Noviembre":11,"Diciembre":12}
    mes = meses_dict.get(mes_nombre, 1)

    if not all([numero_legajo, punto, mes, año]):
        messagebox.showwarning("Advertencia", "Faltan datos.")
        return False

    try:
        numero_legajo_int = int(numero_legajo)
        año_int = int(año)
        punto_int = int(punto)
    except ValueError:
        messagebox.showwarning("Error", "N° Legajo, Año y Punto deben ser números válidos")
        return False

    if comprobar_legajo(numero_legajo_int, mes, año_int):
        messagebox.showinfo("Error", "Ya existe un registro del legajo en el mes y año ingresado.")
        return False
    else:
        actualizar_conducta(id_conducta, numero_legajo_int, punto_int, mes, año_int)
        messagebox.showinfo("Éxito", "Puntaje actualizado.")
        return True

# ===================== BASE DE DATOS ======================

def puntuar_conducta(numero_legajo_int, punto, mes, año_int):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO conducta_personal (nro_legajo, puntos, mes, anio) VALUES (%s, %s, %s, %s)",
                    (numero_legajo_int, punto, mes, año_int))
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar_conducta(id_conducta, numero_legajo_int, punto_int, mes, año_int):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE conducta_personal SET nro_legajo=%s, puntos=%s, mes=%s, anio=%s WHERE id_conducta=%s",
        (numero_legajo_int, punto_int, mes, año_int, id_conducta)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

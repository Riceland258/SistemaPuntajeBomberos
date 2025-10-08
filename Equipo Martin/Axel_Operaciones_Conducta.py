# ====================== IMPORTACIONES ======================
import tkinter as tk
from Axel_Base_de_Datos import Conectar
from Axel_Operaciones_Personal import comprobar_existencia
from Axel_Utilidades import centrar_ventana

# ===================== ABRIDORES VENTANAS =====================

def cerrar_actualizar_fila(ventana_listado, ventana_actualizar):
    ventana_actualizar.withdraw()

def abrir_puntuar_conducta(ventana_principal, ventana_puntuar):
    ventana_puntuar.deiconify()
    # Ocultar la actual después de un pequeño retraso
    ventana_puntuar.after(50, lambda: ventana_principal.withdraw())

def volver_ventana_principal_conducta(self):
    if self.parent:
        self.parent.deiconify()
        self.parent.state("zoomed")
        self.parent.lift()
        # Ocultar la actual después de un pequeño retraso
        self.parent.after(50, lambda: self.withdraw())

# ===================== COMPROBACIONES =====================

def comprobar_existencia(numero_legajo):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM personal WHERE nro_legajo = %s AND borradopersonal = 'E'", (numero_legajo,))
    existencia = cursor.fetchone() is not None
    cursor.close()
    conexion.close()
    return existencia

def comprobar_legajo(numero_legajo, mes, año):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM conducta_personal WHERE nro_legajo = %s AND mes = %s AND anio = %s",
                    (numero_legajo, mes, año))
    comprobacion_conducta = cursor.fetchone() is not None
    cursor.close()
    conexion.close()
    return comprobacion_conducta

def comprobar_legajo_actualizar(numero_legajo, mes, año, id_conducta):
    conexion = Conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM conducta_personal WHERE nro_legajo = %s AND mes = %s AND anio = %s AND id_conducta != %s",
                    (numero_legajo, mes, año, id_conducta))
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
        mostrar_advertencia_personalizado("Error", "Complete todos los campos", None)
        return

    # Validar número de legajo
    try:
        numero_legajo_int = int(numero_legajo)
        if numero_legajo_int <= 0:
            mostrar_advertencia_personalizado("Error", "El legajo debe ser mayor a 0", None)
            return
    except ValueError:
        mostrar_advertencia_personalizado("Error", "Legajo debe ser un número", None)
        return

    # Validar año
    try:
        año_int = int(año)
        if año_int <= 0:
            mostrar_advertencia_personalizado("Error", "El año debe ser mayor a 0", None)
            return
    except ValueError:
        mostrar_advertencia_personalizado("Error", "Año debe ser un número", None)
        return

    # Comprobar existencia
    if comprobar_legajo(numero_legajo_int, mes, año_int):
        mostrar_advertencia_personalizado("Error", "El puntaje de conducta ya fue registrado\nen el mes y año ingresados", None)
        return
    
    elif not comprobar_existencia(numero_legajo_int):
        mostrar_advertencia_personalizado("Error", "El legajo no existe", None)
        return

    else:
        puntuar_conducta(numero_legajo_int, punto, mes, año_int)
        mostrar_info_personalizado("Éxito", "Puntaje de conducta registrado", None)
        return

def actualizar_conducta_revision(id_conducta, entradas_conducta):
    numero_legajo = entradas_conducta[0].get()
    punto = entradas_conducta[1].get()
    mes_nombre = entradas_conducta[2].get()
    año = entradas_conducta[3].get()

    meses_dict = {"Enero":1,"Febrero":2,"Marzo":3,"Abril":4,"Mayo":5,"Junio":6, "Julio":7,"Agosto":8,"Septiembre":9,"Octubre":10,"Noviembre":11,"Diciembre":12}
    mes = meses_dict.get(mes_nombre, 1)

    if not all([numero_legajo, punto, mes, año]):
        mostrar_advertencia_personalizado("Error", "Complete todos los campos", None)
        return False

    try:
        numero_legajo_int = int(numero_legajo)
        año_int = int(año)
        punto_int = int(punto)
    except ValueError:
        mostrar_advertencia_personalizado("Error", "N° Legajo, Año y Punto deben ser números", None)
        return False

    if comprobar_legajo_actualizar(numero_legajo_int, mes, año_int, id_conducta):
        mostrar_advertencia_personalizado("Error", "El puntaje de conducta ya fue registrado\nen el mes y año ingresados", None)
        return False
    else:
        actualizar_conducta(id_conducta, numero_legajo_int, punto_int, mes, año_int)
        mostrar_info_personalizado("Éxito", "Puntaje de conducta actualizado", None)
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

def borrar_conducta(id_conducta):
    try:
        conexion = Conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE conducta_personal SET borradoconducta = 'N' WHERE id_conducta = %s",
            (id_conducta,)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        return False

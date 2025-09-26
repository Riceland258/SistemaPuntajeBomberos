# ====================== IMPORTACIONES ======================
import tkinter as tk
from tkinter import ttk
from Axel_Base_de_Datos import Conectar

# =================== CENTRADOR VENTANAS ====================
def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth()  // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# ================= VALIDACIONES COMUNES ===================
def solo_numeros(char):
    # Permite solo numeros en campos numericos
    return char.isdigit()


def configurar_validacion_numerica(widget):
    # Configura un widget Entry para aceptar solo números
    validacion_numeros = (widget.register(solo_numeros), '%S')
    widget.config(validate='key', validatecommand=validacion_numeros)

# ================= MANEJO DE DOBLE CLICK ==================
def prevenir_doble_click(ventana, texto_boton, tiempo_bloqueo=2000):
    try:
        for widget in ventana.winfo_children():
            if isinstance(widget, tk.Frame):
                for button in widget.winfo_children():
                    if isinstance(button, tk.Button) and texto_boton in button['text']:
                        button.config(state='disabled')
                        ventana.after(tiempo_bloqueo, lambda: button.config(state='normal'))
                        return True
        return False
    except Exception:
        return False

# ================= LIMPIEZA DE FORMULARIOS =================
def limpiar_campos_genericos(entradas_lista, tipo_ultimo_campo="StringVar"):
    try:
        for i, entrada in enumerate(entradas_lista):
            if i < len(entradas_lista) - 1:
                if hasattr(entrada, 'delete'):
                    entrada.delete(0, tk.END)
            else:
                if tipo_ultimo_campo == "StringVar" and hasattr(entrada, 'set'):
                    entrada.set("1")
    except Exception:
        pass

# ================= MANEJO DE BASE DE DATOS =================
def manejar_conexion_bd(cursor, conexion, exito=True):
    try:
        if exito:
            conexion.commit()
        cursor.close()
        conexion.close()
    except Exception:
        pass

# ================= PERMISOS POR ROL ================
# from martin_login import rol_usuario  # Importar valor global del login
# global rol_usuario  # Definir como variable global

# Rol temporal
rol = 3

# Rol 3: Acceso completo - Personal y Conducta
# Rol 2: Acceso medio - Solo Personal  
# Rol 1: Sin permisos - Solo lectura

# ================= BLOQUEO DE BOTONES POR PERMISOS ================
def bloquear_botones_personal(ventana):
    if rol == 1:
        _bloquear_botones_accion(ventana)

def bloquear_botones_conducta(ventana):
    if rol in [1, 2]:
        _bloquear_botones_accion(ventana)

def _bloquear_botones_accion(ventana):
    palabras_clave = ['ingresar', 'agregar', 'borrar', 'eliminar', 'editar', 'modificar', 'actualizar', 'puntuar']
    
    def buscar_en_contenedor(contenedor):
        for widget in contenedor.winfo_children():
            if isinstance(widget, tk.Button):
                texto = widget['text'].lower()
                if any(palabra in texto for palabra in palabras_clave):
                    widget.config(state='disabled', bg='#555555', fg='#888888')
            elif isinstance(widget, tk.Frame):
                buscar_en_contenedor(widget)
    
    buscar_en_contenedor(ventana)

# ================= MESSAGEBOX PERSONALIZADOS ================

def cuadro_mensaje_personalizado(titulo, mensaje, tipo="informacion", ventana_padre=None):
    ventana_mensaje = tk.Toplevel(ventana_padre)
    ventana_mensaje.title(titulo)
    ventana_mensaje.configure(bg="black")
    ventana_mensaje.resizable(False, False)
    ventana_mensaje.grab_set()  # Modal
    
    # MARCO PRINCIPAL
    marco_principal = tk.Frame(ventana_mensaje, bg="black", padx=20, pady=20)
    marco_principal.pack(expand=True, fill="both")
    
    # ETIQUETA MENSAJE
    etiqueta_mensaje = tk.Label(
        marco_principal, 
        text=mensaje,
        font=("Arial", 12, "bold"),
        bg="black", 
        fg="white",
        wraplength=400,
        justify="center"
    )
    etiqueta_mensaje.pack(pady=(0, 20))
    
    # MARCO BOTONES
    marco_botones = tk.Frame(marco_principal, bg="black")
    marco_botones.pack()
    
    respuesta_usuario = None
    
    def al_hacer_clic_si():
        nonlocal respuesta_usuario
        respuesta_usuario = True
        ventana_mensaje.destroy()
    
    def al_hacer_clic_no():
        nonlocal respuesta_usuario
        respuesta_usuario = False
        ventana_mensaje.destroy()
    
    def al_hacer_clic_ok():
        nonlocal respuesta_usuario
        respuesta_usuario = True
        ventana_mensaje.destroy()
    
    if tipo == "pregunta":
        boton_si = tk.Button(
            marco_botones, text="Sí",
            font=("Arial", 11, "bold"),
            bg="green", fg="white",
            command=al_hacer_clic_si, width=8
        )
        boton_si.pack(side="left", padx=5)
        
        boton_no = tk.Button(
            marco_botones, text="No",
            font=("Arial", 11, "bold"),
            bg="red", fg="white",
            command=al_hacer_clic_no, width=8
        )
        boton_no.pack(side="left", padx=5)
    else:
        boton_ok = tk.Button(
            marco_botones, text="OK",
            font=("Arial", 11, "bold"),
            bg="blue", fg="white",
            command=al_hacer_clic_ok, width=10
        )
        boton_ok.pack()
    
    centrar_ventana(ventana_mensaje)
    
    # Esperar respuesta del usuario
    ventana_mensaje.wait_window()
    return respuesta_usuario

def mostrar_info_personalizado(titulo, mensaje, ventana_padre=None):
    return cuadro_mensaje_personalizado(titulo, mensaje, "informacion", ventana_padre)

def mostrar_advertencia_personalizado(titulo, mensaje, ventana_padre=None):
    return cuadro_mensaje_personalizado(titulo, mensaje, "advertencia", ventana_padre)

def mostrar_error_personalizado(titulo, mensaje, ventana_padre=None):
    return cuadro_mensaje_personalizado(titulo, mensaje, "error", ventana_padre)

def preguntar_si_no_personalizado(titulo, mensaje, ventana_padre=None):
    return cuadro_mensaje_personalizado(titulo, mensaje, "pregunta", ventana_padre)

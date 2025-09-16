import tkinter as tk
from tkinter import ttk

import Database as db
import Funciones as fn

import abm_personal

# CONSTANTES
ROOT = tk.Tk()
ROOT.resizable(False, False) # Deshabilitar redimensionamiento
ROOT.state('zoomed')  # Iniciar maximizado
PAD = 12 # Padding general
halfPAD = PAD // 2

def Reset_ROOT():
    for widget in ROOT.winfo_children():
        widget.destroy()

def Redireccionar(rol):
    if rol == '1':
        Menu_Root()
    elif rol == '2':
        pass
    elif rol == '3':
        pass

def Menu_Root():
    ROOT.title('Root')
    Reset_ROOT()

    # Frame principal
    frame_main = ttk.Frame(ROOT, padding=(PAD**2, PAD, PAD**2, PAD), relief='ridge')
    frame_main.pack(fill=tk.BOTH, expand=True)

    # Eventos
    eventos = fn.Eventos_Consultar()

    frame_eventos = ttk.LabelFrame(frame_main, padding=(PAD, halfPAD, 0, 0), text='Eventos')
    frame_eventos.pack(fill='both', expand=True)

    for i in range(len(eventos)):
        if i % 3 == 0:
            frame_eventos_sub = ttk.Frame(frame_eventos)
            frame_eventos_sub.pack(fill='both', expand=True)
            
        evento = eventos[i]
        button_evento = ttk.Button(frame_eventos_sub, text=f'{evento[1]}')
        button_evento.pack(fill='both', expand=True, side='left', padx=(0, PAD), pady=(0, PAD))

    # Navegación
    frame_navegar = ttk.LabelFrame(frame_main, padding=(PAD, halfPAD, 0, PAD), text='Navegar')
    frame_navegar.pack(fill='both', expand=False)

    button_personal = ttk.Button(frame_navegar, text='Personal', command=lambda: abm_personal.abrir_abm_personal())
    button_personal.pack(fill='both', expand=True, side='left', padx=(0, PAD))
    
    button_eventos = ttk.Button(frame_navegar, text='Eventos')
    button_eventos.pack(fill='both', expand=True, side='left', padx=(0, PAD))
    
    button_asistencias = ttk.Button(frame_navegar, text='Asistencias')
    button_asistencias.pack(fill='both', expand=True, side='left', padx=(0, PAD))

    button_salir = ttk.Button(frame_navegar, text='Salir', command=ROOT.destroy)
    button_salir.pack(fill='both', expand=True, side='right', padx=(0, PAD))    
    
if __name__ == '__main__':
    # Configuración de la ventana principal
    ROOT.title('Inicio de sesión')

    frame_main = ttk.Frame(ROOT, padding=(PAD**2, PAD, PAD**2, PAD), relief='ridge')
    frame_main.pack(fill='both', expand=True)

    frame_usuario = ttk.LabelFrame(frame_main, padding=PAD, text='Usuario')
    frame_usuario.pack(fill='both', pady=(0, PAD))

    entry_usuario = ttk.Entry(frame_usuario)
    entry_usuario.pack(fill='x', expand=True)

    frame_contrasenia = ttk.LabelFrame(frame_main, padding=PAD, text='Contraseña')
    frame_contrasenia.pack(fill='both', pady=(0, PAD))

    entry_contrasenia = ttk.Entry(frame_contrasenia, show='*')
    entry_contrasenia.pack(fill='x', expand=True)

    button_login = ttk.Button(frame_main, text='Iniciar sesión', command=lambda: Redireccionar(fn.Iniciar_Sesion(entry_usuario.get(), entry_contrasenia.get())))
    button_login.pack(fill='both', expand=True)
    
    # Iniciar el bucle principal de la interfaz gráfica
    print('Administrador: admin / admin')
    ROOT.mainloop()
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

if __name__ == '__main__':
    # Configuración de la ventana principal
    ROOT.title('Bomberos')

    # Frame principal
    frame_main = ttk.Frame(ROOT, padding=(PAD**2, PAD, PAD**2, PAD), relief='ridge')
    frame_main.pack(fill=tk.BOTH, expand=True)

    # Eventos
    eventos = fn.Eventos_Consultar()
    print(eventos)

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

    button_Personal = ttk.Button(frame_navegar, text='Personal', command=lambda: abm_personal.abrir_abm_personal())
    button_Personal.pack(fill='both', expand=True, side='left', padx=(0, PAD))
    
    button_Eventos = ttk.Button(frame_navegar, text='Eventos')
    button_Eventos.pack(fill='both', expand=True, side='left', padx=(0, PAD))
    
    button_Asistencias = ttk.Button(frame_navegar, text='Asistencias')
    button_Asistencias.pack(fill='both', expand=True, side='left', padx=(0, PAD))

    # Iniciar el bucle principal de la interfaz gráfica
    ROOT.mainloop()
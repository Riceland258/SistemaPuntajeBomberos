import tkinter as tk
from tkinter import ttk

import Database as db
import Funciones as fn

# CONSTANTES
ROOT = tk.Tk()
ROOT.resizable(False, False) # Deshabilitar redimensionamiento
ROOT.state('zoomed')  # Iniciar maximizado
PAD = 12 # Padding general
COLOR_BG = '#f0f0f0' # Color de fondo

if __name__ == '__main__':
    # Configuración de la ventana principal
    ROOT.title('Bomberos')

    # Frame principal
    frame_main = ttk.Frame(ROOT, padding=PAD, relief='ridge')
    frame_main.pack(fill=tk.BOTH, expand=True)

    # Contenido
    eventos = fn.Eventos_Consultar

    # Iniciar el bucle principal de la interfaz gráfica
    ROOT.mainloop()
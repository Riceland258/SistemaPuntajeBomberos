import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'bomberos',
}

PAD = 12

def Limpiar(frame):
    for widget in frame.winfo_children():
        widget.destroy()

class Menu_Eventos:
    def __init__(self, master):
        if not master:
            self.root = tk.Tk()
            self.UI()
            self.root.mainloop()

        else:
            self.root = master
            self.UI()
    
    def UI(self):
        self.frame = ttk.Frame(self.root, padding=PAD)
        self.frame.pack(fill='both', expand=True)

        self.frame_eventos = ttk.Labelframe(self.root, padding=PAD)
        self.frame_eventos.pack(fill='both', expand=True)

class Conexion:
    def __init__(self):
        self.DB = mysql.connector.connect(**DB_CONFIG)

    def Consultar_Eventos(self):
        crs = self.DB.cursor()
        crs.execute('SELECT * FROM eventos')
        resultados = crs.fetchall()
        crs.close()
        return resultados
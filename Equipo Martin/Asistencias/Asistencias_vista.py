import tkinter as tk
from tkinter import ttk
import Asistencias_controlador as con

PAD = 12

class Asistencias(tk.Tk):
    def __init__(self, asistencias, personal, eventos):
        super().__init__()
        self.title('Bomberos')

        self.frame = ttk.Frame(self, padding=PAD)
        self.frame.pack(expand=True, fill='both')

        self.frame_navegar = ttk.Labelframe(self.frame, text='Navegar', padding=PAD)
        self.frame_navegar.pack(expand=False, fill='both', side='left', padx=(0, PAD))

        self.button_salir = ttk.Button(self.frame_navegar, text='Salir')
        self.button_salir.pack()

        self.frame_contenido = ttk.LabelFrame(self.frame, text='Planilla', padding=PAD)
        self.frame_contenido.pack(expand=True, fill='both', side='right')

        columnas = ('Evento', 'Asistencias', 'Total', 'Puntaje')
        self.tree = ttk.Treeview(self.frame_contenido, columns=columnas)
        for columna in columnas:
            self.tree.heading(columna, text=columna)
        self.tree.pack(expand=True, fill='both', side='left')

        for nro_legajo, datos in asistencias.items():
            level1 = self.tree.insert('', 'end', text=personal.get(nro_legajo)['apellido_nombre'])

            for id_evento, evento in datos.items():
                self.tree.insert(level1, 'end', values=(eventos.get(id_evento)['evento'], evento['asistencias'], evento['cantidad'], evento['calculo']))

        self.scrollbar_v = ttk.Scrollbar(self.frame_contenido, orient='vertical', command=self.tree.yview)
        self.scrollbar_v.pack(expand=False, fill='y', side='right')
        self.tree.configure(yscrollcommand=self.scrollbar_v.set)


class OtherAppGUI(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Bomberos')

        self.button_nav = ttk.Button(self, text='?')
        self.button_nav.pack()
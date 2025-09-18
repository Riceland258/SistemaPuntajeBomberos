import mysql.connector
import tkinter
from tkinter import ttk, messagebox
import re

import Funciones as fn

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql',  
    'database': 'bomberos',
}
PAD = 12
halfPAD = PAD // 2
squaredPAD = PAD ** 2

Mensajes = {
    'ERROR_CAMPOS_VACIOS'          : 'Error: No se permiten campos vacíos.',
    'ERROR_EVENTO_PUNTOS'          : 'Error: Los puntos deben ser un número entero positivo menor o igual a 10.',
    'ERROR_EVENTO_NO_SELECCIONADO' : 'Error: No se ha seleccionado ningún evento.',
    'ERROR_EVENTO_NOMBRE'          : 'Error: El nombre del evento no es válido. Solo se permiten letras, números y espacios, con una longitud máxima de 100 caracteres.',
    'EXITO_EVENTO_AGREGADO'        : 'Éxito: Evento agregado correctamente.',
    'EXITO_EVENTO_MODIFICADO'      : 'Éxito: Evento modificado correctamente.',
    'EXITO_EVENTO_ELIMINADO'       : 'Éxito: Evento eliminado correctamente.',
}

def Limpiar(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def Abrir():
    window = tkinter.Tk()
    window.title('ABM Eventos')
    window.resizable(False, False)
    window.state('zoomed')
    ABM_Eventos(window)

def ABM_Eventos(window, parent=None):
    if parent:
        window = tkinter.Toplevel(parent)

    Limpiar(window)

    frame_main = ttk.Frame(window, padding=PAD, relief='ridge')
    frame_main.pack(fill='both', expand=True)

    frame_tree = ttk.LabelFrame(frame_main, padding=(PAD, halfPAD, PAD , PAD), text='Eventos')
    frame_tree.pack(fill='both', expand=True)

    _Eventos = Eventos()
    eventos = _Eventos.Consultar()
    columnas = [columna[0] for columna in _Eventos.Consultar_Columnas()]

    tree = ttk.Treeview(frame_tree, columns=columnas, show='headings')
    tree.pack(fill='both', expand=True)

    tree.heading(columnas[0], text='ID')
    tree.heading(columnas[1], text='Evento')
    tree.heading(columnas[2], text='Puntos')

    for evento in eventos:
        tree.insert('', 'end', values=evento)

    frame_botones = ttk.LabelFrame(frame_main, padding=PAD, text='Acciones')
    frame_botones.pack(fill=tkinter.BOTH, expand=False, pady=(PAD, 0))

    buttons = ['Salir', 'Eliminar', 'Modificar', 'Agregar']
    for button in buttons:
        button_ = ttk.Button(frame_botones, text=button)
        button_.pack(side='left', fill='x', expand=True, padx=(0, PAD) if button != buttons[-1] else 0)

        match button:
            case 'Salir':
                 button_.config(command=window.destroy)

            case 'Eliminar':
                button_.config(command=lambda: [_Eventos.Eliminar(tree.item(tree.selection())['values'][0]), ABM_Eventos(window)])

            case 'Modificar':
                button_.config(command=lambda: ABM_Modificar(window, _Eventos, tree.item(tree.selection())['values'][0], tree.item(tree.selection())['values'][1], tree.item(tree.selection())['values'][2]) if tree.selection() else messagebox.showerror('Error', Mensajes['ERROR_EVENTO_NO_SELECCIONADO']))

            case 'Agregar':
                button_.config(command=lambda: ABM_Agregar(window, _Eventos))

    window.mainloop()

def ABM_Agregar(window, _Eventos):
    Limpiar(window)    

    frame_main = ttk.Frame(window, padding=(squaredPAD, PAD, squaredPAD, PAD), relief='ridge')
    frame_main.pack(fill='both', expand=True)

    frame_entradas = ttk.LabelFrame(frame_main, padding=(PAD, halfPAD, PAD , PAD), text='Nuevo Evento')
    frame_entradas.pack(fill='both', expand=True)

    frame_nombre = ttk.LabelFrame(frame_entradas, text='Nombre del Evento')
    frame_nombre.pack(fill='x', expand=True, pady=(0, PAD))

    entry_nombre = ttk.Entry(frame_nombre)
    entry_nombre.pack(fill='x', expand=True, padx=PAD, pady=halfPAD)

    frame_puntos = ttk.LabelFrame(frame_entradas, text='Puntos del Evento')
    frame_puntos.pack(fill='x', expand=True, pady=(0, PAD))

    entry_puntos = ttk.Entry(frame_puntos)
    entry_puntos.pack(fill='x', expand=True, padx=PAD, pady=halfPAD)

    frame_botones = ttk.LabelFrame(frame_main, padding=PAD, text='Acciones')
    frame_botones.pack(fill=tkinter.BOTH, expand=False)

    button_cancelar = ttk.Button(frame_botones, text='Cancelar', command=lambda: ABM_Eventos(window=window))
    button_cancelar.pack(side='left', fill='x', expand=True)

    button_guardar = ttk.Button(frame_botones, text='Guardar', command=lambda: [_Eventos.Agregar(entry_nombre.get(), entry_puntos.get()), ABM_Eventos(window)])
    button_guardar.pack(side='left', fill='x', expand=True, padx=PAD)

def ABM_Modificar(window, _Eventos, evento_id, evento_nombre, evento_puntos):
    Limpiar(window)    

    frame_main = ttk.Frame(window, padding=(squaredPAD, PAD, squaredPAD, PAD), relief='ridge')
    frame_main.pack(fill='both', expand=True)

    frame_entradas = ttk.LabelFrame(frame_main, padding=(PAD, halfPAD, PAD , PAD), text='Modificar Evento')
    frame_entradas.pack(fill='both', expand=True)

    frame_nombre = ttk.LabelFrame(frame_entradas, text='Nombre del Evento')
    frame_nombre.pack(fill='x', expand=True, pady=(0, PAD))

    entry_nombre = ttk.Entry(frame_nombre)
    entry_nombre.insert(0, evento_nombre)
    entry_nombre.pack(fill='x', expand=True, padx=PAD, pady=halfPAD)

    frame_puntos = ttk.LabelFrame(frame_entradas, text='Puntos del Evento')
    frame_puntos.pack(fill='x', expand=True, pady=(0, PAD))

    entry_puntos = ttk.Entry(frame_puntos)
    entry_puntos.insert(0, evento_puntos)
    entry_puntos.pack(fill='x', expand=True, padx=PAD, pady=halfPAD)

    frame_botones = ttk.LabelFrame(frame_main, padding=PAD, text='Acciones')
    frame_botones.pack(fill=tkinter.BOTH, expand=False)

    button_cancelar = ttk.Button(frame_botones, text='Cancelar', command=lambda: ABM_Eventos(window=window))
    button_cancelar.pack(side='left', fill='x', expand=True)

    button_guardar = ttk.Button(frame_botones, text='Guardar', command=lambda: [_Eventos.Modificar(evento_id, entry_nombre.get(), entry_puntos.get()), ABM_Eventos(window)])
    button_guardar.pack(side='left', fill='x', expand=True, padx=PAD)

class Eventos:
    def __init__(self):
        self.DB = mysql.connector.connect(**DB_CONFIG)

    def Consultar(self):
        crs = self.DB.cursor()
        crs.execute('SELECT * FROM eventos')
        resultados = crs.fetchall()
        crs.close()
        return resultados

    def Consultar_Columnas(self):
        crs = self.DB.cursor()
        crs.execute('SHOW COLUMNS FROM eventos')
        resultados = crs.fetchall()
        crs.close()
        return resultados

    def Agregar(self, evento, puntos):
        if not self.Validar(evento, puntos):
            return
        
        crs = self.DB.cursor()
        crs.execute('INSERT INTO eventos (evento, puntos) VALUES (%s, %s)', (evento, puntos))
        self.DB.commit()
        crs.close()

    def Modificar(self, evento_id, evento, puntos):
        if not self.Validar(evento, puntos):
            return
        
        crs = self.DB.cursor()
        crs.execute('UPDATE eventos SET evento = %s, puntos = %s WHERE id_evento = %s', (evento, puntos, evento_id))
        self.DB.commit()
        crs.close()

    def Eliminar(self, id_evento):        
        crs = self.DB.cursor()
        crs.execute('DELETE FROM eventos WHERE id_evento = %s', (id_evento,))
        self.DB.commit()
        crs.close()

    def Validar(self, evento, puntos):
        if not evento or not puntos:
            messagebox.showerror('Error', Mensajes['ERROR_CAMPOS_VACIOS'])
            return False

        if not re.match(r'^[\w\s]{1,100}$', evento):
            messagebox.showerror('Error', Mensajes['ERROR_EVENTO_NOMBRE'])
            return False
        
        try:
            puntos = int(puntos)
            
            if puntos < 1 or puntos > 10:
                messagebox.showerror('Error', Mensajes['ERROR_EVENTO_PUNTOS'])
                return False
            
        except ValueError:
            messagebox.showerror('Error', Mensajes['ERROR_EVENTO_PUNTOS'])
            return False

        messagebox.showinfo('Éxito', Mensajes['EXITO_EVENTO_AGREGADO'])
        return True

if __name__ == "__main__":
    Abrir()
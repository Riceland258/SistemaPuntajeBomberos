import tkinter
from tkinter import ttk, messagebox
import mysql.connector

import facu_abm_personal
import martin_abm_eventos

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql',  
    'database': 'bomberos',
}

MENSAJES = {
    'ERROR_CAMPOS_VACIOS' : 'Complete todos los campos.',
    'ERROR_USUARIO'       : 'Usuario no encontrado.',
    'ERROR_PASS'          : 'Contraseña incorrecta.',
    'ERROR_ROL'           : 'Rol de usuario inexistente.',
}

PAD = 12
halfPAD = PAD // 2
squaredPAD = PAD ** 2

def Limpiar(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def Abrir():
    window = tkinter.Tk()
    window.title('Bomberos')
    window.resizable(False, False)
    window.state('zoomed')
    Menu_Login(window)
    window.mainloop()

def Redireccionar(window, rol):
    match rol:
        case '1':
            Menu_Root(window)
            
        case '2':
            pass
        
        case '3':
            pass
        
        case _:
            pass

def Menu_Root(window):
    Limpiar(window)
    window.title('Menú Principal - Root')
    
    # Frame principal
    frame_main = ttk.Frame(window, padding=(squaredPAD, PAD, squaredPAD, PAD), relief='ridge')
    frame_main.pack(fill='both', expand=True)

    Conexion_ = Conexion()
    eventos = Conexion_.Consultar_Eventos()

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
    frame_navegar = ttk.LabelFrame(frame_main, padding=(PAD, halfPAD, PAD, PAD), text='Navegar')
    frame_navegar.pack(fill='both', expand=False)

    buttons_navegar = ['Salir', 'Asistencias', 'Eventos', 'Personal', 'Recargar']
    for button in buttons_navegar:
        button_ = ttk.Button(frame_navegar, text=button)
        button_.pack(side='left', fill='x', expand=True, padx=(0, PAD) if button != buttons_navegar[-1] else 0)

        match button:
            case 'Salir':
                button_.config(command=lambda: Menu_Login(window))

            case 'Asistencias':
                pass

            case 'Eventos':
                button_.config(command=lambda: martin_abm_eventos.Abrir())

            case 'Personal':
                button_.config(command=lambda: facu_abm_personal.abrir_abm_personal())

            case 'Recargar':
                button_.config(command=lambda: Menu_Root(window))
    
def Menu_Login(window):
    Limpiar(window)
    window.title('Inicio de sesión')

    Conexion_ = Conexion()

    frame_main = ttk.Frame(window, padding=(PAD**2, PAD, PAD**2, PAD), relief='ridge')
    frame_main.pack(fill='both', expand=True)

    frame_usuario = ttk.LabelFrame(frame_main, padding=PAD, text='Usuario')
    frame_usuario.pack(fill='both', pady=(0, PAD))

    entry_usuario = ttk.Entry(frame_usuario)
    entry_usuario.pack(fill='x', expand=True)

    frame_contrasenia = ttk.LabelFrame(frame_main, padding=PAD, text='Contraseña')
    frame_contrasenia.pack(fill='both', pady=(0, PAD))

    entry_contrasenia = ttk.Entry(frame_contrasenia, show='*')
    entry_contrasenia.pack(fill='x', expand=True)

    button_login = ttk.Button(frame_main, text='Iniciar sesión', command=lambda: Redireccionar(window, Conexion_.Iniciar_Sesion(entry_usuario.get(), entry_contrasenia.get())))
    button_login.pack(fill='both', expand=True)

class Conexion:
    def __init__(self):
        self.DB = mysql.connector.connect(**DB_CONFIG)

    def Iniciar_Sesion(self, user, passw):
        crs = self.DB.cursor()

        if not user or not passw:
            messagebox.showerror('Error', MENSAJES['ERROR_CAMPOS_VACIOS'])
            return

        crs.execute('SELECT COUNT(*) FROM personal WHERE user = %s', (user,))
        if crs.fetchone()[0] == 0:
            messagebox.showerror('Error', MENSAJES['ERROR_USUARIO'])
            return

        crs.execute('SELECT COUNT(*) FROM personal WHERE user = %s AND pass = %s', (user, passw))
        if crs.fetchone()[0] == 0:
            messagebox.showerror('Error', MENSAJES['ERROR_PASS'])
            return
        
        crs.execute('SELECT rol FROM personal WHERE user = %s AND pass = %s', (user, passw))

        return crs.fetchone()[0]

    def Consultar_Eventos(self):
        crs = self.DB.cursor()
        crs.execute('SELECT * FROM eventos')

        return crs.fetchall()

if __name__ == '__main__':
    print('Administrador: admin / admin')
    Abrir()
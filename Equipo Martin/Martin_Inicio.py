import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'bomberos',
}

MENSAJES = {
    'ERROR_CAMPOS_VACIOS' : 'Complete todos los campos.',
    'ERROR_USUARIO'       : 'Usuario no encontrado.',
    'ERROR_PASS'          : 'Contraseña incorrecta.',
    'ERROR_ROL'           : 'Rol de usuario inexistente.',
}

PAD = 12

def Limpiar(frame):
    for widget in frame.winfo_children():
        widget.destroy()

class Menu_Login:
    def __init__(self, master=None):
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

        self.frame_usuario = ttk.Labelframe(self.frame, padding=PAD, text='Usuario')
        self.frame_usuario.pack(fill='both', expand=True)

        self.entry_usuario = ttk.Entry(self.frame_usuario)
        self.entry_usuario.pack(fill='x', expand=True)
        
        self.frame_contrasenia = ttk.Labelframe(self.frame, padding=PAD, text='Contraseña')
        self.frame_contrasenia.pack(fill='both', expand=True)

        self.entry_contrasenia = ttk.Entry(self.frame_contrasenia)
        self.entry_contrasenia.pack(fill='x', expand=True)

        self.button_login = ttk.Button(self.frame, text='Iniciar sesión', command=lambda: self.Iniciar_Sesion())
        self.button_login.pack(fill='both', expand=True)

    def Iniciar_Sesion(self):
        conexion = Conexion()
        user = conexion.Iniciar_Sesion(self.entry_usuario.get(), self.entry_contrasenia.get())

        match user:
            case 'root':
                Limpiar(self.root)
                Menu_Root(self.root)

class Menu_Root:
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

        self.frame_eventos = ttk.Labelframe(self.frame, text='Eventos')
        self.frame_eventos.pack()

        eventos = Conexion().Consultar_Eventos()
        print(eventos)

        # for i in range(len(eventos)):
        #     if i % 3 == 0:
        #         frame_eventos_sub = ttk.Frame(self.frame_eventos)
        #         frame_eventos_sub.pack(fill='both', expand=True)
                
        #     evento = eventos[i]
        #     button_evento = ttk.Button(frame_eventos_sub, text=f'{evento[1]}')
        #     button_evento.pack(fill='both', expand=True, side='left', padx=(0, PAD), pady=(0, PAD))

        self.frame_navegar = ttk.Labelframe(self.frame, text='Navegar')
        self.frame_navegar.pack()

        buttons_navegar = ['Salir', 'Asistencias', 'Eventos', 'Personal', 'Recargar']
        for button in buttons_navegar:
            button_ = ttk.Button(self.frame_navegar, text=button)
            button_.pack(side='left', fill='x', expand=True, padx=(0, PAD) if button != buttons_navegar[-1] else 0)

            match button:
                case 'Salir':
                    button_.config(command=lambda: [self.root.destroy(), Menu_Login()])

class Conexion:
    def __init__(self):
        try:
            self.DB = mysql.connector.connect(**DB_CONFIG)

        except:
            self.Generar_Datos()
            self.DB = mysql.connector.connect(**DB_CONFIG)
        

    def Generar_Datos(self):
        crs = self.DB.cursor()
        crs.execute("DROP DATABASE IF EXISTS bomberos")
        crs.execute("CREATE DATABASE bomberos")
        crs.execute("USE bomberos")

        # Ejecutar el script bomberos.sql
        with open('bomberos.sql', 'r', encoding='utf8') as file:
            sql_queries = file.read()

        for query in sql_queries.split(';'):
            try:
                if query.strip() != '':
                    crs.execute(query)
                    
            except Exception as e:
                print("Error executing query:", str(e))

        self.DB.commit()

        # Insertar datos en la tabla personal
        datos_personal = [
            (1, 'root', 0, 'root', 'root'),
            (2, 'user', 0, 'user', 'user')
        ]
        
        for nro_legajo, apellido_nombre, dni, user, password in datos_personal:
            crs.execute(f'INSERT INTO personal (nro_legajo, apellido_nombre, dni, user, pass) VALUES (%s, %s, %s, %s, %s)',
                        (nro_legajo, apellido_nombre, dni, user, password))

        self.DB.commit()

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
        
        crs.execute('SELECT user FROM personal WHERE user = %s AND pass = %s', (user, passw))

        return crs.fetchone()[0]

    def Consultar_Eventos(self):
        crs = self.DB.cursor()
        crs.execute('SELECT * FROM eventos')
        resultados = crs.fetchall()
        crs.close()
        return resultados

def Abrir():
    Menu_Login()

if __name__ == '__main__':
    Abrir()
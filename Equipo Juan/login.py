import tkinter as tk
from tkinter import ttk
import mysql.connector
from baseuni import DB_HOST, DB_NAME, DB_USER
import eventos_grupo_juan
import conducta_grupo_juan
import personal_grupo_juan
import cargar_planilla

conector = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USER,
    database = DB_NAME
)

def cerrarPrograma():
    root.destroy()
    
def menuPrincipal():
    menu = tk.Toplevel()
    menu.title("Bomberos Voluntarios Totoras")
    menu.attributes("-fullscreen", True)
    menu.config(background="#333")

    ttk.Label(menu, text="Seleccione lo que desee hacer", font=("arial", 25), foreground="#fff", background="#333").place(x=560, y=200)

    salir = tk.Button(menu, text="Menú principal", background="#FFA82B", width=20, height=2, command=menu.destroy)
    salir.place(x=700, y=550)
    
    tk.Button(menu, text="Eventos", background="#FFA82B", width=20, height=2, command=eventos_grupo_juan.menuEventos).place(x=290, y=350)
    tk.Button(menu, text="Personal", background="#FFA82B", width=20, height=2, command=personal_grupo_juan.menuPersonal).place(x=700, y=350)
    tk.Button(menu, text="Conducta", background="#FFA82B", width=20, height=2, command=conducta_grupo_juan.menuConducta).place(x=1090, y=350)
    
def validarLogIn():
    user = usuario.get()
    password = contra.get()
    
    if not user or not password:
        return
    
    cursor = conector.cursor()
    cursor.execute("SELECT user, pass FROM personal")
    datos = cursor.fetchall()
    cursor.close()
    
    for dato in datos:
        us = dato[0]
        pas = dato[1]
        if us == user and pas == password:
            try:
                cargar_planilla.menuBombero(user)
                return
            except:
                mensajeError = tk.Label(root, background="#333", text="Usuario o contraseña incorrectos!", foreground="#f00", font=("Arial", 20))
                mensajeError.place(x=580, y=550)
                mensajeError.after(1500, mensajeError.destroy)
                return
        elif user == "admin" and password == "admin":
            try:
                menuPrincipal()
                return
            except:
                mensajeError = tk.Label(root, background="#333", text="Usuario o contraseña incorrectos!", foreground="#f00", font=("Arial", 20))
                mensajeError.place(x=580, y=550)
                mensajeError.after(1500, mensajeError.destroy)
                return

root = tk.Tk()
root.title("Escuela comercio")
root.attributes("-fullscreen", True)
root.config(background="#333")

ttk.Label(root, text="Ingrese sus datos para iniciar sesión", font=("arial", 25), foreground="#fff", background="#333").place(x=500, y=200)

ttk.Label(root, text="Usuario", background="#333", foreground="#fff", font=("arial, 15")).place(x=725, y=280)

usuario = ttk.Entry(root, width=30)
usuario.place(x=665, y=320)

ttk.Label(root, text="Contraseña", background="#333", foreground="#fff", font=("arial, 15")).place(x=705, y=370)

contra = ttk.Entry(root, width=30)
contra.place(x=665, y=400)

login = tk.Button(root, text="Entrar", background="#FFA82B", width=10, command=validarLogIn)
login.place(x=720, y=450)

salir = tk.Button(root, text="Cerrar programa", background="#FFA82B", command=cerrarPrograma)
salir.place(x=710, y=500)

root.mainloop()
import mysql.connector
import Database as db
import tkinter as tk
from tkinter import ttk

DB = db.Conectar_DB()
PAD = 12

def Limpiar_ROOT(ROOT):
    for child in ROOT.winfo_children():
        child.destroy()

def Iniciar_Sesion(user, passw):
    crs = DB.cursor()
    crs.execute('SELECT rol FROM personal WHERE user = %s AND pass = %s', (user, passw))

    return crs.fetchone()[0]

def Eventos_Consultar():
    crs = DB.cursor()
    crs.execute('SELECT * FROM eventos')

    return crs.fetchall()


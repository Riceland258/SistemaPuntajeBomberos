import mysql.connector
import Database as db
import tkinter as tk
from tkinter import ttk

DB = db.Conectar_DB()

def Limpiar_ROOT(ROOT):
    for child in ROOT.winfo_children():
        child.destroy()

def Eventos_Consultar():
    crs = DB.cursor()
    crs.execute('SELECT * FROM eventos')

    return crs.fetchall()


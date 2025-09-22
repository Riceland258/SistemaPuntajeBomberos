# ======================= IMPORTACIONES ==========================
import mysql.connector

# ================ CONEXION CON LA BASE DE DATOS =================
def Conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bomberos"
    )

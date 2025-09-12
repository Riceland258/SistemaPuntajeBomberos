import mysql.connector
import Database as db

def Destruir_DB(DB):
    CURSOR = DB.cursor()
    CURSOR.execute('DROP DATABASE IF EXISTS bomberos')
    DB.commit()
    CURSOR.close()
    DB.close()

def Eventos_Consultar(DB):
    CURSOR = DB.cursor()
import mysql.connector

def Destruir_DB():
    db = mysql.connector.connect(host='localhost',
                                 user='root',
                                 password='')
    crs = db.cursor()

    crs.execute('DROP DATABASE IF EXISTS `bomberos`')
    db.commit()
    
    crs.close()
    db.close()
    print('Base de datos destruida.')

def Crear_DB():
    db = mysql.connector.connect(host='localhost',
                                 user='root',
                                 password='')
    
    crs = db.cursor()
    crs.execute('CREATE DATABASE IF NOT EXISTS `bomberos`')

    with open('bomberos.sql', 'r', encoding='utf8') as file:
        crs.execute(file.read(), multi=True)

        db.commit()

    print('Base de datos creada exitosamente.')

try:
    Destruir_DB()
    DB = mysql.connector.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='bomberos')
    CRS = DB.cursor()

except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        print("Base de datos no encontrada, creando 'bomberos'.")
        Crear_DB()

finally:
    DB = mysql.connector.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='bomberos')
    CRS = DB.cursor()
    print('Conexión a la base de datos establecida.')
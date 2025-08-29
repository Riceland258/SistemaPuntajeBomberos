import mysql.connector


def Crear_DB(config):
    temp_db = mysql.connector.connect(
        host = config['host'],
        user = config['user'],
        password = config['password'])

    cursor = temp_db.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {config['database']}')

    cursor.execute(f'USE {config['database']}')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Prueba (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero INT NOT NULL)''')

    cursor.close()
    temp_db.close()

def Destruir_DB():
    CURSOR.execute('DROP DATABASE IF EXISTS bomberos')
    DB.commit()
    CURSOR.close()
    DB.close()


DB_CONFIG = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '',
    'database' : 'bomberos'}

try:
    DB = mysql.connector.connect(**DB_CONFIG)

except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        print('La base de datos no existe. Creándola...')
        Crear_DB(DB_CONFIG)

finally:
    DB = mysql.connector.connect(**DB_CONFIG) # Conexión global a la base de datos
    CURSOR = DB.cursor() # Cursor global para ejecutar consultas
    print('Conexión exitosa a la base de datos.')
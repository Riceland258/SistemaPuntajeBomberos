import mysql.connector


def Crear_DB(config):
    db = mysql.connector.connect(
        host = config['host'],
        user = config['user'],
        password = config['password'])

    with open('bomberos.sql', 'r') as file:
        with db.cursor() as cursor:
            cursor.execute(file.read(), multi=True)

        db.commit()

    print('Base de datos creada exitosamente.')

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
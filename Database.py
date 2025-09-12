import mysql.connector
import os

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
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="")

    # Create a cursor to execute queries
    cursor = conn.cursor()

    # Open and read the SQL file
    cursor.execute('CREATE DATABASE `bomberos`')
    
    with open('bomberos.sql', 'r', encoding='utf8') as file:
        sql_queries = file.read()

    # Split the SQL file content into individual queries
    queries = sql_queries.split(';')

    # Iterate over the queries and execute them
    for query in queries:
        try:
            if query.strip() != '':
                cursor.execute(query)
                conn.commit()
                
        except Exception as e:
            print("Error executing query:", str(e))

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

def Poblar_DB(DB):
    CRS = DB.cursor()

    eventos = [
        (1, 'Evento1', 1),
        (2, 'Evento2', 2),
        (3, 'Evento3', 3)
    ]

    for id_evento, evento, puntos in eventos:
        CRS.execute('INSERT INTO `eventos` (id_evento, evento, puntos) VALUES (%s, %s, %s)',
                    (id_evento, evento, puntos))

    DB.commit()

def Conectar_DB():
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
        print('Conexión a la base de datos establecida.')
        Poblar_DB(DB)

        return DB
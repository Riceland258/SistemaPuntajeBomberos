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
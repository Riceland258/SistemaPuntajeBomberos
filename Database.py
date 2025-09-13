import mysql.connector
import os
import random

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'bomberos',
}

def Destruir_DB():
    db = mysql.connector.connect(**{k: v for k, v in DB_CONFIG.items() if k != 'database'})  # Conectar sin especificar la base de datos
    crs = db.cursor()

    crs.execute('DROP DATABASE IF EXISTS `bomberos`')
    db.commit()
    
    crs.close()
    db.close()
    print('Base de datos destruida.')

def Crear_DB():
    db = mysql.connector.connect(**{k: v for k, v in DB_CONFIG.items() if k != 'database'})

    # Create a cursor to execute queries
    cursor = db.cursor()

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
                db.commit()
                
        except Exception as e:
            print("Error executing query:", str(e))

    # Close the cursor and the database connection
    cursor.close()
    db.close()

# CREATE TABLE `personal` (
#   `nro_legajo` int(10) NOT NULL,
#   `apellido_nombre` varchar(100) NOT NULL,
#   `dni` int(8) NOT NULL,
#   `user` varchar(20) NOT NULL,
#   `pass` varchar(8) NOT NULL
# )

def Poblar_DB(DB):
    CRS = DB.cursor()

    eventos = [
        (1, 'Evento1', 1),
        (2, 'Evento2', 2),
        (3, 'Evento3', 3),
        (4, 'Evento4', 4),
        (5, 'Evento5', 5),
    ]
    
    personal_nombres = ['Alberto', 'Bruno', 'Carlos', 'Diego', 'Esteban', 'Facundo', 'Gustavo', 'Hernan', 'Ignacio', 'Javier']
    personal_apellidos = ['Gomez', 'Fernandez', 'Lopez', 'Martinez', 'Garcia', 'Rodriguez', 'Sanchez', 'Ramirez', 'Torres', 'Flores']
    random.seed(0)  # Fijar la semilla para reproducibilidad
    
    for i in range(21):
        nro_legajo = i + 100
        apellido_nombre = f"{random.choice(personal_apellidos)} {random.choice(personal_nombres)}"
        dni = random.randint(30000000, 50000000)
        user = f"user{i}"
        password = str(random.randint(1000, 9999))
        
        CRS.execute('INSERT INTO `personal` (nro_legajo, apellido_nombre, dni, user, pass) VALUES (%s, %s, %s, %s, %s)',
                    (nro_legajo, apellido_nombre, dni, user, password))
    
    DB.commit()

    for id_evento, evento, puntos in eventos:
        CRS.execute('INSERT INTO `eventos` (id_evento, evento, puntos) VALUES (%s, %s, %s)',
                    (id_evento, evento, puntos))

    DB.commit()

def Conectar_DB():
    try:
        Destruir_DB()
        DB = mysql.connector.connect(**DB_CONFIG)

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Base de datos no encontrada, creando 'bomberos'.")
            Crear_DB()
        
        elif err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error de acceso: nombre de usuario o contraseña incorrectos.")
            
        elif err.errno == mysql.connector.errorcode.ER_BAD_HOST_ERROR:
            print("Error de host")
            
        elif err.errno == mysql.connector.errorcode.CR_CONN_HOST_ERROR:
            print("Error de conexión a la base de datos. ¿Está abierto XAMPP?")
        
        else:
            print(f"Otro error al conectar a la base de datos: {err}")

    else:
        DB = mysql.connector.connect(**DB_CONFIG)
        print('Conexión a la base de datos establecida.')
        Poblar_DB(DB)

        return DB
    
    finally:
        raise SystemExit('No se pudo conectar a la base de datos.')
import random
import Database as Conexion

# Genera una lista de 10 números aleatorios entre 1 y 100
datos = [random.randint(1, 100) for _ in range(10)]
print("Números aleatorios:", datos)

# Inserta los números generados en la tabla Prueba de la base de datos
for numero in datos:
    Conexion.CURSOR.execute('INSERT INTO Prueba (numero) VALUES (%s)', (numero,))
Conexion.DB.commit()

# Recupera y muestra los números almacenados en la base de datos
Conexion.CURSOR.execute('SELECT numero FROM Prueba')

resultados = Conexion.CURSOR.fetchall()

print('Números en la base de datos:', end=' ')
for (numero,) in resultados:
    print(numero, end=' ')
print()

# Destruye la base de datos y cierra la conexión
Conexion.Destruir_DB()
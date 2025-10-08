import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'bomberosrell',
}

class DB():
    def __init__(self):
        try:
            self.DB = mysql.connector.connect(**DB_CONFIG)

        except:
            print('Fallo en la conexión')

    def get(self):
        return self.DB

    def close(self):
        self.DB.close()

class Personal:
    def __init__(self):
        self.DB = DB().get()
        self.CUR = self.DB.cursor()

    def getAll(self):
        self.CUR.execute('''
            SELECT nro_legajo, apellido_nombre, dni
            FROM personal
            ''')

        query = self.CUR.fetchall()
        personal = {}

        for nro_legajo, apellido_nombre, dni in query:
            datos = {
                'apellido_nombre' : apellido_nombre,
                'dni' : dni
            }
            personal[nro_legajo] = datos

        return personal

class Eventos:
    def __init__(self):
        self.DB = DB().get()
        self.CUR = self.DB.cursor()
        
    def getAll(self):
        self.CUR.execute('''
                SELECT id_evento, evento, puntos
                FROM eventos
                ''')

        query = self.CUR.fetchall()
        eventos = {}

        for id_evento, evento, puntos in query:
            datos = {
                'evento' : evento,
                'puntos' : puntos
            }
            eventos[id_evento] = datos

        return eventos

class Asistencias:
    def __init__(self):
        self.DB = DB().get()
        self.CUR = self.DB.cursor()

    def getAll(self):
        self.CUR.execute('''
            WITH cantidad_eventos AS (
                SELECT cab.id_evento, COUNT(*) AS cantidad
                FROM asistencia_evento_cabecera cab
                GROUP BY cab.id_evento ),
                
            puntajes AS (
                SELECT 
                    det.nro_legajo,
                    cab.id_evento,
                    COUNT(*) AS asistencias,
                    ce.cantidad,
                    e.puntos,
                    COUNT(*) / ce.cantidad * e.puntos AS calculo
                FROM asistencia_evento_cabecera cab
                JOIN asistencia_evento_detalle det ON cab.id_asistencia_cabecera = det.id_asistencia_cabecera
                JOIN cantidad_eventos ce ON ce.id_evento = cab.id_evento
                JOIN eventos e ON e.id_evento = cab.id_evento
                GROUP BY det.nro_legajo, cab.id_evento )
                
            SELECT
                nro_legajo,
                GROUP_CONCAT(
                    CONCAT_WS(',', id_evento, asistencias, cantidad, calculo)
                    ORDER BY id_evento
                    SEPARATOR ';') AS eventos
            FROM puntajes
            GROUP BY nro_legajo
            ORDER BY nro_legajo;''')

        query = self.CUR.fetchall()

        asistencias = {}

        for nro_legajo, eventos in query:
            puntajes = {}
            for evento in eventos.split(';'):
                id_evento, presentes, cantidad, calculo = evento.split(',')
                puntajes_dict = {
                    'asistencias' : int(presentes),
                    'cantidad' : int(cantidad),
                    'calculo' : float(calculo)
                }
                puntajes[int(id_evento)] = puntajes_dict
            
            asistencias[nro_legajo] = puntajes

        return asistencias

if __name__ == '__main__':
    pass
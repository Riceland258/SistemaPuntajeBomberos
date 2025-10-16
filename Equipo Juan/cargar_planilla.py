from ttkwidgets import CheckboxTreeview
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import Calendar
import mysql.connector
from baseuni import DB_HOST, DB_NAME, DB_USER

conector = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USER,
    database = DB_NAME
)

bombeAsistidos = []
bombeLicencia = []
idLicencia = []

def menuBombero(usuario):
    bombero = tk.Toplevel()
    bombero.title("Bomberos Voluntarios Totoras")
    bombero.attributes("-fullscreen", True)
    bombero.config(background="#333")
    
    cursor = conector.cursor()
    cursor.execute("SELECT eventos.id_evento, eventos.evento FROM eventos")
    eventosData = cursor.fetchall()
    cursor.close()
    
    cursor = conector.cursor()
    cursor.execute("SELECT nro_legajo, apellido_nombre FROM personal")
    personalData = cursor.fetchall()
    cursor.close()
    
    cursor = conector.cursor()
    cursor.execute("SELECT `id_unidad`, `nombre` FROM `unidades`")
    unidadData = cursor.fetchall()
    cursor.close()
    
        
    mapaUnidad = {f"{nombre}": id_unidad for id_unidad, nombre in unidadData}
    mapaEventos = {f"{evento}": id_evento for id_evento, evento in eventosData}
    mapaPersonal = {f"{apellido_nombre}": nro_legajo for nro_legajo, apellido_nombre in personalData}
    
    ttk.Label(bombero, text="Cargar planilla", font=("arial", 20), foreground="#fff", background="#333").place(x=650, y=100)
    
    tk.Label(bombero, text="Evento:", foreground="#fff", background="#333", font=('arial', 10)).place(x=620, y=200)
    comboEventos = ttk.Combobox(bombero, state="readonly", values=list(mapaEventos.keys()), width=27)
    comboEventos.place(x=680, y=200)
    
    tk.Label(bombero, text="Unidad:", foreground="#fff", background="#333", font=('arial', 10)).place(x=620, y=250)
    comboUnidad = ttk.Combobox(bombero, state="readonly", values=list(mapaUnidad.keys()), width=27)
    comboUnidad.place(x=680, y=250)
    
    tk.Label(bombero, text="Fecha:", foreground="#fff", background="#333", font=('arial', 10)).place(x=622, y=300)
    fechaEvento = Calendar(bombero, selectmode="day", year=2025, month=10, day=8)
    fechaEvento.place(x=680, y=300)
    
    tk.Label(bombero, text="Descripción:", foreground="#fff", background="#333", font=('arial', 10)).place(x=600, y=550)
    descSalida = tk.Entry(bombero, width=27)
    descSalida.place(x=680, y=550)
    
    def cargarAsistencias():
        asistencia = tk.Toplevel()
        asistencia.title("Seleccionar asistencias")
        asistencia.geometry("500x500")
        asistencia.config(background="#333")
        
        i = 1
        
        tk.Label(asistencia, text="Asistencias", foreground="#fff", background="#333", font=('arial', 15)).place(x=200, y=50)
        asistencias = CheckboxTreeview(asistencia)
        asistencias.place(x=150, y=110)
        
        for personal in mapaPersonal:
            asistencias.insert("", "end", {i}, text=personal)
            i = i + 1
    
        def validarAsis():
            obtenerAsistencias = asistencias.get_checked()
            if obtenerAsistencias:
                for iid in obtenerAsistencias:
                    asistencias2 = asistencias.item(iid, "text")
                    bombeAsistidos.append(asistencias2)
            mensajeExito = tk.Label(asistencia, background="#333", text="Las asistencias se guardaron con éxito!", foreground="#0f0", font=("Arial", 15))
            mensajeExito.place(x=100, y=350)
            asistencia.after(2000, asistencia.destroy)
        
        tk.Button(asistencia, text="Guardar asistencia", background="#FFA82B", width=20, height=2, command=validarAsis).place(x=170, y=400)
    
    def cargarLicencias():
        licencia = tk.Toplevel()
        licencia.title("Seleccionar licencias")
        licencia.geometry("500x500")
        licencia.config(background="#333")
        
        i = 1
        
        tk.Label(licencia, text="Licencias", foreground="#fff", background="#333", font=('arial', 15)).place(x=200, y=50)
        licencias = CheckboxTreeview(licencia)
        licencias.place(x=150, y=110)
        
        for personal in mapaPersonal:
            licencias.insert("", "end", {i}, text=personal)
            i = i + 1
        
    
        def validarLicen():
            obtenerLicencias = licencias.get_checked()
            if obtenerLicencias:
                for iid in obtenerLicencias:
                    licencias2 = licencias.item(iid, "text")
                    bombeLicencia.append(licencias2)
                
                cursor = conector.cursor()    
                for bombeLicen in bombeLicencia:
                    cursor.execute("SELECT `nro_legajo` FROM `personal` WHERE apellido_nombre = %s", (bombeLicen,))
                    bomberito = cursor.fetchone()
                    idLicencia.append(bomberito)
                cursor.close()
            mensajeExito = tk.Label(licencia, background="#333", text="Las licencias se guardaron con éxito!", foreground="#0f0", font=("Arial", 15))
            mensajeExito.place(x=100, y=350)
            licencia.after(2000, licencia.destroy)
        
        tk.Button(licencia, text="Guardar Licencias", background="#FFA82B", width=20, height=2, command=validarLicen).place(x=170, y=400)
    
    def validacionFinal():
        seleccion1 = comboEventos.get()
        seleccion2 = fechaEvento.get_date()
        seleccion4 = comboUnidad.get()
        data3 = descSalida.get()
        
        fechaCorrecta = datetime.strptime(seleccion2, "%m/%d/%y").strftime("%Y/%m/%d")
        
        validacionNumero = False
        
        try:
            int(data3)
        except:
            validacionNumero = True
        
        eventoSeleccionado = mapaEventos[seleccion1]
        unidadSeleccionada = mapaUnidad[seleccion4]
        
        cursor = conector.cursor()
        cursor.execute("SELECT e.id_evento FROM eventos e WHERE e.id_evento = %s", (eventoSeleccionado,))
        idEve = cursor.fetchone()
        cursor.close()
        
        cursor = conector.cursor()
        cursor.execute("SELECT p.nro_legajo FROM personal p WHERE p.user = %s", (usuario,))
        responsable = cursor.fetchone()
        cursor.close()
        
        cursor = conector.cursor()
        cursor.execute("SELECT u.id_unidad FROM unidades u WHERE u.id_unidad = %s", (unidadSeleccionada,))
        idUni = cursor.fetchone()
        cursor.close()
        
        idAsistidos = []
        
        cursor = conector.cursor()
        for asistencia in bombeAsistidos:
            cursor.execute("SELECT `nro_legajo` FROM `personal` WHERE apellido_nombre = %s", (asistencia,))
            bomberito = cursor.fetchone()
            idAsistidos.append(bomberito)
        cursor.close()
        
        if not seleccion1 or not seleccion2 or not data3 or not bombeLicencia or not bombeAsistidos or not seleccion4:
            mensajeError = tk.Label(bombero, background="#333", text="Complete todos los datos", foreground="#f00", font=("Arial", 15))
            mensajeError.place(x=650, y=600)
            mensajeError.after(1500, mensajeError.destroy)
        elif validacionNumero == False:
            mensajeError = tk.Label(bombero, background="#333", text="Ingrese una descripción acorde!", foreground="#f00", font=("Arial", 15))
            mensajeError.place(x=650, y=600)
            mensajeError.after(1500, mensajeError.destroy)
        elif idAsistidos == None or not idAsistidos:
            mensajeError = tk.Label(bombero, background="#333", text="Debe ingresar al meno un bombero!", foreground="#f00", font=("Arial", 15))
            mensajeError.place(x=620, y=600)
            mensajeError.after(1500, mensajeError.destroy)
        else:
            cursor = conector.cursor()
            cursor.execute("""
                INSERT INTO asistencia_evento_cabecera (id_evento, fecha, confirmada, nro_legajo_responsable, descripcion)
                VALUES (%s, %s, 'N', %s, %s)
            """, (idEve[0], fechaCorrecta, responsable[0], data3))

            eventoActual = cursor.lastrowid
            conector.commit()
            cursor.close()
            
            for idAsi in idAsistidos:
                cursor = conector.cursor()
                cursor.execute("INSERT INTO `asistencia_evento_detalle`(`nro_legajo`, `licencia`, `id_asistencia_cabecera`, `id_unidad`) VALUES (%s, 'N', %s, %s)", (idAsi[0], eventoActual, idUni[0]))
                conector.commit()
                cursor.close()
            
            for idLic in idLicencia:
                cursor = conector.cursor()
                cursor.execute("INSERT INTO `asistencia_evento_detalle`(`nro_legajo`, `licencia`, `id_asistencia_cabecera`) VALUES (%s, 'S', %s)", (idLic[0], eventoActual))
                conector.commit()
                cursor.close()
            
            mensajeExito = tk.Label(bombero, background="#333", text="La planilla se agregó con éxito!", foreground="#0f0", font=("Arial", 15))
            mensajeExito.place(x=650, y=600)
            mensajeExito.after(1500, mensajeExito.destroy)
    
    tk.Button(bombero, text="Cargar asistencias", background="#FFA82B", width=20, height=2, command=cargarAsistencias).place(x=400, y=800)
    tk.Button(bombero, text="Subir", background="#FFA82B", width=20, height=2, command=validacionFinal).place(x=600, y=800)
    tk.Button(bombero, text="Salir", background="#FFA82B", width=20, height=2, command=bombero.destroy).place(x=800, y=800)
    tk.Button(bombero, text="Cargar licencias", background="#FFA82B", width=20, height=2, command=cargarLicencias).place(x=1000, y=800)
    
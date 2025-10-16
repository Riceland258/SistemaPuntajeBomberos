import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

conector = mysql.connector.connect(
    host = "localhost",
    user = "root",
    database = "bomberos"
)

def menuEventos():
    eventos = tk.Toplevel()
    eventos.title("ABM EVENTOS")
    eventos.config(bg="#333")
    eventos.attributes("-fullscreen", True)
    
    tk.Label(eventos, text="ABM Eventos", foreground="#fff", background="#333", font=('arial', 20)).place(x=680, y=200)
    tk.Label(eventos, text="Cargar evento", foreground="#fff", background="#333", font=('arial', 15)).place(x=300, y=300)
    tk.Label(eventos, text="Modificar evento", foreground="#fff", background="#333", font=('arial', 15)).place(x=700, y=300)
    tk.Label(eventos, text="Eliminar evento", foreground="#fff", background="#333", font=('arial', 15)).place(x=1100, y=300)

    def formulario_evento():
        form = tk.Toplevel()
        form.title("Agregar Evento")
        form.geometry("500x500")
        form.config(background="#333")  
        
        tk.Label(form, text="Rellene los campos con los datos: ", foreground="#fff", background="#333", font=('arial', 15)).pack()
        
        tk.Label(form, text="ID Evento", background="#333", foreground="#fff").pack(pady = 10)
        entryid = tk.Entry(form, width=27)
        entryid.pack()
        tk.Label(form, text="Evento:", foreground="#fff", background="#333", font=('arial', 10)).pack(pady = 10)
        entryeve = tk.Entry(form, width=27)
        entryeve.pack()
        tk.Label(form, text="Puntos:", background="#333", foreground="#fff", font=('arial', 10)).pack(pady =10)
        entrypun = tk.Entry(form, width=27)
        entrypun.pack()

        def guardar():
            try:
                id_evento_val = entryid.get().strip()
                evento_val = entryeve.get().strip()
                puntos_val = entrypun.get().strip()
                
                if not id_evento_val or not evento_val or not puntos_val:
                    messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
                    return
                
                if not puntos_val.isdigit():
                    messagebox.showwarning("Atención", "El campo 'Puntos' debe ser un número entero.")
                    return
                
                cursor = conector.cursor()

                sql = "INSERT INTO eventos (id_evento, evento, puntos) VALUES (%s, %s, %s)"
                cursor.execute(sql, (id_evento_val, evento_val, puntos_val))
                conector.commit()
                cursor.close()
                conector.close()

                messagebox.showinfo("Éxito", "Evento guardado correctamente")
                form.destroy()

            except mysql.connector.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    messagebox.showerror("Error", f"Ya existe un evento con el ID {id_evento_val}.")
                else:
                    messagebox.showerror("Error de BD", str(e))

            except Exception as e:
                messagebox.showerror("Error inesperado", str(e))
        tk.Button(form, text="Guardar", command=guardar, background="#FFA82B", font=('arial', 10)).pack(pady=15)   
    def modificarEventos():
        evento = tk.Toplevel()
        evento.title("Modificar Evento")
        evento.geometry("500x500")
        evento.config(bg="#333")
        
        cursor = conector.cursor()
        cursor.execute("SELECT eventos.id_evento, eventos.evento FROM eventos")
        eventosData = cursor.fetchall()
        cursor.close()
        
        mapaEventos = {f"{evento}": id_evento for id_evento, evento in eventosData}
        
        tk.Label(evento, text="Seleccione el evento a modificar", foreground="#fff", background="#333", font=('arial', 15)).place(x=100, y=80)
        
        tk.Label(evento, text="Evento:", foreground="#fff", background="#333", font=('arial', 10)).place(x=120, y=140)
        comboEventos = ttk.Combobox(evento, state="readonly", values=list(mapaEventos.keys()), width=27)
        comboEventos.place(x=180, y=140)
        
        tk.Label(evento, text="ID:", background="#333", foreground="#fff").place(x=147, y=190)
        idE = tk.Entry(evento, width=27)
        idE.place(x=180, y=190)
                
        tk.Label(evento, text="Nombre:", background="#333", foreground="#fff").place(x=115, y=220)
        nombreE = tk.Entry(evento, width=27)
        nombreE.place(x=180, y=220)
                
        tk.Label(evento, text="Puntos:", background="#333", foreground="#fff").place(x=123, y=250)
        puntos = tk.Entry(evento, width=27)
        puntos.place(x=180, y=250)
        
        def elegirEvento():
            seleccion = comboEventos.get()
            if not seleccion:
                return
            
            eventoSeleccionado = mapaEventos[seleccion]
            
            cursor = conector.cursor()
            cursor.execute("SELECT * FROM eventos WHERE eventos.id_evento = %s", (eventoSeleccionado,))
            datos = cursor.fetchone()
            cursor.close()

            if not datos:
                return
        
            idData, nombreData, puntosData = datos
            
            idE.delete(0, tk.END)
            idE.insert(0, idData)

            nombreE.delete(0, tk.END)
            nombreE.insert(0, nombreData)

            puntos.delete(0, tk.END)
            puntos.insert(0, puntosData)
            
            def actualizarDatos():
                validacionNumero = True
                validacionNombre = all(palabra.isalpha() for palabra in nombreE.get().split())
                validacionId = True
                
                try:
                    int(puntos.get())
                except:
                    validacionNumero = False
                    
                try:
                    int(idE.get())
                except:
                    validacionId = False
                    
                if not idE.get() or not nombreE.get() or not puntos.get():
                    mensajeError = tk.Label(evento, background="#333", text="Complete todos los datos", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=130, y=290)
                    mensajeError.after(1500, mensajeError.destroy)
                elif validacionNumero == False:
                    mensajeError = tk.Label(evento, background="#333", text="Ingrese un puntaje válido", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=150, y=290)
                    mensajeError.after(1500, mensajeError.destroy)
                elif validacionId == False:
                    mensajeError = tk.Label(evento, background="#333", text="Ingrese un ID válido", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=180, y=290)
                    mensajeError.after(1500, mensajeError.destroy)
                elif validacionNombre == False:
                    mensajeError = tk.Label(evento, background="#333", text="Ingrese un nombre de evento válido", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=120, y=290)
                    mensajeError.after(1500, mensajeError.destroy)
                else:
                    cursor = conector.cursor()
                    cursor.execute("UPDATE eventos SET id_evento=%s, evento=%s, puntos=%s WHERE id_evento = %s", (idE.get(), nombreE.get(), puntos.get(), eventoSeleccionado))
                    conector.commit()
                    cursor.close()
        
                    mensajeExito = tk.Label(evento, background="#333", text="El evento se modificó con éxito", foreground="#0f0", font=("Arial", 15))
                    mensajeExito.place(x=120, y=290)
                    mensajeExito.after(1500, mensajeExito.destroy)
                    
                    idE.delete(0, tk.END)
                    nombreE.delete(0, tk.END)
                    puntos.delete(0, tk.END)
                
            tk.Button(evento, text="Modificar", background="#FFA82B", width=10, command=actualizarDatos).place(x=220, y=350)
        
        tk.Button(evento, text="Seleccionar", background="#FFA82B", command=elegirEvento).place(x=380, y=137)   
    def eliminarEvento():
        eventos = tk.Toplevel()
        eventos.title("Eliminar Evento")
        eventos.geometry("500x400")
        eventos.config(bg="#333")

        cursor = conector.cursor()
        cursor.execute("SELECT id_evento, evento, puntos FROM eventos")
        eventosData = cursor.fetchall()
        cursor.close()

        mapaEventos = {evento: (id_evento, puntos) for id_evento, evento, puntos in eventosData}

        tk.Label(eventos, text="Seleccione el evento a eliminar",
                fg="#fff", bg="#333", font=('arial', 15)).pack(pady=20)

        comboEventos = ttk.Combobox(eventos, state="readonly", values=list(mapaEventos.keys()), width=40)
        comboEventos.pack(pady=10)

        infoEvento = tk.Label(eventos, text="", fg="#fff", bg="#333", font=("Arial", 12))
        infoEvento.pack(pady=10)

        def mostrarDetalles(_=None):
            seleccion = comboEventos.get()
            if not seleccion:
                infoEvento.config(text="")
                return
            id_evento, puntos = mapaEventos[seleccion]
            infoEvento.config(
                text=f"ID: {id_evento}\nEvento: {seleccion}\nPuntos: {puntos}",
                fg="#fff"
            )

        comboEventos.bind("<<ComboboxSelected>>", mostrarDetalles)

        def borrarEvento():
            seleccion = comboEventos.get()
            if not seleccion:
                return

            id_evento, _ = mapaEventos[seleccion]

            confirmar = tk.messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Seguro que desea eliminar el evento:\n\n'{seleccion}'?"
            )
            if not confirmar:
                return

            try:
                cursor = conector.cursor()
                cursor.execute("DELETE FROM eventos WHERE id_evento=%s", (id_evento,))
                conector.commit()
                cursor.close()

                tk.messagebox.showinfo("Éxito", f"Evento '{seleccion}' eliminado correctamente.")

                # Refrescar combobox
                comboEventos.set("")
                comboEventos["values"] = [ev for ev in mapaEventos.keys() if ev != seleccion]
                infoEvento.config(text="")
                mapaEventos.pop(seleccion)

            except Exception as e:
                tk.messagebox.showerror("Error", f"No se pudo eliminar el evento.\n\n{e}")

        tk.Button(eventos, text="Eliminar", background="#FFA82B", width=20, height=2,command=borrarEvento).pack(pady=20)

        tk.Button(eventos, text="Cerrar", background="#FFA82B", width=20, height=2, command=eventos.destroy).pack(pady=10)
    

    tk.Button(eventos, text="Añadir evento", background="#FFA82B", width=20, height=2, command=formulario_evento ).place(x=290, y=350)
    tk.Button(eventos, text="Modificar evento", background="#FFA82B", width=20, height=2, command= modificarEventos).place(x=700, y=350)
    tk.Button(eventos, text="Eliminar evento", background="#FFA82B", width=20, height=2, command = eliminarEvento).place(x=1090, y=350)
    tk.Button(eventos, text="Volver", background="#FFA82B", width=20, height=2, command=eventos.destroy).place(x=700, y=550)
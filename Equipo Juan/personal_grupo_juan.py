import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

conector = mysql.connector.connect(
    host = "localhost",
    user = "root",
    database = "bomberos"
)

def menuPersonal():
    personal = tk.Toplevel()
    personal.title("ABM personal")
    personal.config(bg="#333")
    personal.attributes("-fullscreen", True)
    
    tk.Label(personal, text="ABM Bomberos", foreground="#fff", background="#333", font=('arial', 20)).place(x=680, y=200)
    tk.Label(personal, text="Agregar bombero", foreground="#fff", background="#333", font=('arial', 15)).place(x=280, y=300)
    tk.Label(personal, text="Modificar bombero", foreground="#fff", background="#333", font=('arial', 15)).place(x=680, y=300)
    tk.Label(personal, text="Eliminar bombero", foreground="#fff", background="#333", font=('arial', 15)).place(x=1080, y=300)

    def formulario_evento():
        bombero = tk.Toplevel()
        bombero.title("Agregar Evento")
        bombero.geometry("500x500")
        bombero.config(background="#333")  
        
        tk.Label(bombero, text="Rellene los campos con los datos: ", foreground="#fff", background="#333", font=('arial', 15)).place(x=100, y=100)
        
        ttk.Label(bombero, text="Número legajo:", background="#333", foreground="#fff").place(x=70, y=190)
        nroLegajo = tk.Entry(bombero, width=27)
        nroLegajo.place(x=180, y=190)
                
        tk.Label(bombero, text="Apellido y nombre:", background="#333", foreground="#fff").place(x=52, y=220)
        nombreB = tk.Entry(bombero, width=27)
        nombreB.place(x=180, y=220)
                
        tk.Label(bombero, text="DNI:", background="#333", foreground="#fff").place(x=130, y=250)
        dniB = tk.Entry(bombero, width=27)
        dniB.place(x=180, y=250)
        
        tk.Label(bombero, text="Usuario:", background="#333", foreground="#fff").place(x=110, y=280)
        usuario = tk.Entry(bombero, width=27)
        usuario.place(x=180, y=280)
        
        tk.Label(bombero, text="Contraseña:", background="#333", foreground="#fff").place(x=90, y=310)
        contraseña = tk.Entry(bombero, width=27)
        contraseña.place(x=180, y=310)

        def guardar():
            try:
                nroLegajoBombero = nroLegajo.get().strip()
                nombreBombero = nombreB.get().strip()
                dniBombero = dniB.get().strip()
                userBombero = usuario.get().strip()
                passBombero = contraseña.get().strip()
                
                if not nroLegajoBombero or not nombreBombero or not dniBombero or not userBombero or not passBombero:
                    mensajeError = tk.Label(bombero, background="#333", text="Complete todos los datos", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=130, y=350)
                    mensajeError.after(1500, mensajeError.destroy)
                    return
                
                if not dniBombero.isdigit():
                    mensajeError = tk.Label(bombero, background="#333", text="Ingrese un DNI válido", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=145, y=350)
                    mensajeError.after(1500, mensajeError.destroy)
                    return
                
                cursor = conector.cursor()
                cursor.execute("INSERT INTO personal(nro_legajo, apellido_nombre, dni, user, pass) VALUES (%s, %s, %s, %s, %s)", (nroLegajoBombero, nombreBombero, dniBombero, userBombero, passBombero))
                conector.commit()
                cursor.close()
                conector.close()

                messagebox.showinfo("Éxito", "Bombero agregado correctamente")
                bombero.destroy()

            except mysql.connector.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    mensajeError = tk.Label(bombero, background="#333", text="Ya existe un bombero con ese número de legajo", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=80, y=350)
                    mensajeError.after(1500, mensajeError.destroy)
                else:
                    messagebox.showerror("Error de BD", str(e))

            except Exception as e:
                messagebox.showerror("Error inesperado", str(e))
        tk.Button(bombero, text="Guardar", background="#FFA82B", width=10, font=('arial', 10), command=guardar).place(x=200 ,y=400) 
    def modificarPersonal():
        bombero = tk.Toplevel()
        bombero.title("Modificar Personal")
        bombero.geometry("500x500")
        bombero.config(bg="#333")
        
        cursor = conector.cursor()
        cursor.execute("SELECT personal.nro_legajo, personal.apellido_nombre FROM personal")
        personalData = cursor.fetchall()
        cursor.close()
        
        mapaPersonal = {f"{apellido_nombre}": nro_legajo for nro_legajo, apellido_nombre in personalData}
        
        tk.Label(bombero, text="Seleccione el bombero a modificar", foreground="#fff", background="#333", font=('arial', 15)).place(x=100, y=80)
        
        tk.Label(bombero, text="Bombero:", foreground="#fff", background="#333", font=('arial', 10)).place(x=105, y=140)
        comboBombero = ttk.Combobox(bombero, state="readonly", values=list(mapaPersonal.keys()), width=24)
        comboBombero.place(x=180, y=140)
        
        tk.Label(bombero, text="Número legajo:", background="#333", foreground="#fff").place(x=70, y=190)
        nroLegajo = tk.Entry(bombero, width=27)
        nroLegajo.place(x=180, y=190)
                
        tk.Label(bombero, text="Apellido y nombre:", background="#333", foreground="#fff").place(x=52, y=220)
        nombreB = tk.Entry(bombero, width=27)
        nombreB.place(x=180, y=220)
                
        tk.Label(bombero, text="DNI:", background="#333", foreground="#fff").place(x=130, y=250)
        dniB = tk.Entry(bombero, width=27)
        dniB.place(x=180, y=250)
        
        tk.Label(bombero, text="Usuario:", background="#333", foreground="#fff").place(x=110, y=280)
        usuario = tk.Entry(bombero, width=27)
        usuario.place(x=180, y=280)
        
        tk.Label(bombero, text="Contraseña:", background="#333", foreground="#fff").place(x=90, y=310)
        contraseña = tk.Entry(bombero, width=27)
        contraseña.place(x=180, y=310)
        
        def elegirBombero():
            seleccion = comboBombero.get()
            if not seleccion:
                return
            
            bomberoSeleccionado = mapaPersonal[seleccion]
            
            cursor = conector.cursor()
            cursor.execute("SELECT * FROM personal WHERE personal.nro_legajo = %s", (bomberoSeleccionado,))
            datos = cursor.fetchone()
            cursor.close()

            if not datos:
                return
        
            legajoData, nombreData, dniData, userData, passData = datos
            
            nroLegajo.delete(0, tk.END)
            nroLegajo.insert(0, legajoData)

            nombreB.delete(0, tk.END)
            nombreB.insert(0, nombreData)

            dniB.delete(0, tk.END)
            dniB.insert(0, dniData)
            
            usuario.delete(0, tk.END)
            usuario.insert(0, userData)
            
            contraseña.delete(0, tk.END)
            contraseña.insert(0, passData)
            
            def actualizarDatos():
                validacionDni = True
                validacionNombre = all(palabra.isalpha() for palabra in nombreB.get().split())
                validacionId = True
                length = len(dniB.get())
                
                try:
                    int(dniB.get())
                except:
                    validacionDni = False
                    
                try:
                    int(nroLegajo.get())
                except:
                    validacionId = False
                    
                if nroLegajo.get() == "" or nombreB.get() == "" or dniB.get() == "" or usuario.get() == "" or contraseña.get() == "":
                    mensajeError = tk.Label(bombero, background="#333", text="Complete todos los datos", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=130, y=360)
                    mensajeError.after(1500, mensajeError.destroy)
                elif validacionDni == False or length < 8 or length > 9:
                    mensajeError = tk.Label(bombero, background="#333", text="Ingrese un DNI válido", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=145, y=360)
                    mensajeError.after(1500, mensajeError.destroy)
                elif validacionId == False:
                    mensajeError = tk.Label(bombero, background="#333", text="El número de legajo no puede tener letras", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=110, y=350)
                    mensajeError.after(1500, mensajeError.destroy)
                elif validacionNombre == False:
                    mensajeError = tk.Label(bombero, background="#333", text="El nombre no puede contener números", foreground="#f00", font=("Arial", 15))
                    mensajeError.place(x=110, y=350)
                    mensajeError.after(1500, mensajeError.destroy)
                else:
                    cursor = conector.cursor()
                    cursor.execute("UPDATE personal SET nro_legajo=%s, apellido_nombre=%s, dni=%s, user=%s, pass=%s WHERE personal.nro_legajo = %s", (nroLegajo.get(), nombreB.get(), dniB.get(), usuario.get(), contraseña.get(), bomberoSeleccionado))
                    conector.commit()
                    cursor.close()
        
                    mensajeExito = tk.Label(bombero, background="#333", text="El bombero se modificó con éxito", foreground="#0f0", font=("Arial", 15))
                    mensajeExito.place(x=120, y=350)
                    mensajeExito.after(1500, mensajeExito.destroy)
                    
                    nroLegajo.delete(0, tk.END)
                    nombreB.delete(0, tk.END)
                    dniB.delete(0, tk.END)
                    usuario.delete(0, tk.END)
                    contraseña.delete(0, tk.END)
                
            tk.Button(bombero, text="Modificar", background="#FFA82B", width=10, command=actualizarDatos).place(x=220, y=390)
        
        tk.Button(bombero, text="Seleccionar", background="#FFA82B", command=elegirBombero).place(x=380, y=137)   
    def eliminarBombero():
        bombero = tk.Toplevel()
        bombero.title("Eliminar Bombero")
        bombero.geometry("500x500")
        bombero.config(bg="#333")

        cursor = conector.cursor()
        cursor.execute("SELECT * FROM personal")
        personalData = cursor.fetchall()
        cursor.close()

        mapaPersonal = {f"{apellido_nombre}": nro_legajo for nro_legajo, apellido_nombre, dni, user, password in personalData}

        tk.Label(bombero, text="Seleccione el evento a eliminar",
                fg="#fff", bg="#333", font=('arial', 15)).pack(pady=20)

        comboBomberos = ttk.Combobox(bombero, state="readonly", values=list(mapaPersonal.keys()), width=40)
        comboBomberos.pack(pady=10)

        infoBombero = tk.Label(bombero, text="", fg="#fff", bg="#333", font=("Arial", 12))
        infoBombero.pack(pady=10)

        def borrarBombero():
            seleccion = comboBomberos.get()
            if not seleccion:
                return

            bomberoSeleccionado = mapaPersonal[seleccion]

            confirmar = tk.messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Seguro que desea eliminar a:\n\n'{seleccion}'?"
            )
            if not confirmar:
                return

            try:
                cursor = conector.cursor()
                cursor.execute("DELETE FROM personal WHERE nro_legajo=%s", (bomberoSeleccionado,))
                conector.commit()
                cursor.close()

                tk.messagebox.showinfo("Éxito", f"'{seleccion}' ha sido eliminado correctamente.")

                # Refrescar combobox
                comboBomberos.set("")
                comboBomberos["values"] = [ev for ev in mapaPersonal.keys() if ev != seleccion]
                infoBombero.config(text="")
                mapaPersonal.pop(seleccion)

            except Exception as e:
                tk.messagebox.showerror("Error", f"No se pudo eliminar a .\n\n{e}")

        tk.Button(bombero, text="Eliminar", background="#FFA82B", width=20, height=2,command=borrarBombero).pack(pady=20)

        tk.Button(bombero, text="Cerrar", background="#FFA82B", width=20, height=2, command=bombero.destroy).pack(pady=10)

    tk.Button(personal, text="Añadir Bombero", background="#FFA82B", width=20, height=2, command=formulario_evento).place(x=290, y=350)
    tk.Button(personal, text="Modificar Bombero", background="#FFA82B", width=20, height=2, command=modificarPersonal).place(x=700, y=350)
    tk.Button(personal, text="Eliminar Bombero", background="#FFA82B", width=20, height=2, command=eliminarBombero).place(x=1090, y=350)
    tk.Button(personal, text="Menú principal", background="#FFA82B", width=20, height=2, command=personal.destroy).place(x=700, y=550)
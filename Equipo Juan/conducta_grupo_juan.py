import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

conector = mysql.connector.connect(
    host = "localhost",
    user = "root",
    database = "bomberos"
)

def menuConducta():
    conducta = tk.Toplevel()
    conducta.title("ABM Conducta")
    conducta.config(bg="#333")
    conducta.attributes("-fullscreen", True)
    
    tk.Label(conducta, text="ABM Conducta", foreground="#fff", background="#333", font=('arial', 20)).place(x=680, y=200)
    tk.Label(conducta, text="Agregar conducta", foreground="#fff", background="#333", font=('arial', 15)).place(x=280, y=300)
    tk.Label(conducta, text="Modificar conducta", foreground="#fff", background="#333", font=('arial', 15)).place(x=680, y=300)
    tk.Label(conducta, text="Eliminar conducta", foreground="#fff", background="#333", font=('arial', 15)).place(x=1080, y=300)
    
    def agregarConducta():
        bombero = tk.Toplevel()
        bombero.title("Agregar Conducta")
        bombero.geometry("500x500")
        bombero.config(background="#333")  
        
        tk.Label(bombero, text="Complete los datos de la conducta:", foreground="#fff", background="#333", font=('arial', 15)).place(x=100, y=100)
        
        ttk.Label(bombero, text="Número legajo:", background="#333", foreground="#fff").place(x=75, y=190)
        nroLegajo = tk.Entry(bombero, width=27)
        nroLegajo.place(x=180, y=190)
                
        tk.Label(bombero, text="Puntos:", background="#333", foreground="#fff").place(x=115, y=220)
        puntos = tk.Entry(bombero, width=27)
        puntos.place(x=180, y=220)
        
        tk.Label(bombero, text="Mes:", background="#333", foreground="#fff").place(x=130, y=250)
        mes = tk.Entry(bombero, width=27)
        mes.place(x=180, y=250)
        
        tk.Label(bombero, text="Año:", background="#333", foreground="#fff").place(x=130, y=280)
        anio = tk.Entry(bombero, width=27)
        anio.place(x=180, y=280)
        
        def subirConducta():
            validacionMes = True
            validacionAnio = True
            lengthMes = len(mes.get())
            puntaje = int(puntos.get())
            
            try:
                int(mes.get())
            except:
                validacionMes = False
            
            try:
                int(anio.get())
            except:
                validacionAnio = False
            
            mesElegido = int(mes.get())
            anioElegido = int(anio.get())
            cursor = conector.cursor()
            cursor.execute("SELECT YEAR(CURRENT_DATE)")
            data2 = cursor.fetchone()
            cursor.close()
            
            bomberoSeleccionado = nroLegajo.get()
            
            cursor = conector.cursor()
            cursor.execute("SELECT nro_legajo FROM personal WHERE nro_legajo = %s", (bomberoSeleccionado,))
            data = cursor.fetchone()
            cursor.close()
            
            if not nroLegajo.get() or not puntos.get() or not mes.get() or not anio.get():
                mensajeError = tk.Label(bombero, background="#333", text="Complete todos los datos", foreground="#f00", font=("Arial", 15))
                mensajeError.place(x=130, y=325)
                mensajeError.after(1500, mensajeError.destroy)
            elif data == None:
                mensajeError = tk.Label(bombero, background="#333", text="Ese número de legajo no existe", foreground="#f00", font=("Arial", 15))
                mensajeError.place(x=110, y=325)
                mensajeError.after(1500, mensajeError.destroy)
            elif puntaje < 0 or puntaje > 1:
                mensajeError = tk.Label(bombero, background="#333", text="Ingrese un puntaje válido", foreground="#f00", font=("Arial", 15))
                mensajeError.place(x=125, y=325)
                mensajeError.after(1500, mensajeError.destroy)
            elif validacionMes == False or lengthMes > 2 or (mesElegido > 12 or mesElegido < 1):
                mensajeError = tk.Label(bombero, background="#333", text="Ingrese un mes válido", foreground="#f00", font=("Arial", 15))
                mensajeError.place(x=145, y=325)
                mensajeError.after(1500, mensajeError.destroy)
            elif validacionAnio == False or data2[0] != anioElegido:
                mensajeError = tk.Label(bombero, background="#333", text="Ingrese el año actual", foreground="#f00", font=("Arial", 15))
                mensajeError.place(x=145, y=325)
                mensajeError.after(1500, mensajeError.destroy)
            else:
                cursor = conector.cursor()
                cursor.execute("INSERT INTO `conducta_personal`(`nro_legajo`, `puntos`, `mes`, `anio`) VALUES (%s, %s, %s, %s)", (nroLegajo.get(), puntos.get(), mes.get(), anio.get())) # Arreglar el insert
                conector.commit()
                cursor.close()
        
                mensajeExito = tk.Label(bombero, background="#333", text="La conducta se agregó con éxito", foreground="#0f0", font=("Arial", 15))
                mensajeExito.place(x=120, y=350)
                mensajeExito.after(1500, mensajeExito.destroy)
                
                nroLegajo.delete(0, tk.END)
                puntos.delete(0, tk.END)
                mes.delete(0, tk.END)
                anio.delete(0, tk.END)
        tk.Button(bombero, text="Guardar", background="#FFA82B", width=10, font=('arial', 10), command=subirConducta).place(x=200 ,y=400)
    def modificarConducta():
        ventana = tk.Toplevel()
        ventana.title("Modificar Conducta")
        ventana.geometry("600x500")
        ventana.config(bg="#333")

        cursor = conector.cursor()
        cursor.execute("SELECT id_conducta, nro_legajo FROM conducta_personal")
        data = cursor.fetchall()
        cursor.close()

        mapa = {f"{idc} - Legajo {legajo}": idc for idc, legajo in data}

        combo = ttk.Combobox(ventana, state="readonly", values=list(mapa.keys()), width=40)
        combo.place(x=150, y=60)

        entries = {}
        campos = ["ID Conducta", "Nro Legajo", "Puntos", "Mes", "Año"]
        for i, c in enumerate(campos):
            tk.Label(ventana, text=c, fg="#fff", bg="#333").place(x=100, y=120 + i*40)
            e = tk.Entry(ventana, width=27)
            e.place(x=250, y=120 + i*40)
            entries[c] = e

        def seleccionar():
            sel = combo.get()
            if not sel:
                return
            idSel = mapa[sel]
            cursor = conector.cursor()
            cursor.execute("SELECT * FROM conducta_personal WHERE id_conducta=%s", (idSel,))
            datos = cursor.fetchone()
            cursor.close()
            if not datos:
                return
            for k, v in zip(campos, datos):
                entries[k].delete(0, tk.END)
                entries[k].insert(0, v)

            def actualizar():
                nuevos = [entries[c].get().strip() for c in campos]

                if not nuevos[1].isdigit():
                    msg = tk.Label(ventana, text="El Nro Legajo debe ser un número.",bg="#333", fg="red", font=("Arial", 12))
                    msg.place(x=150, y=360)
                    msg.after(1500, msg.destroy)
                    return
                if nuevos[2] not in ["1", "0"]:
                    msg = tk.Label(ventana, text="El puntaje debe ser 1, 0 o -1.",bg="#333", fg="red", font=("Arial", 12))
                    msg.place(x=150, y=360)
                    msg.after(1500, msg.destroy)
                    return

                cursor = conector.cursor()
                cursor.execute("UPDATE conducta_personal SET id_conducta=%s, nro_legajo=%s, puntos=%s, mes=%s, anio=%s WHERE id_conducta=%s", (*nuevos, idSel))
                conector.commit()
                cursor.close()

                mensajeExito = tk.Label(ventana, background="#333", text="La conducta se modificó con éxito", foreground="#0f0", font=("Arial", 15))
                mensajeExito.place(x=120, y=370)
                mensajeExito.after(1500, mensajeExito.destroy)

            tk.Button(ventana, text="Modificar", bg="#FFA82B", command=actualizar).place(x=250, y=400)

        tk.Button(ventana, text="Seleccionar", bg="#FFA82B", command=seleccionar).place(x=400, y=58)
    def eliminarConducta():
        ventana = tk.Toplevel()
        ventana.title("Eliminar Conducta")
        ventana.geometry("500x400")
        ventana.config(bg="#333")

        cursor = conector.cursor()
        cursor.execute("SELECT id_conducta, nro_legajo FROM conducta_personal")
        data = cursor.fetchall()
        cursor.close()

        mapa = {f"{idc} - Legajo {legajo}": idc for idc, legajo in data}
        combo = ttk.Combobox(ventana, state="readonly", values=list(mapa.keys()), width=40)
        combo.pack(pady=20)

        def borrar():
            sel = combo.get()
            if not sel:
                return
            idSel = mapa[sel]
            cursor = conector.cursor()
            cursor.execute("DELETE FROM conducta_personal WHERE id_conducta=%s", (idSel,))
            conector.commit()
            cursor.close()
            mensajeExito = tk.Label(ventana, background="#333", text="La conducta se eliminó con éxito", foreground="#0f0", font=("Arial", 15))
            mensajeExito.place(x=120, y=150)
            mensajeExito.after(1500, mensajeExito.destroy)
                
        tk.Button(ventana, text="Eliminar", bg="#FFA82B", command=borrar).pack(pady=20)
    tk.Button(conducta, text="Añadir Conducta", background="#FFA82B", width=20, height=2, command=agregarConducta).place(x=290, y=350)
    tk.Button(conducta, text="Modificar Conducta", background="#FFA82B", width=20, height=2, command=modificarConducta).place(x=700, y=350)
    tk.Button(conducta, text="Eliminar Conducta", background="#FFA82B", width=20, height=2, command=eliminarConducta).place(x=1090, y=350)
    tk.Button(conducta, text="Volver", background="#FFA82B", width=20, height=2, command=conducta.destroy).place(x=700, y=550)
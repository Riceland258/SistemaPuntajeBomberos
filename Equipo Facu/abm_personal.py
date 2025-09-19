import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

class BaseDeDatos:
    def __init__(self):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql"
        )
        self.cursor = self.connexion.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS bomberos")
        self.connexion.commit()
        self.cursor.close()
        self.connexion.close()

        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="bomberos"
        )
        self.cursor = self.connexion.cursor()
    
    def crear_tablas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS personal(
                nro_legajo INT PRIMARY KEY,
                apellido_nombre VARCHAR(100),
                dni INT,
                user VARCHAR(50),
                password VARCHAR(50),
                estado VARCHAR(20) DEFAULT 'activo'
            )
        """)
        self.connexion.commit()

    def alta_bombero(self, nro_legajo, apellido_nombre, dni, user, password, estado='activo'):
        self.cursor.execute("""
            INSERT INTO personal (nro_legajo, apellido_nombre, dni, user, password, estado)
            VALUES(%s,%s,%s,%s,%s,%s)
        """, (nro_legajo, apellido_nombre, dni, user, password, estado))
        self.connexion.commit()

    def borrar_bombero(self, nro_legajo):
        self.cursor.execute("""
            UPDATE personal SET estado = 'baja' WHERE nro_legajo = %s
        """, (nro_legajo,))
        self.connexion.commit()

    def modificar_bombero(self, nro_legajo_nuevo, apellido_nombre, dni, user, password, estado, nro_legajo_original):
        self.cursor.execute("""
            UPDATE personal 
            SET nro_legajo = %s,
                apellido_nombre = %s,
                dni = %s,
                user = %s,
                password = %s,
                estado = %s
            WHERE nro_legajo = %s
        """, (nro_legajo_nuevo, apellido_nombre, dni, user, password, estado, nro_legajo_original))
        self.connexion.commit()

    def interfaz(self):
        ventana_abm_persona = tk.Tk()
        ventana_abm_persona.attributes("-fullscreen", True)

        legajo_original = [None]

        label_legajo = tk.Label(ventana_abm_persona, text="legajo", font=("Arial", 10))
        label_legajo.place(relx=0.02, rely=0.05)
        entry_legajo = ttk.Entry(ventana_abm_persona)
        entry_legajo.place(relx=0.05, rely=0.05)

        label_apellido_y_nombre = tk.Label(ventana_abm_persona, text="apellido y nombre", font=("Arial",10))
        label_apellido_y_nombre.place(relx=0.15, rely=0.05)
        entry_apellido_y_nombre = ttk.Entry(ventana_abm_persona, width=30)
        entry_apellido_y_nombre.place(relx=0.23, rely=0.05)

        label_dni = tk.Label(ventana_abm_persona, text="dni", font=("Arial", 10))
        label_dni.place(relx=0.36, rely=0.05)
        entry_dni = ttk.Entry(ventana_abm_persona)
        entry_dni.place(relx=0.38, rely=0.05)

        label_user = tk.Label(ventana_abm_persona, text="usuario",font=("Arial", 10))
        label_user.place(relx=0.47, rely=0.05)
        entry_user = ttk.Entry(ventana_abm_persona)
        entry_user.place(relx=0.51, rely=0.05)

        label_password = tk.Label(ventana_abm_persona, text="contraseña", font=("Arial", 10))
        label_password.place(relx=0.60, rely=0.05)
        entry_password = ttk.Entry(ventana_abm_persona)
        entry_password.place(relx=0.65, rely=0.05)

        tree = ttk.Treeview(ventana_abm_persona, columns=("legajo","apellido_nombre","dni","usuario"), show="headings")
        tree.heading("legajo", text="legajo")
        tree.heading("apellido_nombre", text="apellido y nombre")
        tree.heading("dni", text="dni")
        tree.heading("usuario", text="usuario")
        tree.column("legajo", width=80)
        tree.column("apellido_nombre", width=200)
        tree.column("dni", width=100)
        tree.column("usuario", width=100)
        tree.place(x=50, y=200, width=1450, height=400)

        def seleccionar_fila(event):
            item = tree.selection()
            if item:
                valores = tree.item(item)["values"]
                legajo_original[0] = valores[0]
                entry_legajo.delete(0, tk.END)
                entry_legajo.insert(0, valores[0])
                entry_apellido_y_nombre.delete(0, tk.END)
                entry_apellido_y_nombre.insert(0, valores[1])
                entry_dni.delete(0, tk.END)
                entry_dni.insert(0, valores[2])
                entry_user.delete(0, tk.END)
                entry_user.insert(0, valores[3])

                bd.cursor.execute("SELECT password FROM personal WHERE nro_legajo = %s", (valores[0],))
                resultado = bd.cursor.fetchone()
                if resultado and resultado[0] is not None:
                    entry_password.delete(0, tk.END)
                    entry_password.insert(0, resultado[0])
                else:
                    entry_password.delete(0, tk.END)

        tree.bind("<<TreeviewSelect>>", seleccionar_fila)

        def limpiar_campos():
            entry_legajo.config(state='normal')
            entry_legajo.delete(0, tk.END)
            entry_apellido_y_nombre.delete(0, tk.END)
            entry_dni.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_password.delete(0, tk.END)
            legajo_original[0] = None

        def guardar_bombero():
            try:
                legajo_texto = entry_legajo.get().strip()

                if not legajo_texto.isdigit():
                    messagebox.showerror("Error", "El legajo solo puede contener números.")
                    return

                nro_legajo = int(legajo_texto)
                apellido_nombre = entry_apellido_y_nombre.get().strip()
                dni_texto = entry_dni.get().strip()
                user = entry_user.get().strip()
                password = entry_password.get().strip()

                # ✅ Validaciones adicionales
                if len(apellido_nombre) < 2:
                    messagebox.showerror("Error", "El nombre y apellido debe tener al menos 2 caracteres.")
                    return

                if len(user) < 2:
                    messagebox.showerror("Error", "El usuario debe tener al menos 2 caracteres.")
                    return

                if len(password) < 2:
                    messagebox.showerror("Error", "La contraseña debe tener al menos 2 caracteres.")
                    return

                if not dni_texto.isdigit() or not (7 <= len(dni_texto) <= 8):
                    messagebox.showerror("Error", "El DNI debe tener entre 7 y 8 dígitos numéricos.")
                    return

                dni = int(dni_texto)

                bd.cursor.execute("SELECT estado FROM personal WHERE nro_legajo = %s", (nro_legajo,))
                resultado = bd.cursor.fetchone()

                if resultado:
                    estado_actual = resultado[0]

                    if estado_actual == 'activo':
                        respuesta = messagebox.askyesno("Modificar", "Este legajo ya está activo. ¿Desea modificar el bombero?")
                        if respuesta:
                            bd.modificar_bombero(nro_legajo, apellido_nombre, dni, user, password, 'activo', nro_legajo)
                            messagebox.showinfo("Modificado", f"Bombero con legajo {nro_legajo} modificado correctamente.")
                    elif estado_actual == 'baja':
                        reincorporar = messagebox.askyesno("Reincorporar", "Este bombero está dado de baja. ¿Desea volver a incorporarlo?")
                        if reincorporar:
                            bd.modificar_bombero(nro_legajo, apellido_nombre, dni, user, password, 'activo', nro_legajo)
                            messagebox.showinfo("Reincorporado", f"Bombero con legajo {nro_legajo} reincorporado correctamente.")
                else:
                    bd.alta_bombero(nro_legajo, apellido_nombre, dni, user, password)
                    messagebox.showinfo("Guardado", f"El bombero {apellido_nombre} guardado correctamente.")

                actualizar_tree()
                limpiar_campos()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el bombero: {e}")


        def dar_baja_bombero():
            try:
                legajo_texto = entry_legajo.get()
                if not legajo_texto.strip():
                    raise ValueError("El campo legajo está vacío.")
                nro_legajo = int(legajo_texto)
                bd.borrar_bombero(nro_legajo)
                messagebox.showinfo("Éxito", f"El bombero con legajo {nro_legajo} fue dado de baja.")
                actualizar_tree()
                limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo dar de baja: {e}")

        def actualizar_tree():
            for row in tree.get_children():
                tree.delete(row)
            bd.cursor.execute("SELECT nro_legajo, apellido_nombre, dni, user FROM personal WHERE estado = 'activo'")
            datos = bd.cursor.fetchall()
            for fila in datos:
                tree.insert("", "end", values=fila)

        btn_guardar = ttk.Button(ventana_abm_persona, text="guardar", command=guardar_bombero)
        btn_guardar.place(relx=0.75, rely=0.05)

        btn_borrar = ttk.Button(ventana_abm_persona, text="borrar", command=dar_baja_bombero)
        btn_borrar.place(relx=0.81, rely=0.05)

        btn_salir = ttk.Button(ventana_abm_persona, text="salir", command=ventana_abm_persona.destroy)
        btn_salir.place(relx=0.87, rely=0.05)

        actualizar_tree()
        ventana_abm_persona.mainloop()

    def cerrar_conexion(self):
        self.cursor.close()
        self.connexion.close()


if __name__ == "__main__":
    bd = BaseDeDatos()
    bd.crear_tablas()
    bd.interfaz()
    bd.cerrar_conexion()

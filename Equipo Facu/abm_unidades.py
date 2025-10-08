import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

class BaseDeDatos:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host = "localhost",
            user="root",
            password="mysql",
            database="bomberos"
        )
        self.cursor = self.conexion.cursor()
    
    def crear_tabla_unidad(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS unidades(
                            id_unidad INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(50) NOT NULL,
                            operativa TINYINT(1) NOT NULL DEFAULT 0)
                            """)
        self.conexion.commit()
    
    def interfaz(self):
        ventana_abm = tk.Tk()
        ventana_abm.attributes("-fullscreen", True)
        ventana_abm.title("ABM unidades")

        unidad_label = tk.Label(ventana_abm, text="Unidad", font=("Arial", 11))
        unidad_label.place(relx=0.06,rely=0.05)
        unidad_entry = ttk.Entry(ventana_abm)
        unidad_entry.place(relx=0.1, rely=0.05)

        operativa_label = tk.Label(ventana_abm, text="Operativa", font=("Arial",11))
        operativa_label.place(relx=0.2, rely=0.05)
        operativa_entry = ttk.Combobox(ventana_abm, width=10, values=("0", "1"), state="readonly")
        operativa_entry.place(relx=0.25, rely=0.05)
        # seleccionar valor por defecto
        operativa_entry.current(0)

        btn_guardar = ttk.Button(ventana_abm, text="Guardar")
        btn_guardar.place(relx=0.35, rely=0.05)

        btn_borrar = ttk.Button(ventana_abm, text="Borrar")
        btn_borrar.place(relx=0.41, rely=0.05)

        btn_salir = ttk.Button(ventana_abm, text="Salir",   command=ventana_abm.destroy)
        btn_salir.place(relx=0.87, rely=0.05)


        tree = ttk.Treeview(ventana_abm, columns=("id_unidad", "nombre", "operativa"), show="headings", displaycolumns=("nombre", "operativa"))

        tree.heading("nombre", text="Unidad")
        tree.heading("operativa", text="Operativa")
        tree.column("id_unidad", width=0, minwidth=0, stretch=False)
        tree.column("nombre", width=400, anchor="w", minwidth=100)
        tree.column("operativa", width=100, anchor="center", minwidth=50)
        tree.place(x=255, y=250, width=1000, height=300)

        def cargar_unidades():
            for i in tree.get_children():
                tree.delete(i)
            try:
                self.cursor.execute("SELECT id_unidad, nombre, operativa FROM unidades")
                for fila in self.cursor.fetchall():
                    tree.insert("", "end", values=(fila[0], fila[1], fila[2]))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar unidades: {e}")

        selected_id = None

        def guardar_unidad():
            nonlocal selected_id
            nombre = unidad_entry.get().strip()
            operativa = operativa_entry.get()
            if not nombre:
                messagebox.showwarning("Validación", "El campo Unidad no puede estar vacío")
                return
            try:
                if selected_id is None:
                    self.cursor.execute("INSERT INTO unidades (nombre, operativa) VALUES (%s, %s)", (nombre, int(operativa)))
                else:
                    self.cursor.execute("UPDATE unidades SET nombre=%s, operativa=%s WHERE id_unidad=%s", (nombre, int(operativa), selected_id))
                self.conexion.commit()
                unidad_entry.delete(0, tk.END)
                operativa_entry.current(0)
                selected_id = None
                btn_guardar.config(text="Guardar")
                cargar_unidades()
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")

        def borrar_unidad():
            nonlocal selected_id
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Borrar", "Seleccione una unidad para borrar")
                return
            item = tree.item(sel[0])
            id_unidad = item.get("values")[0]
            try:
                self.cursor.execute("DELETE FROM unidades WHERE id_unidad = %s", (id_unidad,))
                self.conexion.commit()
                if selected_id == id_unidad:
                    selected_id = None
                    unidad_entry.delete(0, tk.END)
                    operativa_entry.current(0)
                    btn_guardar.config(text="Guardar")
                cargar_unidades()
            except Exception as e:
                messagebox.showerror("Error", f"Error al borrar: {e}")

        def on_tree_select(event):
            nonlocal selected_id
            sel = tree.selection()
            if not sel:
                return
            item = tree.item(sel[0])
            vals = item.get("values")
            if not vals:
                return
            selected_id = vals[0]
            unidad_entry.delete(0, tk.END)
            unidad_entry.insert(0, vals[1])
            operativa_entry.set(str(vals[2]))
            btn_guardar.config(text="Actualizar")

        tree.bind("<<TreeviewSelect>>", on_tree_select)

        btn_guardar.config(command=guardar_unidad)
        btn_borrar.config(command=borrar_unidad)

        cargar_unidades()

        ventana_abm.mainloop()

if __name__ == "__main__":
    bd = BaseDeDatos()
    bd.crear_tabla_unidad()
    bd.interfaz()
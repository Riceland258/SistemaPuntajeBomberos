import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import re

class BaseDeDatos:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost", user="root", password="mysql", database="bomberos"
        )
        self.cursor = self.conexion.cursor()

    def crear_tablas_eventos(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos(
                id_evento INT AUTO_INCREMENT PRIMARY KEY,
                evento     VARCHAR(255),
                puntos     DECIMAL(10, 2)
            )
        """)
        self.conexion.commit()

    def alta_eventos(self, evento, puntos):
        self.cursor.execute(
            "INSERT INTO eventos(evento, puntos) VALUES(%s, %s)",
            (evento, puntos)
        )
        self.conexion.commit()

    def baja_eventos(self, id_evento):
        self.cursor.execute(
            "DELETE FROM eventos WHERE id_evento = %s",
            (id_evento,)
        )
        self.conexion.commit()

    def modificar_eventos(self, id_evento, evento, puntos):
        self.cursor.execute(
            "UPDATE eventos SET evento = %s, puntos = %s WHERE id_evento = %s",
            (evento, puntos, id_evento)
        )
        self.conexion.commit()

    def interfaz_eventos(self):
        ventana = tk.Tk()
        ventana.attributes("-fullscreen", True)

        # Labels y Entry
        tk.Label(ventana, text="Evento", font=("Arial", 10)).place(relx=0.02, rely=0.05)
        entry_nombre = ttk.Entry(ventana, width=30)
        entry_nombre.place(relx=0.05, rely=0.05)

        tk.Label(ventana, text="Puntos", font=("Arial", 10)).place(relx=0.18, rely=0.05)
        entry_puntos = ttk.Entry(ventana, width=10)
        entry_puntos.place(relx=0.21, rely=0.05)

        # Treeview
        tree = ttk.Treeview(ventana, columns=("evento", "puntos"), show="headings")
        tree.heading("evento", text="Evento")
        tree.heading("puntos", text="Puntos")
        tree.place(x=50, y=200, width=1450, height=400)

        # Estado de edición
        selected_id = {"value": None}

        def cargar_eventos():
            for fila in tree.get_children():
                tree.delete(fila)
            self.cursor.execute("SELECT id_evento, evento, puntos FROM eventos")
            for id_evt, ev, pts in self.cursor.fetchall():
                tree.insert(
                    "", tk.END,
                    iid=str(id_evt),
                    values=(ev, f"{pts:.2f}")
                )

        def on_tree_select(event):
            sel = tree.selection()
            if not sel:
                return
            id_evt = sel[0]
            ev, pts_str = tree.item(id_evt)["values"]
            selected_id["value"] = id_evt

            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, ev)
            entry_puntos.delete(0, tk.END)
            entry_puntos.insert(0, pts_str)

            btn_guardar.config(text="Modificar")

        tree.bind("<<TreeviewSelect>>", on_tree_select)

        def validar(evt, pts):
            if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,}", evt):
                messagebox.showwarning("Datos inválidos",
                    "El nombre debe tener al menos 2 letras y solo letras o espacios.")
                return False
            if not re.fullmatch(r"\d+(\.\d+)?", pts):
                messagebox.showwarning("Datos inválidos",
                    "Puntos debe ser un número válido.")
                return False
            return True

        def guardar_o_modificar():
            evt = entry_nombre.get().strip()
            pts = entry_puntos.get().strip()
            if not validar(evt, pts):
                return
            pts_val = float(pts)

            if selected_id["value"] is None:
                # INSERT
                self.alta_eventos(evt, pts_val)
                messagebox.showinfo("Éxito", "Evento agregado.")
            else:
                id_evt = selected_id["value"]
                self.modificar_eventos(id_evt, evt, pts_val)
                messagebox.showinfo("Éxito", f"Evento {id_evt} modificado.")
                selected_id["value"] = None
                btn_guardar.config(text="Guardar")

            # limpiar entries tras guardar/modificar
            entry_nombre.delete(0, tk.END)
            entry_puntos.delete(0, tk.END)

            cargar_eventos()

        def borrar_evento():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Atención", "Primero seleccioná un evento.")
                return
            id_evt = sel[0]
            ev, _ = tree.item(id_evt)["values"]

            if not messagebox.askyesno("Confirmar borrado", f"¿Borrar «{ev}»?"):
                return

            self.baja_eventos(id_evt)
            messagebox.showinfo("Éxito", f"Evento «{ev}» eliminado.")

            # limpiar entries tras borrar
            entry_nombre.delete(0, tk.END)
            entry_puntos.delete(0, tk.END)
            selected_id["value"] = None
            btn_guardar.config(text="Guardar")

            cargar_eventos()

        btn_guardar = ttk.Button(ventana, text="Guardar", command=guardar_o_modificar)
        btn_guardar.place(relx=0.32, rely=0.05)

        ttk.Button(ventana, text="Borrar",  command=borrar_evento).place(relx=0.38, rely=0.05)
        ttk.Button(ventana, text="Salir",   command=ventana.destroy).place(relx=0.87, rely=0.05)

        cargar_eventos()
        ventana.mainloop()

if __name__ == "__main__":
    bd = BaseDeDatos()
    bd.crear_tablas_eventos()
    bd.interfaz_eventos()

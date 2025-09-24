# ====================== IMPORTACIONES ======================
import tkinter as tk
from tkinter import ttk, messagebox
from Axel_Base_de_Datos import Conectar
from Axel_Operaciones_Personal import (abrir_editor_bombero, volver_ventana_principal)
from Axel_Utilidades import centrar_ventana

# ====================== VENTANA ======================

class VentanaListadoCuerpoBomberos(tk.Toplevel):
    # LIMITADOR DE FILAS QUE SE MUESTRAN POR CARGA
    FILAS_POR_BLOQUE = 50

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Cuerpo de Bomberos")
        self.withdraw()
        self.offset = 0
        self.filtro_actual = ""
        self.crear_tabla()

    def crear_tabla(self):
        # FONDO PRINCIPAL
        self.configure(bg="#2b2b2b")

        # FRAME PRINCIPAL
        marco = tk.Frame(self, bg="#2b2b2b")
        marco.pack(fill="both", expand=True, padx=20, pady=20)

        # FRAME SUPERIOR
        frame_superior = tk.Frame(marco, bg="#2b2b2b")
        frame_superior.pack(fill="x", pady=(0, 10))

        tk.Label(frame_superior, text="CUERPO DE BOMBEROS", 
                font=("Arial", 24, "bold"), fg="#ff4d4d", bg="#2b2b2b"
            ).pack(side="left")

        # BUSCADOR
        frame_busqueda = tk.Frame(frame_superior, bg="#2b2b2b")
        frame_busqueda.pack(side="right")
        self.entry_buscar = tk.Entry(frame_busqueda, font=("Arial", 14, "bold"), bg="#ffd966", fg="#000000")
        self.entry_buscar.pack(side="left", ipady=8, ipadx=6)

        tk.Button(frame_busqueda, text="🔍",
                font=("Arial", 16, "bold"), bg="#ff4d4d", fg="white",
                command=lambda: self.buscar()
            ).pack(side="left", padx=(5,0))

        self.entry_buscar.bind("<Return>", lambda e: self.buscar())
        self.entry_buscar.bind("<FocusOut>", lambda e: self.buscar_si_vacio())

        # FRAME CENTRAL
        frame_tabla = tk.Frame(marco, bg="#2b2b2b")
        frame_tabla.pack(fill="both", expand=True)

        # TABLA
        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        columnas = ("Legajo", "Apellido y Nombre", "DNI", "Rango")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        for col in columnas:
            self.tree.heading(col, text=col)
        self.tree.column("Legajo", width=140, anchor="center")
        self.tree.column("Apellido y Nombre", width=250, anchor="w")
        self.tree.column("DNI", width=140, anchor="center")
        self.tree.column("Rango", width=140, anchor="center")

        # ESTILO DE LA TABLA
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#ff4d4d", foreground="white")
        style.configure("Treeview", font=("Arial", 12, "bold"), rowheight=32, background="#333333", foreground="white", fieldbackground="#333333")
        style.map("Treeview", background=[("selected", "#ffd966")], foreground=[("selected", "#000000")])
        self.tree.tag_configure("oddrow", background="#4d4d4d", foreground="white")
        self.tree.tag_configure("evenrow", background="#666666", foreground="white")
        self.tree.bind("<Double-1>", lambda e: self.on_double_click(e))

        # FRAME INFERIOR
        frame_botones = tk.Frame(marco, bg="#2b2b2b")
        frame_botones.pack(fill="x", pady=(10,0))

        # BOTÓN EDITAR
        frame_editar = tk.Frame(frame_botones, bg="#2b2b2b")
        frame_editar.pack(side="left", expand=True)
        self.btn_editar = tk.Button(frame_editar, text="Editar",
                                font=("Arial", 14, "bold"), width=20, bg="#ff4d4d", fg="white", activebackground="#ffd966",
                                command=lambda: self.editar_fila()
                            )
        self.btn_editar.pack(pady=5)

        # BOTÓN VOLVER
        frame_volver = tk.Frame(frame_botones, bg="#2b2b2b")
        frame_volver.pack(side="right", expand=True)
        self.btn_volver = tk.Button(frame_volver, text="Volver",
                                font=("Arial", 14, "bold"), width=20, bg="#ffd966", fg="#000000", activebackground="#ff4d4d",
                                command=lambda: volver_ventana_principal(self)
                            )
        self.btn_volver.pack(pady=5)

        # BOTON CARGAR MAS
        self.btn_mas = tk.Button(marco, text="Cargar más",
                                font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white",
                                command=lambda: self.cargar_mas()
                            )
        self.btn_mas.pack(pady=5)
        self.cargar_mas()

    def buscar(self):
        self.filtro_actual = self.entry_buscar.get().strip()
        self.offset = 0
        self.tree.delete(*self.tree.get_children())
        self.cargar_mas()

    def buscar_si_vacio(self):
        if self.entry_buscar.get().strip() == "":
            self.filtro_actual = ""
            self.offset = 0
            self.tree.delete(*self.tree.get_children())
            self.cargar_mas()

    def cargar_mas(self):
        conexion = Conectar()
        cursor = conexion.cursor(dictionary=True)
        
        if self.filtro_actual:
            # Buscar SOLO por legajo o DNI
            filtro_texto = self.filtro_actual.strip()
            cursor.execute(
                "SELECT nro_legajo, apellido_nombre, dni, rango "
                "FROM personal "
                "WHERE (CAST(nro_legajo AS CHAR) LIKE %s "
                "OR CAST(dni AS CHAR) LIKE %s) "
                "ORDER BY rango DESC "
                "LIMIT %s OFFSET %s",
                (f"%{filtro_texto}%", f"%{filtro_texto}%",
                 int(self.FILAS_POR_BLOQUE), int(self.offset))
            )
        else:
            cursor.execute(
                "SELECT nro_legajo, apellido_nombre, dni, rango "
                "FROM personal "
                "ORDER BY rango DESC "
                "LIMIT %s OFFSET %s",
                (int(self.FILAS_POR_BLOQUE), int(self.offset))
            )
        
        bloque = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        for i, fila in enumerate(bloque):
            tag = "evenrow" if (self.offset + i) % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(fila["nro_legajo"], fila["apellido_nombre"], fila["dni"], fila["rango"]), tags=(tag,))

        self.offset += len(bloque)

        if len(bloque) < self.FILAS_POR_BLOQUE:
            self.btn_mas.pack_forget()
        else:
            self.btn_mas.pack(pady=5)

    def editar_fila(self):
        seleccion = self.tree.selection()
        if seleccion:
            # Obtener datos de la fila seleccionada
            item = self.tree.item(seleccion[0])
            valores = item['values']
            
            # Crear diccionario con los datos del bombero
            datos_bombero = {
                'nro_legajo': valores[0],
                'apellido_nombre': valores[1],
                'dni': valores[2],
                'rango': valores[3]
            }
            
            # Separar apellido y nombre
            if ', ' in datos_bombero['apellido_nombre']:
                apellido, nombre = datos_bombero['apellido_nombre'].split(', ', 1)
                datos_bombero['apellido'] = apellido
                datos_bombero['nombre'] = nombre
            else:
                datos_bombero['apellido'] = datos_bombero['apellido_nombre']
                datos_bombero['nombre'] = ''
            
            abrir_editor_bombero(self, datos_bombero)
        else:
            messagebox.showwarning("Atención", "Debe seleccionar una fila antes de editar")

    def on_double_click(self, event):
        self.editar_fila()

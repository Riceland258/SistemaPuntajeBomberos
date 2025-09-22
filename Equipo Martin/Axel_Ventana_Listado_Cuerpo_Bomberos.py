# ====================== IMPORTACIONES ======================
import tkinter as tk
from tkinter import ttk
from Axel_Operaciones_Personal import (abrir_editor_bombero, buscar, buscar_si_vacio, cargar_mas, editar_fila, on_double_click, volver_ventana_principal)

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
                command=lambda: buscar(self)
            ).pack(side="left", padx=(5,0))

        self.entry_buscar.bind("<Return>", lambda e: buscar(self))
        self.entry_buscar.bind("<FocusOut>", lambda e: buscar_si_vacio(self))

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
        self.tree.bind("<Double-1>", lambda e: on_double_click(self, e))

        # FRAME INFERIOR
        frame_botones = tk.Frame(marco, bg="#2b2b2b")
        frame_botones.pack(fill="x", pady=(10,0))

        # BOTÓN EDITAR
        frame_editar = tk.Frame(frame_botones, bg="#2b2b2b")
        frame_editar.pack(side="left", expand=True)
        self.btn_editar = tk.Button(frame_editar, text="Editar",
                                font=("Arial", 14, "bold"), width=20, bg="#ff4d4d", fg="white", activebackground="#ffd966",
                                command=lambda: editar_fila(self)
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
                                command=lambda: cargar_mas(self)
                            )
        self.btn_mas.pack(pady=5)
        cargar_mas(self)
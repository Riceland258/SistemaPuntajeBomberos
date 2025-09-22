# ====================== IMPORTACIONES ======================
import tkinter as tk
from tkinter import ttk
from Axel_Operaciones_Conducta import (
                                mostrar_ventana_listado_conducta, abrir_actualizar, recargar_tabla, buscar,
                                buscar_si_vacio, cargar_filas, editar_fila, volver_ventana_principal_conducta
                            )

# ====================== VENTANA ======================

class VentanaListadoConducta(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Registros de conducta")
        self.withdraw()
        self.MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.crear_tabla()

    def crear_tabla(self):
        # FONDO PRINCIPAL
        self.configure(bg="#2b2b2b")

        # FRAME PRINCIPAL
        marco = tk.Frame(self, bg="#2b2b2b")
        marco.pack(fill="both", expand=True, padx=20, pady=20)

        # FRAME SUPERIOR
        frame_superior = tk.Frame(marco, bg="#2b2b2b")
        frame_superior.pack(fill="x", pady=(0,10))

        tk.Label(frame_superior, text="REGISTROS CONDUCTA (Ultimos 100)",
                font=("Arial", 24, "bold"), fg="#ff4d4d", bg="#2b2b2b"
            ).pack(side="left")

        # BUSCADOR
        frame_busqueda = tk.Frame(frame_superior, bg="#2b2b2b")
        frame_busqueda.pack(side="right")
        self.entry_buscar = tk.Entry(frame_busqueda,
                                    font=("Arial", 14, "bold"), bg="#ffd966", fg="#000000"
                                )
        self.entry_buscar.pack(side="left", ipady=6, ipadx=6)
        tk.Button(frame_busqueda, text="🔍",
                font=("Arial", 16, "bold"), bg="#ff4d4d", fg="white",
                command=lambda: cargar_filas(self)
            ).pack(side="left", padx=(5,0))

        self.entry_buscar.bind("<Return>", lambda e: cargar_filas(self, filtro=self.entry_buscar.get().strip()))
        self.entry_buscar.bind("<FocusOut>", lambda e: buscar_si_vacio(self))

        # FRAME CENTRAL
        frame_tabla = tk.Frame(marco, bg="#2b2b2b")
        frame_tabla.pack(fill="both", expand=True)

        # TABLA
        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")

        columnas = ("Legajo", "Apellido y Nombre", "Puntaje", "Mes", "Año")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        for col in columnas:
            self.tree.heading(col, text=col, anchor="center")
            if col in ("Apellido y Nombre", "Mes"):
                self.tree.column(col, anchor="w", width=180)
            else:
                self.tree.column(col, anchor="center", width=150)

        # ESTILO DE LA TABLA
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading",
                        font=("Arial", 14, "bold"), background="#ff4d4d", foreground="white"
                        )
        style.configure("Treeview",
                        font=("Arial", 12, "bold"), rowheight=32, background="#333333", foreground="white", fieldbackground="#333333"
                    )
        style.map("Treeview", background=[("selected", "#ffd966")], foreground=[("selected", "#000000")])
        self.tree.tag_configure("oddrow", background="#4d4d4d", foreground="white")
        self.tree.tag_configure("evenrow", background="#666666", foreground="white")

        # FRAME INFERIOR
        frame_botones = tk.Frame(marco, bg="#2b2b2b")
        frame_botones.pack(fill="x", pady=10)

        # BOTÓN EDITAR
        self.btn_actualizar = tk.Button(frame_botones, text="Editar",
                                        font=("Arial", 14, "bold"), width=20, bg="#ff4d4d", fg="white", activebackground="#ffd966",
                                        command=lambda: editar_fila(self)
                                    )
        self.btn_actualizar.pack(side="left", padx=5, pady=5, expand=True)

        # BOTÓN VOLVER
        self.btn_volver = tk.Button(frame_botones, text="Volver",
                                    font=("Arial", 14, "bold"), width=20, bg="#ffd966", fg="#000000", activebackground="#ff4d4d",
                                    command=lambda: volver_ventana_principal_conducta(self)
                                )
        self.btn_volver.pack(side="right", padx=5, pady=5, expand=True)

        cargar_filas(self)
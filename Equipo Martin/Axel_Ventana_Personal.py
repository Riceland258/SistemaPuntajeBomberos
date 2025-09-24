# ====================== IMPORTACIONES ======================
import tkinter as tk
from Axel_Operaciones_Personal import registrar_personal_revision
from Axel_Operaciones_Personal import abrir_ventana_listado_cuerpo_bomberos

# ====================== VENTANA ======================

class VentanaPersonal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Personal")
        self.configure(bg="#2b2b2b")
        self.state("zoomed")
        self.crear_widgets()

    def crear_widgets(self):
        # MENUS
        opciones_rango_bombero = ["1", "2", "3"]
        self.var_rango = tk.StringVar(value=opciones_rango_bombero[0])

        # CONTENEDOR
        contenedor = tk.Frame(self, width=400, bg="#333333", bd=2, relief="ridge")
        contenedor.pack(expand=True, pady=20, padx=20)
        contenedor.pack_propagate(False)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)

        # TÍTULO
        tk.Label(
            contenedor, text="GESTIÓN DE PERSONAL",
            font=("Arial", 22, "bold"), fg="#ff4d4d", bg="#333333"
        ).grid(row=0, column=0, columnspan=2, pady=(10,20), padx=10)

        # LEGAJO
        tk.Label(
            contenedor, text="N° Legajo:",
            font=("Arial", 14, "bold"), bg="#333333", fg="white"
        ).grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.entrada_legajo = tk.Entry(
            contenedor,
            font=("Arial", 14, "bold"), bg="#4d4d4d", fg="white", insertbackground="white"
        )
        self.entrada_legajo.grid(row=2, column=0, pady=(0,10), padx=(10,5), sticky="we")

        # DNI
        tk.Label(
            contenedor, text="DNI:",
            font=("Arial", 14, "bold"), bg="#333333", fg="white"
        ).grid(row=1, column=1, pady=5, padx=10, sticky="w")
        self.entrada_dni = tk.Entry(
            contenedor,
            font=("Arial", 14, "bold"), bg="#4d4d4d", fg="white", insertbackground="white"
        )
        self.entrada_dni.grid(row=2, column=1, pady=(0,10), padx=(5,10), sticky="we")

        # APELLIDO
        tk.Label(
            contenedor, text="Apellido:",
            font=("Arial", 14, "bold"), bg="#333333", fg="white"
        ).grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.entrada_apellido = tk.Entry(
            contenedor,
            font=("Arial", 14, "bold"), bg="#4d4d4d", fg="white", insertbackground="white"
        )
        self.entrada_apellido.grid(row=4, column=0, pady=(0,10), padx=(10,5), sticky="we")

        # NOMBRE
        tk.Label(
            contenedor, text="Nombre:",
            font=("Arial", 14, "bold"), bg="#333333", fg="white"
        ).grid(row=3, column=1, pady=5, padx=10, sticky="w")
        self.entrada_nombre = tk.Entry(
            contenedor,
            font=("Arial", 14, "bold"), bg="#4d4d4d", fg="white", insertbackground="white"
        )
        self.entrada_nombre.grid(row=4, column=1, pady=(0,10), padx=(5,10), sticky="we")

        # RANGO
        tk.Label(
            contenedor, text="Rango:",
            font=("Arial", 14, "bold"), bg="#333333", fg="white"
        ).grid(row=5, column=0, pady=5, padx=10, sticky="w")
        menu_punto_conducta = tk.OptionMenu(contenedor, self.var_rango, *opciones_rango_bombero)
        menu_punto_conducta.config(
            font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666", relief="flat"
        )
        menu_punto_conducta.grid(row=6, column=0, columnspan=2, pady=(0,10), padx=10, sticky="we")
        menu_punto_conducta["menu"].config(font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white")

        # CONTRASEÑA
        tk.Label(
            contenedor, text="Contraseña:",
            font=("Arial", 14, "bold"), bg="#333333", fg="white"
        ).grid(row=7, column=0, pady=5, padx=10, sticky="w")
        self.entrada_pass = tk.Entry(
            contenedor,
            font=("Arial", 14, "bold"), bg="#4d4d4d", fg="white", show="*", insertbackground="white"
        )
        self.entrada_pass.grid(row=8, column=0, columnspan=2, pady=(0,10), padx=10, sticky="we")

        # DICCIONARIO
        entradas_personal = [
            self.entrada_legajo,
            self.entrada_apellido,
            self.entrada_nombre,
            self.entrada_dni,
            self.entrada_pass,
            self.var_rango
        ]

        # FRAME BOTONES
        frame_botones = tk.Frame(contenedor, bg="#333333")
        frame_botones.grid(row=9, column=0, columnspan=2, pady=(15,10), padx=10, sticky="we")
        frame_botones.columnconfigure(0, weight=1)

        # BOTÓN INGRESAR PERSONAL
        tk.Button(
            frame_botones, text="Ingresar Personal",
            font=("Arial", 14, "bold"), bg="#ffd966", fg="black", activebackground="#ff6666", activeforeground="white",
            relief="flat", bd=0, height=2,
            command=lambda: registrar_personal_revision(entradas_personal),
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=(0,10), sticky="we")

        # BOTÓN CUERPO BOMBEROS
        tk.Button(
            frame_botones, text="Cuerpo Bomberos",
            font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666", activeforeground="white",
            relief="flat", bd=0, height=2,
            command=lambda: abrir_ventana_listado_cuerpo_bomberos(self)
        ).grid(row=1, column=0, columnspan=2, padx=5, pady=(0,10), sticky="we")

        # BOTÓN SALIR
        tk.Button(
            frame_botones, text="Salir",
            font=("Arial", 14, "bold"), bg="#ffd966", fg="black", activebackground="#ff6666", activeforeground="white",
            relief="flat", bd=0, height=2,
            command=self.destroy
        ).grid(row=2, column=0, columnspan=2, padx=5, pady=(0,10), sticky="we")

if __name__ == "__main__":
    app = VentanaPersonal()
    app.mainloop()

# ====================== IMPORTACIONES ======================
import tkinter as tk
import datetime
from Axel_Operaciones_Conducta import puntuar_conducta_revision
from Axel_Ventana_Listado_Conducta import VentanaListadoConducta

# ====================== VENTANA ======================

class VentanaConducta(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Conducta")
        self.state("zoomed")
        self.configure(bg="#2b2b2b")
        self.ventana_listado_conducta = VentanaListadoConducta(self)
        self.crear_widgets()

    def crear_widgets(self):
        # MENU PUNTAJE
        opciones_punto_conducta = ["1", "0", "-1"]
        self.var_punto = tk.StringVar(value=opciones_punto_conducta[0])

        # MENU MESES
        meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio", "Julio","Agosto","Septiembre", "Octubre","Noviembre","Diciembre"]
        self.var_mes = tk.StringVar(value=meses[mes_actual - 1])

        # CONTENEDOR
        contenedor = tk.Frame(self, width=400, bg="#333333", bd=2, relief="ridge", padx=20, pady=20)
        contenedor.pack(expand=True, pady=40, padx=40)
        contenedor.pack_propagate(False)
        contenedor.columnconfigure(0, weight=1)

        # TÍTULO
        tk.Label(contenedor, text="GESTIÓN CONDUCTA",
                font=("Arial", 24, "bold"), fg="#ff4d4d", bg="#333333"
            ).grid(row=0, column=0, pady=(0,20))

        # LEGAJO
        tk.Label(contenedor, text="N° Legajo:",
                font=("Arial", 14, "bold"), fg="white", bg="#333333"
            ).grid(row=1, column=0, pady=(10,5), sticky="w")
        self.entrada_legajo = tk.Entry(contenedor, 
                                    font=("Arial", 14, "bold"), bg="#4d4d4d", fg="white", insertbackground="white")
        self.entrada_legajo.grid(row=2, column=0, pady=(0,10), sticky="we")

        # PUNTAJE
        tk.Label(contenedor, text="Punto:",
                font=("Arial", 14, "bold"), fg="white", bg="#333333"
            ).grid(row=3, column=0, pady=(10,5), sticky="w")
        menu_punto = tk.OptionMenu(contenedor, self.var_punto, *opciones_punto_conducta)
        menu_punto.config(font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666", relief="flat", width=20)
        menu_punto.grid(row=4, column=0, pady=(0,10), sticky="we")
        menu_punto["menu"].config(font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white")

        # FECHA ( Mes / Año )
        tk.Label(contenedor, text="Mes / Año:",
                font=("Arial", 14, "bold"), fg="white", bg="#333333"
            ).grid(row=5, column=0, pady=(10,5), sticky="w")
        frame_fecha = tk.Frame(contenedor, bg="#333333")
        frame_fecha.grid(row=6, column=0, pady=(0,10), sticky="we")
        frame_fecha.columnconfigure(0, weight=1)
        frame_fecha.columnconfigure(1, weight=1)

        # FECHA ( Mes )
        mes_actual = datetime.datetime.now().month
        menu_mes = tk.OptionMenu(frame_fecha, self.var_mes, *meses)
        menu_mes.config(font=("Arial", 14, "bold"), bg="#ffd966", fg="black", relief="flat", activebackground="#fbe190", width=20)
        menu_mes.grid(row=0, column=0, padx=(0,5), sticky="we")
        menu_mes["menu"].config(font=("Arial", 14, "bold"), bg="#ffd966", fg="black")

        # FECHA ( Año )
        self.entrada_anio = tk.Entry(frame_fecha,
                                    font=("Arial", 14, "bold"), justify="center", bg="#4d4d4d", fg="white", insertbackground="white"
                                )
        anio_actual = datetime.datetime.now().year
        self.entrada_anio.insert(0, str(anio_actual))
        self.entrada_anio.grid(row=0, column=1, padx=(5,0), sticky="we")

        # DICCIONARIO
        self.entradas_conducta = [
            self.entrada_legajo,
            self.var_punto,
            self.var_mes,
            self.entrada_anio
        ]

        # FRAME BOTONES
        frame_botones = tk.Frame(contenedor, bg="#333333")
        frame_botones.grid(row=7, column=0, pady=(20,0), sticky="we")
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)

        # BOTÓN PUNTUAR CONDUCTA
        tk.Button(frame_botones, text="Puntuar Conducta",
                font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666",
                height=2,
                command=lambda: puntuar_conducta_revision(self.entradas_conducta)
            ).grid(row=0, column=0, columnspan=2, padx=5, sticky="we")

        # BOTÓN REGISTRO CONDUCTA
        tk.Button(frame_botones, text="Registro Conductar",
                font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666",
                height=2,
                command=lambda: self.ventana_listado_conducta.mostrar_ventana_listado_conducta()
            ).grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="we")

        # BOTÓN SALIR
        tk.Button(frame_botones, text="Salir",
                font=("Arial", 14, "bold"), bg="#ffd966", fg="black", activebackground="#ff6666",
                height=2,
                command=self.destroy
            ).grid(row=4, column=0, columnspan=2, padx=5, sticky="we")

if __name__ == "__main__":
    app = VentanaConducta()
    app.mainloop()
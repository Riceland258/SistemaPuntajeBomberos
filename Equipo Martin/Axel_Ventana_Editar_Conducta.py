# ====================== IMPORTACIONES ======================
import tkinter as tk
from Axel_Operaciones_Conducta import actualizar_conducta_revision, borrar_conducta
from Axel_Utilidades import bloquear_botones_conducta, prevenir_doble_click, mostrar_info_personalizado, mostrar_error_personalizado, preguntar_si_no_personalizado

# ====================== VENTANA ======================

class VentanaEditorConducta(tk.Toplevel):
    def __init__(self, id_conducta, fila, parent=None, listado=None):
        super().__init__(parent)
        self.id_conducta = id_conducta
        self.fila = fila
        self.listado = listado
        self.title("Editor Conducta")
        self.configure(bg="#2b2b2b")
        self.crear_widgets()

    def crear_widgets(self):
        # MENU PUNTAJE
        opciones_punto = ["1", "0", "-1"]
        self.var_punto = tk.StringVar(value=str(self.fila["puntos"]))

        # MENU MESES
        meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio", "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.var_mes = tk.StringVar(value=meses[self.fila["mes"]-1])

        # CONTENEDOR
        contenedor = tk.Frame(self, width=400, bg="#333333", bd=2, relief="ridge", padx=20, pady=20)
        contenedor.pack(expand=True, padx=40, pady=40)
        contenedor.pack_propagate(False)
        contenedor.columnconfigure(0, weight=1)

        # TÍTULO
        tk.Label(contenedor, text="EDITOR CONDUCTAS",
                font=("Arial", 20, "bold"), fg="#ff4d4d", bg="#333333"
            ).grid(row=0, column=0, pady=(0,20))

        # LEGAJO
        tk.Label(contenedor, text="N° Legajo:",
                font=("Arial", 14, "bold"), fg="white", bg="#333333"
            ).grid(row=1, column=0, pady=(10,5), sticky="w")
        self.entrada_legajo = tk.Entry(contenedor, font=("Arial", 14, "bold"), bg="#4d4d4d", fg="white", insertbackground="white")
        self.entrada_legajo.insert(0, self.fila["nro_legajo"])
        self.entrada_legajo.grid(row=2, column=0, pady=(0,10), sticky="we")

        # PUNTAJE
        tk.Label(contenedor, text="Punto:",
                font=("Arial", 14, "bold"), fg="white", bg="#333333"
            ).grid(row=3, column=0, pady=(10,5), sticky="w")
        menu_punto = tk.OptionMenu(contenedor, self.var_punto, *opciones_punto)
        menu_punto.config(font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666", relief="flat", width=20)
        menu_punto.grid(row=4, column=0, pady=(0,10), sticky="we")
        menu_punto["menu"].config(font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white")

        # MES / AÑO
        tk.Label(contenedor, text="Mes / Año:",
                font=("Arial", 14, "bold"), fg="white", bg="#333333"
            ).grid(row=5, column=0, pady=(10,5), sticky="w")
        frame_fecha = tk.Frame(contenedor, bg="#333333")
        frame_fecha.grid(row=6, column=0, pady=(0,10), sticky="we")
        frame_fecha.columnconfigure(0, weight=1)
        frame_fecha.columnconfigure(1, weight=1)

        menu_mes = tk.OptionMenu(frame_fecha, self.var_mes, *meses)
        menu_mes.config(font=("Arial", 14, "bold"), bg="#ffd966", fg="black", relief="flat", activebackground="#fbe190", width=20)
        menu_mes.grid(row=0, column=0, padx=(0,5), sticky="we")
        menu_mes["menu"].config(font=("Arial", 14, "bold"), bg="#ffd966", fg="black")

        self.entrada_anio = tk.Entry(frame_fecha,
                                    font=("Arial", 14, "bold"), justify="center", bg="#4d4d4d", fg="white", insertbackground="white")
        self.entrada_anio.insert(0, str(self.fila["anio"]))
        self.entrada_anio.grid(row=0, column=1, padx=(5,0), sticky="we")

        # VALIDACIONES
        self.configurar_validaciones()

        # FRAME BOTONES
        frame_botones = tk.Frame(contenedor, bg="#333333")
        frame_botones.grid(row=7, column=0, pady=(20,0), sticky="we")
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)

        # BOTÓN ACTUALIZAR
        tk.Button(frame_botones, text="Actualizar",
                font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666", height=2,
                command=self.procesar_actualizacion
            ).grid(row=0, column=0, padx=5, sticky="we")

        # BOTÓN BORRAR
        tk.Button(frame_botones, text="Borrar",
                font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666", height=2,
                command=self.borrar_conducta_dc
            ).grid(row=0, column=1, padx=5, sticky="we")

        # BOTÓN CANCELAR
        tk.Button(frame_botones, text="Cancelar",
                font=("Arial", 14, "bold"), bg="#ffd966", fg="black", activebackground="#ff6666", height=2,
                command=self.destroy
            ).grid(row=1, column=0, columnspan=2, padx=5, pady=(10,0), sticky="we")

        # Bloquear botones según permisos
        bloquear_botones_conducta(self)

    def configurar_validaciones(self):
        # Validación para solo números en legajo y año
        def solo_numeros(char):
            return char.isdigit()
        
        validacion_numeros = (self.register(solo_numeros), '%S')
        
        self.entrada_legajo.config(validate='key', validatecommand=validacion_numeros)
        self.entrada_anio.config(validate='key', validatecommand=validacion_numeros)

    def procesar_actualizacion(self):
        entradas_conducta = [
            self.entrada_legajo,
            self.var_punto,
            self.var_mes,
            self.entrada_anio
        ]
        actualizado = actualizar_conducta_revision(self.id_conducta, entradas_conducta)
        if actualizado:
            if self.listado:
                self.listado.recargar_tabla()
            self.destroy()

    def borrar_conducta_dc(self):
        try:
            # Prevenir doble click
            prevenir_doble_click(self, "Borrar")
            
            # Confirmación de borrado
            confirmacion = preguntar_si_no_personalizado(
                "Confirmar", 
                "¿Seguro que quieres borrar esta conducta?",
                self
            )
            
            if confirmacion:
                exito = borrar_conducta(self.id_conducta)
                if exito:
                    mostrar_info_personalizado("Éxito", "Puntaje de conducta eliminado", self)
                    if self.listado:
                        self.listado.recargar_tabla()
                    self.destroy()
                else:
                    mostrar_error_personalizado("Error", "No se pudo eliminar el puntaje", self)
                    
        except Exception:
            mostrar_error_personalizado("Error", "Error al eliminar", self)

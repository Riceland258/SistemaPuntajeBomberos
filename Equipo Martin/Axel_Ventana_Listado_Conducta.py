# ====================== IMPORTACIONES ======================
import tkinter as tk
from tkinter import ttk
from Axel_Base_de_Datos import Conectar
from Axel_Utilidades import centrar_ventana, bloquear_botones_conducta, mostrar_error_personalizado, mostrar_advertencia_personalizado
from Axel_Operaciones_Conducta import volver_ventana_principal_conducta

# ====================== VENTANA ======================

class VentanaListadoConducta(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Registros de conducta")
        self.withdraw()
        self.MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.FILAS_POR_BLOQUE = 50
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
        frame_superior.pack(fill="x", pady=(0,10))

        tk.Label(frame_superior, text="REGISTROS DE CONDUCTA",
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
                command=self.buscar
            ).pack(side="left", padx=(5,0))

        self.entry_buscar.bind("<Return>", lambda e: self.buscar())
        self.entry_buscar.bind("<FocusOut>", lambda e: self.buscar_si_vacio())
        self.entry_buscar.bind("<KeyRelease>", self.buscar_con_retraso)

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
        
        self.tree.bind("<Double-1>", self.on_double_click)
        # Múltiples eventos de scroll para detección inmediata
        scrollbar.bind("<ButtonRelease-1>", self.on_scroll)
        scrollbar.bind("<B1-Motion>", self.on_scroll)  # Mientras arrastra la barra
        self.tree.bind("<MouseWheel>", self.on_scroll)  # Rueda del mouse
        self.tree.bind("<Button-4>", self.on_scroll)    # Scroll up en Linux
        self.tree.bind("<Button-5>", self.on_scroll)    # Scroll down en Linux
        self.tree.bind("<Up>", self.on_scroll)          # Flecha arriba
        self.tree.bind("<Down>", self.on_scroll)        # Flecha abajo
        self.tree.bind("<Prior>", self.on_scroll)       # Page up
        self.tree.bind("<Next>", self.on_scroll)        # Page down

        # FRAME INFERIOR
        frame_botones = tk.Frame(marco, bg="#2b2b2b")
        frame_botones.pack(fill="x", pady=10)

        # BOTÓN EDITAR
        self.btn_actualizar = tk.Button(frame_botones, text="Editar",
                                        font=("Arial", 14, "bold"), width=20, bg="#ff4d4d", fg="white", activebackground="#ffd966",
                                        command=lambda: self.editar_fila()
                                    )
        self.btn_actualizar.pack(side="left", padx=5, pady=5, expand=True)

        # BOTÓN CARGAR MÁS - Pequeño signo "+" en el centro
        self.btn_mas = tk.Button(frame_botones, text="+",
                                font=("Arial", 18, "bold"), width=3, 
                                bg="#4d4d4d", fg="white", activebackground="#666666",
                                command=self.cargar_mas_manual,
                                relief="solid", bd=1
                            )

        # BOTÓN VOLVER
        self.btn_volver = tk.Button(frame_botones, text="Volver",
                                    font=("Arial", 14, "bold"), width=20, bg="#ffd966", fg="#000000", activebackground="#ff4d4d",
                                    command=lambda: volver_ventana_principal_conducta(self)
                                )
        self.btn_volver.pack(side="right", padx=5, pady=5, expand=True)

        # Variable para controlar si hay más registros
        self.hay_mas_registros = True
        
        # Bloquear botones según permisos
        bloquear_botones_conducta(self)
        
        self.cargar_mas()

    def mostrar_ventana_listado_conducta(self):
        self.deiconify()
        self.recargar_tabla()
        self.state("zoomed")
        self.lift()
        # Asegurar que el scroll esté al inicio al mostrar la ventana
        self.after(100, lambda: self.tree.yview_moveto(0))
        if self.parent:
            # Ocultar la actual después de un pequeño retraso
            self.after(50, lambda: self.parent.withdraw())

    def abrir_actualizar(self, fila):
        from Axel_Ventana_Editar_Conducta import VentanaEditorConducta
        ventana = VentanaEditorConducta(fila["id_conducta"], fila, parent=self, listado=self)
        centrar_ventana(ventana)
        ventana.grab_set()
        ventana.focus()

    def recargar_tabla(self):
        self.offset = 0
        self.filtro_actual = ""
        self.tree.delete(*self.tree.get_children())
        # Reiniciar scroll al inicio
        self.tree.yview_moveto(0)
        self.cargar_mas()

    def cargar_mas(self):
        try:
            conexion = Conectar()
            cursor = conexion.cursor(dictionary=True)
            
            if self.filtro_actual:
                filtro_texto = self.filtro_actual.strip()
                
                # Si es un número exacto (legajo), buscar solo ese legajo específico
                if filtro_texto.isdigit():
                    cursor.execute(
                        "SELECT c.id_conducta, c.nro_legajo, c.puntos, c.mes, c.anio, p.apellido_nombre "
                        "FROM conducta_personal c "
                        "INNER JOIN personal p ON c.nro_legajo = p.nro_legajo "
                        "WHERE c.nro_legajo = %s "
                        "AND p.borradopersonal = 'E' "
                        "ORDER BY c.nro_legajo ASC, c.anio DESC, c.mes DESC, c.id_conducta DESC "
                        "LIMIT %s OFFSET %s",
                        (int(filtro_texto), self.FILAS_POR_BLOQUE, self.offset)
                    )
                else:
                    # Si es texto, buscar por coincidencia parcial en legajo o nombre
                    cursor.execute(
                        "SELECT c.id_conducta, c.nro_legajo, c.puntos, c.mes, c.anio, p.apellido_nombre "
                        "FROM conducta_personal c "
                        "INNER JOIN personal p ON c.nro_legajo = p.nro_legajo "
                        "WHERE (CAST(c.nro_legajo AS CHAR) LIKE %s OR p.apellido_nombre LIKE %s) "
                        "AND p.borradopersonal = 'E' "
                        "ORDER BY c.nro_legajo ASC, c.anio DESC, c.mes DESC, c.id_conducta DESC "
                        "LIMIT %s OFFSET %s",
                        (f"%{filtro_texto}%", f"%{filtro_texto}%", self.FILAS_POR_BLOQUE, self.offset)
                    )
            else:
                # Búsqueda general: ordenar por ID (más recientes primero)
                cursor.execute(
                    "SELECT c.id_conducta, c.nro_legajo, c.puntos, c.mes, c.anio, p.apellido_nombre "
                    "FROM conducta_personal c "
                    "INNER JOIN personal p ON c.nro_legajo = p.nro_legajo "
                    "WHERE p.borradopersonal = 'E' "
                    "ORDER BY c.id_conducta DESC "
                    "LIMIT %s OFFSET %s",
                    (self.FILAS_POR_BLOQUE, self.offset)
                )
            
            bloque = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            for i, fila in enumerate(bloque):
                tag = "evenrow" if (self.offset + i) % 2 == 0 else "oddrow"
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        fila["nro_legajo"],
                        fila["apellido_nombre"],
                        fila["puntos"],
                        self.MESES[fila["mes"]-1],
                        fila["anio"]
                    ),
                    tags=(tag,),
                    iid=fila["id_conducta"]
                )

            self.offset += len(bloque)

            # Controlar si hay más registros
            if len(bloque) < self.FILAS_POR_BLOQUE:
                self.hay_mas_registros = False
                self.btn_mas.place_forget()
            else:
                self.hay_mas_registros = True
                # No mostrar el botón automáticamente, dejar que on_scroll() lo maneje
                
        except Exception as e:
            mostrar_error_personalizado("Error", "Hubo un problema al cargar los registros", self)

    def editar_fila(self):
        seleccion = self.tree.selection()
        if seleccion:
            iid = seleccion[0]
            item = self.tree.item(iid)
            values = item["values"]
            fila = {
                "nro_legajo": values[0],
                "apellido_nombre": values[1],
                "puntos": values[2],
                "mes": self.MESES.index(values[3]) + 1,
                "anio": values[4],
                "id_conducta": int(iid)
            }
            self.abrir_actualizar(fila)
        else:
            mostrar_advertencia_personalizado("Atención", "Debe seleccionar una fila antes de actualizar", self)

    def buscar(self):
        self.filtro_actual = self.entry_buscar.get().strip()
        self.offset = 0
        self.tree.delete(*self.tree.get_children())
        # Ocultar el botón inicialmente y dejar que cargar_mas() determine si debe mostrarse
        if hasattr(self, 'btn_mas'):
            self.btn_mas.place_forget()
        # Reiniciar scroll al inicio
        self.tree.yview_moveto(0)
        self.cargar_mas()

    def buscar_si_vacio(self):
        if self.entry_buscar.get().strip() == "":
            self.filtro_actual = ""
            self.offset = 0
            self.tree.delete(*self.tree.get_children())
            # Ocultar el botón inicialmente y dejar que cargar_mas() determine si debe mostrarse
            if hasattr(self, 'btn_mas'):
                self.btn_mas.place_forget()
            # Reiniciar scroll al inicio
            self.tree.yview_moveto(0)
            self.cargar_mas()

    def on_double_click(self, event):
        self.editar_fila()

    def buscar_con_retraso(self, event):
        if hasattr(self, 'timer_busqueda'):
            self.after_cancel(self.timer_busqueda)
        
        texto_actual = self.entry_buscar.get().strip()
        
        if not texto_actual:
            self.filtro_actual = ""
            self.offset = 0
            self.tree.delete(*self.tree.get_children())
            # Ocultar el botón inicialmente y dejar que cargar_mas() determine si debe mostrarse
            if hasattr(self, 'btn_mas'):
                self.btn_mas.place_forget()
            # Reiniciar scroll al inicio
            self.tree.yview_moveto(0)
            self.cargar_mas()
        else:
            self.timer_busqueda = self.after(800, self.buscar)

    def on_scroll(self, event):
        # Solo mostrar el botón si hay más registros Y hay suficientes registros cargados
        if self.hay_mas_registros and len(self.tree.get_children()) >= self.FILAS_POR_BLOQUE:
            # Obtener la posición del scroll
            top, bottom = self.tree.yview()
            # Si está cerca del final (85% o más), mostrar el botón "+" en el centro
            if bottom >= 0.85:
                # Obtener las dimensiones del frame de botones para centrar el "+"
                frame_width = self.btn_actualizar.master.winfo_width()
                if frame_width > 1:  # Solo si el frame ya tiene dimensiones
                    # Calcular posición centrada
                    x_centro = frame_width // 2 - 20  # Ajustar para centrar mejor
                    # Usar la misma posición Y que los otros botones (5px de padding)
                    self.btn_mas.place(x=x_centro, y=5, height=32)  # Misma altura que los otros
            else:
                self.btn_mas.place_forget()
        else:
            # Si no hay más registros o hay pocos registros, ocultar el botón
            self.btn_mas.place_forget()

    def cargar_mas_manual(self):
        self.cargar_mas()
        self.btn_mas.place_forget()

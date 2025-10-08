# ====================== IMPORTACIONES ======================
import tkinter as tk
from Axel_Operaciones_Personal import actualizar_bombero
from Axel_Utilidades import prevenir_doble_click, bloquear_botones_personal, mostrar_error_personalizado, mostrar_advertencia_personalizado, preguntar_si_no_personalizado

# ====================== VENTANA ======================

class VentanaEditorBomberos(tk.Toplevel):
    def __init__(self, parent=None, datos_bombero=None):
        super().__init__(parent)
        self.parent = parent
        self.datos_bombero = datos_bombero or {}
        self.title("Editor Bomberos")
        self.configure(bg="#2b2b2b")
        self.crear_tabla()

    def crear_tabla(self):
        # MENUS
        opciones_rol_bombero = ["3", "2", "1"]
        self.var_rol = tk.StringVar(value=opciones_rol_bombero[0])

        # CONTENEDOR
        contenedor = tk.Frame(self, width=400, bg="#333333", bd=2, relief="ridge", padx=10, pady=10)
        contenedor.pack(expand=True, pady=20, padx=20)
        contenedor.pack_propagate(False)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)

        # TÍTULO
        tk.Label(
            contenedor, text="EDITOR BOMBEROS",
            font=("Arial", 24, "bold"), fg="#ff4d4d", bg="#333333"
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
            contenedor, font=("Arial", 14, "bold"),
            bg="#4d4d4d", fg="white", insertbackground="white"
        )
        self.entrada_dni.grid(row=2, column=1, pady=(0,10), padx=(5,10), sticky="we")

        # APELLIDO
        tk.Label(
            contenedor, text="Apellido:",
            font=("Arial", 14, "bold"), bg="#333333", fg="white"
        ).grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.entrada_apellido = tk.Entry(
            contenedor, font=("Arial", 14, "bold"),
            bg="#4d4d4d", fg="white", insertbackground="white"
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

        # ROL
        tk.Label(
            contenedor, text="Rol:",
            font=("Arial", 14, "bold"), bg="#333333", fg="white"
        ).grid(row=5, column=0, pady=5, padx=10, sticky="w")
        menu_punto_conducta = tk.OptionMenu(contenedor, self.var_rol, *opciones_rol_bombero)
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
        self.entradas_personal = {
            "nro_legajo": self.entrada_legajo,
            "dni": self.entrada_dni,
            "apellido": self.entrada_apellido,
            "nombre": self.entrada_nombre,
            "rol": self.var_rol,
            "pass": self.entrada_pass,
        }

        # FRAME BOTONES
        frame_botones = tk.Frame(contenedor, bg="#333333")
        frame_botones.grid(row=9, column=0, columnspan=2, pady=(15,10), padx=10, sticky="we")
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)

        # BOTÓN ACTUALIZAR
        tk.Button(
            frame_botones, text="Actualizar",
            font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666", activeforeground="white",
            relief="flat", bd=0, height=2,
            command=self.actualizar_bombero
        ).grid(row=0, column=0, padx=5, pady=(0,10), sticky="we")

        # BOTÓN BORRAR
        tk.Button(
            frame_botones, text="Borrar",
            font=("Arial", 14, "bold"), bg="#ff4d4d", fg="white", activebackground="#ff6666", activeforeground="white",
            relief="flat", bd=0, height=2,
            command=self.borrar_bombero_dc
        ).grid(row=0, column=1, padx=5, pady=(0,10), sticky="we")

        # BOTÓN VOLVER
        tk.Button(
            frame_botones, text="Cerrar",
            font=("Arial", 14, "bold"), bg="#ffd966", fg="black", activebackground="#ff6666", activeforeground="white",
            relief="flat", bd=0, height=2,
            command=self.destroy,
        ).grid(row=1, column=0, columnspan=2, padx=5, pady=(0,10), sticky="we")

        # Bloquear botones según permisos
        bloquear_botones_personal(self)

        self.cargar_datos()

    def cargar_datos(self):
        if self.datos_bombero and 'nro_legajo' in self.datos_bombero:
            from Operaciones_Personal import obtener_datos_bombero
            datos_completos = obtener_datos_bombero(self.datos_bombero['nro_legajo'])
            
            if datos_completos:
                # Cargar legajo
                self.entrada_legajo.insert(0, str(datos_completos['nro_legajo']))
                self.entrada_legajo.config(state='disabled')

                # Cargar DNI
                self.entrada_dni.insert(0, str(datos_completos['dni']))
                
                # Separar apellido y nombre
                apellido_nombre = datos_completos.get('apellido_nombre', '')
                if ', ' in apellido_nombre:
                    apellido, nombre = apellido_nombre.split(', ', 1)
                    self.entrada_apellido.insert(0, apellido)
                    self.entrada_nombre.insert(0, nombre)
                else:
                    self.entrada_apellido.insert(0, apellido_nombre)
                
                # Cargar rol
                self.var_rol.set(str(datos_completos['rol']))
                
                # Cargar contraseña
                self.entrada_pass.insert(0, datos_completos.get('pass', ''))

    def actualizar_bombero(self):
        try:
            # Evita doble click
            prevenir_doble_click(self, "Actualizar")
            
            resultado = actualizar_bombero(self.entradas_personal)
            if resultado is True:

                if self.parent and hasattr(self.parent, 'tree') and hasattr(self.parent, 'cargar_mas'):
                    # Limpiar la tabla actual
                    self.parent.tree.delete(*self.parent.tree.get_children())
                    # Resetear para cargar desde el principio
                    self.parent.offset = 0
                    # Recargar los datos
                    self.parent.cargar_mas()
                
                self.destroy()
                
        except Exception:
            mostrar_error_personalizado("Error", "Error inesperado", self)

    def borrar_bombero_dc(self):
        try:
            from Operaciones_Personal import borrar_bombero_logico
            
            # Evitar doble click
            prevenir_doble_click(self, "Borrar")
            
            # Obtener los datos del bombero actual
            if self.datos_bombero and 'nro_legajo' in self.datos_bombero:
                nro_legajo = self.datos_bombero['nro_legajo']
                apellido_nombre = self.entrada_apellido.get() + ", " + self.entrada_nombre.get()
                
                # Confirmar eliminación
                respuesta = preguntar_si_no_personalizado(
                    "Confirmar Eliminación", 
                    f"¿Está seguro que desea eliminar al bombero?\n\n"
                    f"Legajo: {nro_legajo}\n"
                    f"Nombre: {apellido_nombre}\n\n"
                    f"Esta acción marcará al bombero como eliminado.",
                    self
                )
                
                if respuesta:
                    if borrar_bombero_logico(nro_legajo):
                        # Actualizar la tabla padre si existe
                        if self.parent and hasattr(self.parent, 'tree') and hasattr(self.parent, 'cargar_mas'):
                            self.parent.tree.delete(*self.parent.tree.get_children())
                            self.parent.offset = 0
                            self.parent.cargar_mas()
                        
                        # Cerrar el editor
                        self.destroy()
            else:
                mostrar_advertencia_personalizado("Advertencia", "No se pudo obtener los datos del bombero.", self)
                
        except Exception as e:
            mostrar_error_personalizado("Error", f"Error al eliminar bombero: {str(e)}", self)

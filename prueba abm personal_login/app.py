import tkinter as tk
from tkinter import ttk, messagebox
import Database as db
import Funciones as fn

class PersonalABM:
    def __init__(self, root, database):
        self.root = root
        self.db = database
        self.setup_ui()
        self.cargar_datos()
        
    def setup_ui(self):
        self.root.title('ABM Personal de Bomberos')
        self.root.geometry('1000x700')
        self.root.configure(bg='#f0f0f0')
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        title_label = ttk.Label(main_frame, text="Gestión de Personal de Bomberos", 
                              font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Personal", padding="10")
        form_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(form_frame, text="Nro. Legajo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_legajo = ttk.Entry(form_frame, width=20)
        self.entry_legajo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(form_frame, text="Apellido y Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_apellido_nombre = ttk.Entry(form_frame, width=20)
        self.entry_apellido_nombre.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(form_frame, text="DNI:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_dni = ttk.Entry(form_frame, width=20)
        self.entry_dni.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(form_frame, text="Usuario:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_user = ttk.Entry(form_frame, width=20)
        self.entry_user.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_password = ttk.Entry(form_frame, width=20, show="*")
        self.entry_password.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Crear", command=self.crear_personal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_personal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_personal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.LabelFrame(form_frame, text="Búsqueda", padding="10")
        search_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.search_combo = ttk.Combobox(search_frame, values=["nro_legajo", "apellido_nombre", "dni"], 
                                       state="readonly", width=15)
        self.search_combo.grid(row=0, column=1, padx=5)
        self.search_combo.set("apellido_nombre")
        
        self.entry_search = ttk.Entry(search_frame, width=20)
        self.entry_search.grid(row=0, column=2, padx=5)
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_personal).grid(row=0, column=3, padx=5)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.cargar_datos).grid(row=0, column=4, padx=5)
        
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Personal", padding="10")
        table_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        columns = ('Legajo', 'Apellido y Nombre', 'DNI', 'Usuario', 'Contraseña')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('Legajo', text='Nro. Legajo')
        self.tree.heading('Apellido y Nombre', text='Apellido y Nombre')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Usuario', text='Usuario')
        self.tree.heading('Contraseña', text='Contraseña')
        
        self.tree.column('Legajo', width=100)
        self.tree.column('Apellido y Nombre', width=200)
        self.tree.column('DNI', width=100)
        self.tree.column('Usuario', width=100)
        self.tree.column('Contraseña', width=100)
        
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.tree.bind('<Double-1>', self.seleccionar_personal)
        
        form_frame.columnconfigure(1, weight=1)
        
    def limpiar_campos(self):
        """Limpiar todos los campos del formulario"""
        self.entry_legajo.delete(0, tk.END)
        self.entry_apellido_nombre.delete(0, tk.END)
        self.entry_dni.delete(0, tk.END)
        self.entry_user.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        
    def validar_campos(self):
        """Validar que los campos requeridos estén completos"""
        if not self.entry_legajo.get().strip():
            messagebox.showerror("Error", "El número de legajo es requerido")
            return False
        if not self.entry_apellido_nombre.get().strip():
            messagebox.showerror("Error", "El apellido y nombre es requerido")
            return False
        if not self.entry_dni.get().strip():
            messagebox.showerror("Error", "El DNI es requerido")
            return False
        if not self.entry_user.get().strip():
            messagebox.showerror("Error", "El usuario es requerido")
            return False
        if not self.entry_password.get().strip():
            messagebox.showerror("Error", "La contraseña es requerida")
            return False
            
        try:
            int(self.entry_legajo.get())
        except ValueError:
            messagebox.showerror("Error", "El número de legajo debe ser un número")
            return False
            
        try:
            int(self.entry_dni.get())
        except ValueError:
            messagebox.showerror("Error", "El DNI debe ser un número")
            return False
            
        return True
        
    def crear_personal(self):
        """Crear un nuevo registro de personal"""
        if not self.validar_campos():
            return
            
        nro_legajo = int(self.entry_legajo.get())
        apellido_nombre = self.entry_apellido_nombre.get().strip()
        dni = int(self.entry_dni.get())
        user = self.entry_user.get().strip()
        password = self.entry_password.get().strip()
        
        exito, mensaje = fn.Personal_Crear(self.db, nro_legajo, apellido_nombre, dni, user, password)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", mensaje)
            
    def actualizar_personal(self):
        """Actualizar un registro existente de personal"""
        if not self.validar_campos():
            return
            
        nro_legajo = int(self.entry_legajo.get())
        apellido_nombre = self.entry_apellido_nombre.get().strip()
        dni = int(self.entry_dni.get())
        user = self.entry_user.get().strip()
        password = self.entry_password.get().strip()
        
        exito, mensaje = fn.Personal_Actualizar(self.db, nro_legajo, apellido_nombre, dni, user, password)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", mensaje)
            
    def eliminar_personal(self):
        """Eliminar un registro de personal"""
        if not self.entry_legajo.get().strip():
            messagebox.showerror("Error", "Seleccione un personal para eliminar")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este personal?"):
            nro_legajo = int(self.entry_legajo.get())
            exito, mensaje = fn.Personal_Eliminar(self.db, nro_legajo)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_campos()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", mensaje)
                
    def buscar_personal(self):
        """Buscar personal según criterio seleccionado"""
        campo = self.search_combo.get()
        valor = self.entry_search.get().strip()
        
        if not valor:
            messagebox.showerror("Error", "Ingrese un valor para buscar")
            return
            
        registros = fn.Personal_Buscar(self.db, campo, valor)
        self.actualizar_tabla(registros)
        
    def cargar_datos(self):
        """Cargar todos los datos en la tabla"""
        registros = fn.Personal_Leer_Todos(self.db)
        self.actualizar_tabla(registros)
        
    def actualizar_tabla(self, registros):
        """Actualizar la tabla con los registros proporcionados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for registro in registros:
            self.tree.insert('', tk.END, values=registro)
            
    def seleccionar_personal(self, event):
        """Seleccionar un personal de la tabla y cargar sus datos en el formulario"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.limpiar_campos()
            self.entry_legajo.insert(0, str(values[0]))
            self.entry_apellido_nombre.insert(0, values[1])
            self.entry_dni.insert(0, str(values[2]))
            self.entry_user.insert(0, values[3])
            self.entry_password.insert(0, values[4])

ROOT = tk.Tk()
PAD = 12
COLOR_BG = '#f0f0f0'

if __name__ == '__main__':
    try:
        DB = db.Conectar_DB()
        
        app = PersonalABM(ROOT, DB)
        
        ROOT.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {str(e)}")
        print(f"Error: {str(e)}")
    finally:
        try:
            DB.close()
        except:
            pass
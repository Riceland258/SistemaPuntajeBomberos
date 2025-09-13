import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'bomberos',
}

COLUMNS = (
    'nro_legajo',
    'apellido_nombre',
    'dni',
    'user',
    'pass',
)

PAD = 8


def get_connection():
    """Crea y devuelve una conexión a MySQL utilizando DB_CONFIG."""
    return mysql.connector.connect(**DB_CONFIG)


def build_ui(parent):
    main = ttk.Frame(parent, padding=PAD)
    main.pack(fill='both', expand=True)
    main.columnconfigure(0, weight=1)

    title = ttk.Label(main, text='ABM Personal', font=('Segoe UI', 16, 'bold'))
    title.grid(row=0, column=0, sticky='w', pady=(0, PAD))

    form = ttk.LabelFrame(main, text='Datos del personal', padding=PAD)
    form.grid(row=1, column=0, sticky='ew', padx=(0, 0))
    for i in range(8):
        form.columnconfigure(i, weight=1)

    var_legajo = tk.StringVar()
    var_apellido_nombre = tk.StringVar()
    var_dni = tk.StringVar()
    var_user = tk.StringVar()
    var_pass = tk.StringVar()

    ttk.Label(form, text='Nro Legajo*').grid(row=0, column=0, sticky='w')
    ent_legajo = ttk.Entry(form, textvariable=var_legajo, width=15)
    ent_legajo.grid(row=1, column=0, sticky='ew', padx=(0, PAD))

    ttk.Label(form, text='Apellido y Nombre*').grid(row=0, column=1, sticky='w')
    ent_apellido_nombre = ttk.Entry(form, textvariable=var_apellido_nombre)
    ent_apellido_nombre.grid(row=1, column=1, columnspan=3, sticky='ew', padx=(0, PAD))

    ttk.Label(form, text='DNI*').grid(row=0, column=4, sticky='w')
    ent_dni = ttk.Entry(form, textvariable=var_dni, width=15)
    ent_dni.grid(row=1, column=4, sticky='ew', padx=(0, PAD))

    ttk.Label(form, text='Usuario*').grid(row=0, column=5, sticky='w')
    ent_user = ttk.Entry(form, textvariable=var_user)
    ent_user.grid(row=1, column=5, sticky='ew', padx=(0, PAD))

    ttk.Label(form, text='Contraseña*').grid(row=0, column=6, sticky='w')
    ent_pass = ttk.Entry(form, textvariable=var_pass, show='•')
    ent_pass.grid(row=1, column=6, sticky='ew', padx=(0, PAD))

    btns = ttk.Frame(form)
    btns.grid(row=1, column=7, sticky='e')

    var_search = tk.StringVar()

    search_bar = ttk.LabelFrame(main, text='Buscar', padding=PAD)
    search_bar.grid(row=2, column=0, sticky='ew', pady=(PAD, 0))
    search_bar.columnconfigure(1, weight=1)
    ttk.Label(search_bar, text='Texto:').grid(row=0, column=0, sticky='w')
    ent_search = ttk.Entry(search_bar, textvariable=var_search)
    ent_search.grid(row=0, column=1, sticky='ew', padx=(PAD//2, PAD))

    table_frame = ttk.Frame(main, padding=(0, PAD, 0, 0))
    table_frame.grid(row=3, column=0, sticky='nsew')
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    tree = ttk.Treeview(
        table_frame,
        columns=COLUMNS,
        show='headings',
        height=14,
    )
    tree.heading('nro_legajo', text='Legajo')
    tree.heading('apellido_nombre', text='Apellido y Nombre')
    tree.heading('dni', text='DNI')
    tree.heading('user', text='Usuario')
    tree.heading('pass', text='Contraseña')
    tree.column('nro_legajo', width=100, anchor='center')
    tree.column('apellido_nombre', width=280)
    tree.column('dni', width=120, anchor='center')
    tree.column('user', width=140, anchor='center')
    tree.column('pass', width=140, anchor='center')
    tree.grid(row=0, column=0, sticky='nsew')
    vsb = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    hsb = ttk.Scrollbar(table_frame, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    state = {
        'root': parent,
        'tree': tree,
        'var_legajo': var_legajo,
        'var_apellido_nombre': var_apellido_nombre,
        'var_dni': var_dni,
        'var_user': var_user,
        'var_pass': var_pass,
        'var_search': var_search,
        'ent_legajo': ent_legajo,
    }

    def bind_select(event):
        on_select_row_handler(state)

    tree.bind('<<TreeviewSelect>>', bind_select)

    ttk.Button(btns, text='Nuevo', command=lambda: clear_form(state)).grid(row=0, column=0, padx=2)
    ttk.Button(btns, text='Guardar', command=lambda: create_or_update(state)).grid(row=0, column=1, padx=2)
    ttk.Button(btns, text='Eliminar', command=lambda: delete_selected(state)).grid(row=0, column=2, padx=2)
    ttk.Button(search_bar, text='Buscar', command=lambda: search(state)).grid(row=0, column=2)
    ttk.Button(search_bar, text='Refrescar', command=lambda: refresh(state)).grid(row=0, column=3, padx=(PAD//2, 0))

    return state

def clear_form(state):
    state['var_legajo'].set('')
    state['var_apellido_nombre'].set('')
    state['var_dni'].set('')
    state['var_user'].set('')
    state['var_pass'].set('')
    state['ent_legajo'].focus_set()

def on_select_row_handler(state):
    tree = state['tree']
    sel = tree.selection()
    if not sel:
        return
    item = tree.item(sel[0])
    values = item['values']
    if not values:
        return
    state['var_legajo'].set(values[0])
    state['var_apellido_nombre'].set(values[1])
    state['var_dni'].set(values[2])
    state['var_user'].set(values[3])
    state['var_pass'].set(values[4])

def populate_table(state, rows):
    tree = state['tree']
    tree.delete(*tree.get_children())
    for r in rows:
        tree.insert('', 'end', values=r)

def _validate_inputs(state):
    if not state['var_legajo'].get().strip() or not state['var_apellido_nombre'].get().strip() or not state['var_dni'].get().strip() or not state['var_user'].get().strip() or not state['var_pass'].get().strip():
        messagebox.showwarning('Validación', 'Todos los campos con * son obligatorios.')
        return None
    try:
        legajo = int(state['var_legajo'].get())
    except ValueError:
        messagebox.showwarning('Validación', 'El Nro Legajo debe ser numérico.')
        return None
    try:
        dni = int(state['var_dni'].get())
    except ValueError:
        messagebox.showwarning('Validación', 'El DNI debe ser numérico.')
        return None
    usuario = state['var_user'].get().strip()
    clave = state['var_pass'].get()
    nombre = state['var_apellido_nombre'].get().strip()
    if len(usuario) > 20:
        messagebox.showwarning('Validación', 'Usuario no debe superar 20 caracteres.')
        return None
    if len(clave) > 8:
        messagebox.showwarning('Validación', 'Contraseña no debe superar 8 caracteres.')
        return None
    if len(nombre) > 100:
        messagebox.showwarning('Validación', 'Apellido y Nombre no debe superar 100 caracteres.')
        return None
    return {
        'nro_legajo': legajo,
        'apellido_nombre': nombre,
        'dni': dni,
        'user': usuario,
        'pass': clave,
    }

def refresh(state):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT nro_legajo, apellido_nombre, dni, user, pass FROM personal ORDER BY nro_legajo ASC')
        rows = cur.fetchall()
        populate_table(state, rows)
    except Error as e:
        messagebox.showerror('DB Error', f'No se pudo obtener el listado.\n{e}')
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

def search(state):
    q = state['var_search'].get().strip()
    if not q:
        refresh(state)
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        params = []
        where = []
        if q.isdigit():
            where.append('(nro_legajo = %s OR dni = %s)')
            params.extend([int(q), int(q)])
        like = f"%{q}%"
        where.append('(apellido_nombre LIKE %s OR user LIKE %s)')
        params.extend([like, like])
        sql = 'SELECT nro_legajo, apellido_nombre, dni, user, pass FROM personal WHERE ' + ' OR '.join(where) + ' ORDER BY nro_legajo ASC'
        cur.execute(sql, params)
        rows = cur.fetchall()
        populate_table(state, rows)
    except Error as e:
        messagebox.showerror('DB Error', f'No se pudo buscar.\n{e}')
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

def create_or_update(state):
    data = _validate_inputs(state)
    if not data:
        return
    legajo = data['nro_legajo']
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(1) FROM personal WHERE nro_legajo=%s', (legajo,))
        exists = cur.fetchone()[0] == 1
        if exists:
            cur.execute(
                'UPDATE personal SET apellido_nombre=%s, dni=%s, user=%s, pass=%s WHERE nro_legajo=%s',
                (data['apellido_nombre'], data['dni'], data['user'], data['pass'], legajo)
            )
            conn.commit()
            messagebox.showinfo('Actualizado', f'Legajo {legajo} actualizado correctamente.')
        else:
            cur.execute(
                'INSERT INTO personal (nro_legajo, apellido_nombre, dni, user, pass) VALUES (%s, %s, %s, %s, %s)',
                (data['nro_legajo'], data['apellido_nombre'], data['dni'], data['user'], data['pass'])
            )
            conn.commit()
            messagebox.showinfo('Creado', f'Legajo {legajo} creado correctamente.')
        refresh(state)
        _select_row_by_legajo(state, legajo)
    except Error as e:
        if getattr(e, 'errno', None) == 1062:
            messagebox.showerror('Duplicado', f'El legajo {legajo} ya existe.')
        else:
            messagebox.showerror('DB Error', f'No se pudo guardar.\n{e}')
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

def _select_row_by_legajo(state, legajo):
    tree = state['tree']
    for iid in tree.get_children():
        vals = tree.item(iid, 'values')
        if not vals:
            continue
        if str(vals[0]) == str(legajo):
            tree.selection_set(iid)
            tree.see(iid)
            on_select_row_handler(state)
            break

def delete_selected(state):
    tree = state['tree']
    sel = tree.selection()
    if not sel:
        messagebox.showinfo('Eliminar', 'Seleccione un registro para eliminar.')
        return
    item = tree.item(sel[0])
    values = item['values']
    if not values:
        return
    legajo = values[0]
    if not messagebox.askyesno('Confirmar', f'¿Eliminar legajo {legajo}? Esta acción no se puede deshacer.'):
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM personal WHERE nro_legajo=%s', (legajo,))
        conn.commit()
        messagebox.showinfo('Eliminado', f'Legajo {legajo} eliminado.')
        refresh(state)
        clear_form(state)
    except Error as e:
        messagebox.showerror('DB Error', f'No se pudo eliminar.\n{e}')
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

def abrir_abm_personal(parent=None):
    if parent is None:
        root = tk.Tk()
        root.title('ABM Personal - Bomberos')
        root.state('zoomed')
        state = build_ui(root)
        refresh(state)
        root.mainloop()
    else:
        win = tk.Toplevel(parent)
        win.title('ABM Personal - Bomberos')
        win.geometry('1024x600')
        state = build_ui(win)
        refresh(state)
        win.transient(parent)
        win.grab_set()
        return win

# if __name__ == '__main__':
#     abrir_abm_personal()

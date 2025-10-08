import Asistencias_modelo as mod
import Asistencias_vista as vis

def Asistencias():
    global gui_Asistencias

    asistencias = mod.Asistencias().getAll()
    personal = mod.Personal().getAll()
    eventos = mod.Eventos().getAll()

    gui_Asistencias = vis.Asistencias(asistencias, personal, eventos)
    gui_Asistencias.attributes('-fullscreen', True)

    gui_Asistencias.button_salir.configure(command=lambda: [gui_Asistencias.destroy()])
    
    gui_Asistencias.mainloop()

if __name__ == '__main__':
    Asistencias()
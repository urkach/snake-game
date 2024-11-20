from tkinter import *
from modo_obstaculos import gameLoop

def modos_de_juego():
    # Eliminar todos los widgets actuales
    for widget in window.winfo_children():
        widget.destroy()

    # Cambiar el título y agregar nuevos botones y etiquetas
    window.title("Modos de Juego")
    nuevo_label = Label(window, text="Selecciona un Modo de Juego")
    nuevo_label.config(font=("Verdana", 24))
    nuevo_label.pack()

    boton_modo1 = Button(text="Modo Clásico", height=10, width=20)
    boton_modo1.place(relx=0.5, rely=0.5, anchor='center')

    boton_modo2 = Button(text="Modo obstaculos", height=10, width=20, command=gameLoop)
    boton_modo2.place(relx=0.5, rely=0.25, anchor='center')

    boton_multijugador = Button(text="MULTIJUGADOR", height=10, width=20)
    boton_multijugador.place(relx=0.5, rely=0.75, anchor='center')

    # Botón "ATRÁS" en la esquina inferior derecha
    boton_atras = Button(text="ATRÁS", height=3, width=10, command=pantalla_inicio)
    boton_atras.place(relx=0.1, rely=0.9, anchor='se')


def pantalla_inicio():
    # Eliminar todos los widgets actuales
    for widget in window.winfo_children():
        widget.destroy()

    # Configurar la pantalla inicial
    window.title("Juego de la serpiente")
    label = Label(window, text="¡Juego de la serpiente!")
    label.config(font=("Verdana", 24))
    label.pack()

    botonplay = Button(text="PLAY", height=10, width=20, command=modos_de_juego)
    botonplay.place(relx=0.5, rely=0.5, anchor='center')

    botontienda = Button(text="TIENDA", height=10, width=20)
    botontienda.place(relx=0.5, rely=0.25, anchor='center')

    botonconfig = Button(text="CONFIGURACIÓN", height=10, width=20)
    botonconfig.place(relx=0.5, rely=0.75, anchor='center')


# Configuración inicial de la ventana
BACKGROUND_COLOR = "#ffffff"
window = Tk()
window.title("Juego de la serpiente")

width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))

pantalla_inicio()

window.mainloop()

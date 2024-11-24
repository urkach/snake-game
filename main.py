from tkinter import *
from modos.modo_obstaculos import gameLoop as gameLoopObstaculos
from modos.modo_obstaculos_multi import gameLoop as gameLoopObstaculosMulti
from modos.modo_clasico import gameLoop as gameLoopClasico
from modos.modo_clasico_multi import gameLoop as gameLoopClasicoMulti
from modos.modo_extremo import gameLoop as gameLoopExtremo
from modos.modo_extremo_multi import gameLoop as gameLoopExtremoMulti


def seleccionar_tipo_juego(normal_mode, multi_mode):
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Seleccionar Tipo de Juego")
    nuevo_label = Label(window, text="¿Quieres jugar en modo Normal o Multijugador?")
    nuevo_label.config(font=("Verdana", 20))
    nuevo_label.pack(pady=40)

    boton_normal = Button(window, text="Normal", height=5, width=20, command=lambda: iniciar_juego(normal_mode))
    boton_normal.pack(pady=10)

    boton_multijugador = Button(window, text="Multijugador", height=5, width=20, command=lambda: iniciar_juego(multi_mode))
    boton_multijugador.pack(pady=10)

    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=modos_de_juego)
    boton_atras.pack(pady=20)

def iniciar_juego(modo_juego):
    window.withdraw()
    modo_juego(window)

def obstaculos():
    seleccionar_tipo_juego(gameLoopObstaculos, gameLoopObstaculosMulti)

def clasico():
    seleccionar_tipo_juego(gameLoopClasico, gameLoopClasicoMulti)

def extremo():
    seleccionar_tipo_juego(gameLoopExtremo, gameLoopExtremoMulti)

def modos_de_juego():
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Modos de Juego")
    nuevo_label = Label(window, text="Selecciona un Modo de Juego")
    nuevo_label.config(font=("Verdana", 24))
    nuevo_label.pack()

    boton_modo1 = Button(window, text="Modo Clásico", height=10, width=20, command=clasico)
    boton_modo1.place(relx=0.5, rely=0.25, anchor='center')

    boton_modo2 = Button(window, text="Modo Obstáculos", height=10, width=20, command=obstaculos)
    boton_modo2.place(relx=0.5, rely=0.5, anchor='center')

    boton_modo3 = Button(window, text="Modo Extremo", height=10, width=20, command=extremo)
    boton_modo3.place(relx=0.5, rely=0.75, anchor='center')

    boton_atras = Button(window, text="ATRÁS", height=3, width=10, command=pantalla_inicio)
    boton_atras.place(relx=0.1, rely=0.9, anchor='se')

def pantalla_inicio():
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Juego de la serpiente")
    label = Label(window, text="¡Juego de la serpiente!")
    label.config(font=("Verdana", 24))
    label.pack()

    botonplay = Button(window, text="JUGAR", height=10, width=20, command=modos_de_juego)
    botonplay.place(relx=0.5, rely=0.5, anchor='center')

    botontienda = Button(window, text="TIENDA", height=10, width=20)
    botontienda.place(relx=0.5, rely=0.25, anchor='center')

    botonconfig = Button(window, text="CONFIGURACIÓN", height=10, width=20)
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

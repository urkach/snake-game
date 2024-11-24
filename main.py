from tkinter import *
from modos.modo_obstaculos import gameLoop as gameLoopObstaculos
from modos.modo_obstaculos_multi import gameLoop as gameLoopObstaculosMulti
from modos.modo_clasico import gameLoop as gameLoopClasico
from modos.modo_clasico_multi import gameLoop as gameLoopClasicoMulti
from modos.modo_extremo import gameLoop as gameLoopExtremo
from modos.modo_extremo_multi import gameLoop as gameLoopExtremoMulti

def on_enter(event):
    event.widget.config(bg="#6c777e", fg="white")

def on_leave(event):
    event.widget.config(bg="#343030", fg="white")

def seleccionar_tipo_juego(normal_mode, multi_mode):
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Seleccionar Tipo de Juego")
    nuevo_label = Label(window, text="¿Quieres jugar en modo Solitario o Multijugador?")
    nuevo_label.config(font=("Verdana", 20), fg="white", bg="#343030")
    nuevo_label.pack(pady=40)

    boton_normal = Button(window, text="Solitario", height=10, width=20, command=lambda: iniciar_juego(normal_mode),
                          bg="#343030", fg="white", font=("Verdana", 14))
    boton_normal.pack(pady=10)
    boton_normal.bind("<Enter>", on_enter)
    boton_normal.bind("<Leave>", on_leave)

    boton_multijugador = Button(window, text="Multijugador", height=10, width=20, command=lambda: iniciar_juego(multi_mode),
                                bg="#343030", fg="white", font=("Verdana", 14))
    boton_multijugador.pack(pady=10)
    boton_multijugador.bind("<Enter>", on_enter)
    boton_multijugador.bind("<Leave>", on_leave)

    boton_atras = Button(window, text="ATRÁS", height=10, width=20, command=modos_de_juego,
                         bg="#343030", fg="white", font=("Verdana", 14))
    boton_atras.pack(pady=20)
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)

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
    nuevo_label.config(font=("Verdana", 24), fg="white", bg="#343030")
    nuevo_label.pack()

    boton_modo1 = Button(window, text="Modo Clásico", height=10, width=20, command=clasico,
                         bg="#343030", fg="white", font=("Verdana", 14))
    boton_modo1.place(relx=0.5, rely=0.25, anchor='center')
    boton_modo1.bind("<Enter>", on_enter)
    boton_modo1.bind("<Leave>", on_leave)

    boton_modo2 = Button(window, text="Modo Obstáculos", height=10, width=20, command=obstaculos,
                         bg="#343030", fg="white", font=("Verdana", 14))
    boton_modo2.place(relx=0.5, rely=0.5, anchor='center')
    boton_modo2.bind("<Enter>", on_enter)
    boton_modo2.bind("<Leave>", on_leave)

    boton_modo3 = Button(window, text="Modo Extremo", height=10, width=20, command=extremo,
                         bg="#343030", fg="white", font=("Verdana", 14))
    boton_modo3.place(relx=0.5, rely=0.75, anchor='center')
    boton_modo3.bind("<Enter>", on_enter)
    boton_modo3.bind("<Leave>", on_leave)

    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=pantalla_inicio,
                         bg="#343030", fg="white", font=("Verdana", 14))
    boton_atras.place(relx=0.1, rely=0.9, anchor='se')
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)

def pantalla_inicio():
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Juego de la serpiente")
    
    label = Label(window, text="¡Juego de la serpiente!", font=("Verdana", 24), fg="white", bg="#343030")
    label.pack()

    botonplay = Button(window, text="JUGAR", height=10, width=20, command=modos_de_juego,
                       bg="#343030", fg="white", font=("Verdana", 14))
    botonplay.place(relx=0.5, rely=0.5, anchor='center')
    botonplay.bind("<Enter>", on_enter)
    botonplay.bind("<Leave>", on_leave)

    botontienda = Button(window, text="TIENDA", height=10, width=20, bg="#343030", fg="white", font=("Verdana", 14))
    botontienda.place(relx=0.5, rely=0.25, anchor='center')
    botontienda.bind("<Enter>", on_enter)
    botontienda.bind("<Leave>", on_leave)

    botonconfig = Button(window, text="CONFIGURACIÓN", height=10, width=20, bg="#343030", fg="white", font=("Verdana", 14))
    botonconfig.place(relx=0.5, rely=0.75, anchor='center')
    botonconfig.bind("<Enter>", on_enter)
    botonconfig.bind("<Leave>", on_leave)

BACKGROUND_COLOR = "#212121"
window = Tk()
window.title("Juego de la serpiente")

width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))
window.config(bg=BACKGROUND_COLOR)

window.iconbitmap('logo.ico')

pantalla_inicio()

window.mainloop()

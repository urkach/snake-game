from tkinter import *
from tkinter import font, messagebox
import pygame
from modos.modo_obstaculos import gameLoop as gameLoopObstaculos
from modos.modo_obstaculos_multi import gameLoop as gameLoopObstaculosMulti
from modos.modo_clasico import gameLoop as gameLoopClasico
from modos.modo_clasico_multi import gameLoop as gameLoopClasicoMulti
from modos.modo_caos import gameLoop as gameLoopExtremo
from modos.modo_caos_multi import gameLoop as gameLoopExtremoMulti

def on_enter(event):
    event.widget.config(bg="#6c777e", fg="white")

def on_leave(event):
    event.widget.config(bg="#343030", fg="white")

def play():
    pygame.mixer.music.load('Audio\cyberpunk_audio.mp3')
    pygame.mixer.music.play(loops=-1)

def stop():
    pygame.mixer.music.stop()

def set_volume(volume):
    pygame.mixer.music.set_volume(float(volume) / 100)

def toggle_mute():
    global is_muted
    if is_muted:
        pygame.mixer.music.set_volume(current_volume)
        mute_button.config(text="MUTE")
    else:
        pygame.mixer.music.set_volume(0)
        mute_button.config(text="UNMUTE")
    is_muted = not is_muted

def mostrar_copyright():
    messagebox.showinfo("Copyright", "Música: Cyberpunk Audio\nAutor: Karl Casey @ White Bat Audio\nLicencia: Usada con permiso del autor.")

def configuracion():
    global mute_button, current_volume, is_muted

    for widget in window.winfo_children():
        widget.destroy()

    is_muted = False
    current_volume = pygame.mixer.music.get_volume()

    window.title("Configuración")
    label = Label(window, text="CONFIGURACIÓN", font=("Press Start 2P", 30), fg="white", bg="#343030")
    label.pack(pady=40)

    volume_label = Label(window, text="Volumen de la Música", font=("Press Start 2P", 14), fg="white", bg="#343030")
    volume_label.pack(pady=10)

    volume_slider = Scale(window, from_=0, to=100, orient=HORIZONTAL, command=set_volume, bg="#343030", fg="white",
                          font=("Press Start 2P", 12), length=300)
    volume_slider.set(pygame.mixer.music.get_volume() * 100)
    volume_slider.pack(pady=10)

    mute_button = Button(window, text="MUTE", command=toggle_mute, height=2, width=10, bg="#343030", fg="white",
                         font=("Press Start 2P", 12))
    mute_button.pack(pady=20)

    copyright_button = Button(window, text="Copyright", command=mostrar_copyright, height=2, width=15,
                              bg="#343030", fg="white", font=("Press Start 2P", 12))
    copyright_button.pack(pady=10)

    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=pantalla_inicio, bg="#343030", fg="white",
                         font=("Press Start 2P", 14))
    boton_atras.pack(pady=20)
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)

def seleccionar_tipo_juego(normal_mode, multi_mode):
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Seleccionar Tipo de Juego")
    nuevo_label = Label(window, text="¿SOLO / MULTIJUGADOR?")
    nuevo_label.config(font=("Press Start 2P", 30), fg="white", bg="#343030")
    nuevo_label.pack(pady=40)

    boton_normal = Button(window, text="SOLO", height=10, width=20, command=lambda: iniciar_juego(normal_mode),
                          bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_normal.pack(pady=10)
    boton_normal.bind("<Enter>", on_enter)
    boton_normal.bind("<Leave>", on_leave)

    boton_multijugador = Button(window, text="MULTIJUGADOR", height=10, width=20, command=lambda: iniciar_juego(multi_mode),
                                bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_multijugador.pack(pady=10)
    boton_multijugador.bind("<Enter>", on_enter)
    boton_multijugador.bind("<Leave>", on_leave)

    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=modos_de_juego,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_atras.place(relx=0.1, rely=0.9, anchor='center')
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)

def iniciar_juego(modo_juego):
    play()  # Reproduce la música cuando comienza el juego
    window.withdraw()
    modo_juego(window)
    pygame.mixer.music.stop()  # Detener la música al salir del juego

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
    nuevo_label = Label(window, text="MODO JUEGO")
    nuevo_label.config(font=("Press Start 2P", 30), fg="white", bg="#343030")
    nuevo_label.pack()

    boton_modo1 = Button(window, text="CLASSIC", height=10, width=20, command=clasico,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_modo1.place(relx=0.5, rely=0.25, anchor='center')
    boton_modo1.bind("<Enter>", on_enter)
    boton_modo1.bind("<Leave>", on_leave)

    boton_modo2 = Button(window, text="OBSTACULOS", height=10, width=20, command=obstaculos,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_modo2.place(relx=0.5, rely=0.5, anchor='center')
    boton_modo2.bind("<Enter>", on_enter)
    boton_modo2.bind("<Leave>", on_leave)

    boton_modo3 = Button(window, text="CAOS", height=10, width=20, command=extremo,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_modo3.place(relx=0.5, rely=0.75, anchor='center')
    boton_modo3.bind("<Enter>", on_enter)
    boton_modo3.bind("<Leave>", on_leave)

    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=pantalla_inicio,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_atras.place(relx=0.1, rely=0.9, anchor='center')
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)

def pantalla_inicio():
    for widget in window.winfo_children():
        widget.destroy()

    window.title("SNAKE GAME")
    
    label = Label(window, text="SNAKE GAME", font=("Press Start 2P", 40), fg="white", bg="#343030")
    label.pack()

    botonplay = Button(window, text="JUGAR", height=10, width=20, command=modos_de_juego,
                       bg="#343030", fg="white", font=("Press Start 2P", 12))
    botonplay.place(relx=0.5, rely=0.5, anchor='center')
    botonplay.bind("<Enter>", on_enter)
    botonplay.bind("<Leave>", on_leave)

    botontienda = Button(window, text="TIENDA", height=10, width=20, bg="#343030", fg="white", font=("Press Start 2P", 12))
    botontienda.place(relx=0.5, rely=0.25, anchor='center')
    botontienda.bind("<Enter>", on_enter)
    botontienda.bind("<Leave>", on_leave)

    botonconfig = Button(window, text="CONFIGURACIÓN", height=10, width=20, command=configuracion,
                         bg="#343030", fg="white", font=("Press Start 2P", 12))
    botonconfig.place(relx=0.5, rely=0.75, anchor='center')
    botonconfig.bind("<Enter>", on_enter)
    botonconfig.bind("<Leave>", on_leave)

window = Tk()
window.title("Juego de la serpiente")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f"{width}x{height}")
pygame.mixer.init()

pantalla_inicio()
window.mainloop()

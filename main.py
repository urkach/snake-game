from tkinter import *
from tkinter import font, messagebox
import pygame
from modos.modo_obstaculos import gameLoop as gameLoopObstaculos
from modos.modo_obstaculos_multi import gameLoop as gameLoopObstaculosMulti
from modos.modo_clasico import gameLoop as gameLoopClasico
from modos.modo_clasico_multi import gameLoop as gameLoopClasicoMulti
from modos.modo_caos import gameLoop as gameLoopExtremo
from modos.modo_caos_multi import gameLoop as gameLoopExtremoMulti
from tkinter import messagebox
from PIL import Image, ImageTk

monedas = 0 
skins = ["chill snake", "blue wise snake", "red dead snake"]
imagenes_skins=["skins_images/yellow.png", "skins_images/blue.png", "skins_images/red.png"]
precios_skins = [10, 15, 15] 
colores_skins=["yellow","blue","red"]
skin_actual = "green"
BACKGROUND_COLOR="#212121"
skins_compradas=[]

def cargar_monedas(): 
    global monedas 
    try: 
        with open("monedas.txt", "r") as file: 
            monedas = int(file.read()) 

    except FileNotFoundError: 
        monedas = 0 

def guardar_monedas(): 
    with open("monedas.txt", "w") as file: 
        file.write(str(monedas))

def cargar_skins_compradas():
    global skins_compradas
    try:
        with open("skins_compradas.txt", "r") as file:
            skins_compradas = file.read().splitlines()
    except FileNotFoundError:
        skins_compradas = []

def guardar_skins_compradas():
    with open("skins_compradas.txt", "w") as file:
        file.write("\n".join(skins_compradas))

def on_enter(event):
    event.widget.config(bg="#6c777e", fg="white")

def on_leave(event):
    event.widget.config(bg="#343030", fg="white")

def actualizar_monedas():
    global label_monedas, label_monedas_tienda
    cargar_monedas()
    if 'label_monedas' in globals():
        label_monedas.config(text=f"Monedas: {monedas}")
    if 'label_monedas_tienda' in globals():
        label_monedas_tienda.config(text=f"Monedas: {monedas}")
    window.after(500,actualizar_monedas)

def comprar_skin(skin, precio,color): 
            global monedas, skin_actual
            cargar_monedas()
            cargar_skins_compradas()
            
            if skin in skins_compradas:
                messagebox.showinfo("Ya comprada", f"Ya tienes la skin {skin}.")
                return
            if monedas >= precio: 
                monedas -= precio
                skins_compradas.append(skin)
                skin_actual = color
                guardar_monedas()
                guardar_skins_compradas()
                actualizar_monedas()
                messagebox.showinfo("Compra Exitosa", f"Has comprado la skin {skin}!")
                tienda()
            else:
                messagebox.showinfo("Monedas Insuficientes", "No tienes suficientes monedas.") 

def play():
    if not pygame.mixer.get_init():
        pygame.mixer.init()  # Re-inicializa el mixer si no está inicializado
    pygame.mixer.music.load('Audio/cyberpunk_audio.mp3')
    pygame.mixer.music.play(loops=-1)

def stop():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()


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
    nuevo_label = Label(window, text="¿SOLO / MULTIJUGADOR?", font=("Press Start 2P", 30), fg="white", bg="#343030")
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

def tienda():
    global label_monedas_tienda
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Tienda de Skins")

    label_tienda = Label(window, text="Tienda de Skins", font=("Verdana", 24), fg="white", bg="#343030")
    label_tienda.pack(pady=20)

    label_monedas_tienda=Label(window,text=f"monedas: {monedas}", font=("verdana", 14),fg="white",bg="#343030")
    label_monedas_tienda.pack(pady=10)

    contenedor_skins = Frame(window, bg=BACKGROUND_COLOR)
    contenedor_skins.pack(pady=20)

    imagenes_tk = []  # Lista para las imágenes
    for i in range(3):
        frame_skin = Frame(contenedor_skins, bg="#212121", bd=2, relief="solid", width=400, height=800)
        frame_skin.pack_propagate(False)
        frame_skin.grid(row=0, column=i, padx=30, pady=(3, 20))

        label_skin = Label(frame_skin, text=skins[i], bg="#212121", fg="white", font=("Verdana", 14))
        label_skin.pack(pady=5)

        try:
            imagen_skin = Image.open(imagenes_skins[i])
            imagen_skin = imagen_skin.resize((400, 500), Image.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen_skin)

            label_imagen = Label(frame_skin, image=imagen_tk, bg="#212121")
            label_imagen.image = imagen_tk  # Mantener la referencia de la imagen
            label_imagen.pack(pady=10)

            imagenes_tk.append(imagen_tk)
        except Exception as e:
            label_error = Label(frame_skin, text=f"Error loading image: {e}", bg="#212121", fg="red", font=("Verdana", 10))
            label_error.pack(pady=10)

        if skins[i] in skins_compradas:
            boton_skin = Button(frame_skin, text="Comprada", state=DISABLED, bg="#343030", fg="white", font=("Verdana", 12), height=2, width=20)
            boton_skin.pack(pady=10)

            boton_equipar = Button(frame_skin, text=f"Equipar {skins[i]}",
                                   command=lambda color=colores_skins[i]: equipar_skin(color),
                                   bg="#343030", fg="white", font=("Verdana", 12), height=2, width=20)
            boton_equipar.pack(pady=10)
        else: 
            boton_skin = Button(frame_skin, text=f"Comprar {precios_skins[i]} monedas",
                                  command=lambda s=skins[i], precio=precios_skins[i], color=colores_skins[i]: comprar_skin(s, precio, color),
                                  bg="#343030", fg="white", font=("Verdana", 12), height=2, width=20)
            boton_skin.pack(pady=10) 
            
    boton_atras = Button(window, text="ATRÁS", command=pantalla_inicio, bg="#343030", fg="white", font=("Verdana", 14))
    boton_atras.pack(pady=20)
    actualizar_monedas()

def comprar_y_actualizar(skin,precio, color):
    comprar_skin(skin, precio, color)
    tienda()
def equipar_skin(color):
    global skin_actual
    skin_actual = color
    guardar_skin_actual()
    messagebox.showinfo("Skin equipada", f"¡Has equipado la skin {color}!")
    tienda()

def guardar_skin_actual():
    with open("skin_actual.txt", "w") as file:
        file.write(skin_actual)

def cargar_skin_actual():
    global skin_actual
    try:
        with open("skin_actual.txt", "r") as file:
            skin_actual = file.read().strip()
    except FileNotFoundError:
        skin_actual = "green" 


def modos_de_juego():
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Modos de Juego")
    nuevo_label = Label(window, text="MODO JUEGO", font=("Press Start 2P", 30), fg="white", bg="#343030")
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
    window.config(bg="#343030")

    label = Label(window, text="SNAKE GAME", font=("Press Start 2P", 40), fg="white", bg="#343030")
    label.pack()

    global label_monedas
    label_monedas = Label(window, text=f"Monedas: {monedas}", font=("Verdana", 14), fg="white", bg="#343030")
    label_monedas.pack(pady=10) 
    actualizar_monedas()

    botonplay = Button(window, text="JUGAR", height=10, width=20, command=modos_de_juego,
                       bg="#343030", fg="white", font=("Press Start 2P", 12))
    botonplay.place(relx=0.5, rely=0.5, anchor='center')
    botonplay.bind("<Enter>", on_enter)
    botonplay.bind("<Leave>", on_leave)

    botontienda = Button(window, text="TIENDA", height=10, width=20, command=tienda, bg="#343030", fg="white", font=("Press Start 2P", 12))
    botontienda.place(relx=0.5, rely=0.25, anchor='center')
    botontienda.bind("<Enter>", on_enter)
    botontienda.bind("<Leave>", on_leave)

    botonconfig = Button(window, text="CONFIGURACIÓN", height=10, width=20, command=configuracion,
                         bg="#343030", fg="white", font=("Press Start 2P", 12))
    botonconfig.place(relx=0.5, rely=0.75, anchor='center')
    botonconfig.bind("<Enter>", on_enter)
    botonconfig.bind("<Leave>", on_leave)

def comer_fruta():
    global monedas
    monedas +=1
    guardar_monedas()
    actualizar_monedas()

def dibujar_serpiente(canvas, snake):
    canvas.delete("all") 
    for segment in snake:
        canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill=skin_actual)
BACKGROUND_COLOR = "#212121"


window = Tk()
window.title("Juego de la serpiente")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f"{width}x{height}")
window.resizable(False,False)
pygame.mixer.init()


cargar_monedas()
cargar_skins_compradas()
cargar_skin_actual()
pantalla_inicio()
window.mainloop()

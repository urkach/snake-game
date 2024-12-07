# Importa las librerías necesarias para la interfaz gráfica (Tkinter) y otras funcionalidades
from tkinter import *
from tkinter import font, messagebox  # Para fuentes y cuadros de diálogo
import pygame  # Para manejar audio
from modos.modo_obstaculos import gameLoop as gameLoopObstaculos  # Importa el bucle principal del modo Obstáculos
from modos.modo_obstaculos_multi import gameLoop as gameLoopObstaculosMulti  # Modo multijugador Obstáculos
from modos.modo_clasico import gameLoop as gameLoopClasico  # Bucle principal del modo clásico
from modos.modo_clasico_multi import gameLoop as gameLoopClasicoMulti  # Modo multijugador clásico
from modos.modo_caos import gameLoop as gameLoopExtremo  # Bucle principal del modo Extremo
from modos.modo_caos_multi import gameLoop as gameLoopExtremoMulti  # Modo multijugador Extremo
from tkinter import messagebox  # Para cuadros de mensajes
from PIL import Image, ImageTk  # Para cargar y manejar imágenes

# Variables globales
monedas = 0  # Contador de monedas del jugador
label_monedas = None  # Referencia a un widget para mostrar monedas en pantalla principal
label_monedas_tienda = None  # Referencia a un widget para mostrar monedas en la tienda
skins = ["chill snake", "blue wise snake", "red dead snake"]  # Nombres de las skins disponibles
imagenes_skins = ["skins_images/yellow.png", "skins_images/blue.png", "skins_images/red.png"]  # Rutas de las imágenes de las skins
precios_skins = [10, 15, 20]  # Precios de las skins
colores_skins = ["yellow", "blue", "red"]  # Colores asociados a las skins
skin_actual = "green"  # Color predeterminado de la serpiente
BACKGROUND_COLOR = "#212121"  # Color de fondo
skins_compradas = []  # Lista de skins que el jugador ha comprado

# Función para cargar monedas desde un archivo
def cargar_monedas(): 
    global monedas 
    try: 
        with open("monedas.txt", "r") as file: 
            monedas = int(file.read())  # Lee y convierte las monedas a entero
    except FileNotFoundError: 
        monedas = 0  # Si no se encuentra el archivo, asigna 0 monedas

# Función para guardar monedas en un archivo
def guardar_monedas(): 
    with open("monedas.txt", "w") as file: 
        file.write(str(monedas))  # Guarda la cantidad actual de monedas

# Función para cargar las skins compradas desde un archivo
def cargar_skins_compradas():
    global skins_compradas
    try:
        with open("skins_compradas.txt", "r") as file:
            skins_compradas = file.read().splitlines()  # Carga las skins como una lista de líneas
    except FileNotFoundError:
        skins_compradas = []  # Si no se encuentra el archivo, inicia una lista vacía

# Función para guardar las skins compradas en un archivo
def guardar_skins_compradas():
    with open("skins_compradas.txt", "w") as file:
        file.write("\n".join(skins_compradas))  # Guarda la lista de skins como texto separado por líneas

# Cambia el color de fondo y texto de un widget al pasar el mouse
def on_enter(event):
    event.widget.config(bg="#6c777e", fg="white")

# Restaura el color original de un widget al salir el mouse
def on_leave(event):
    event.widget.config(bg="#343030", fg="white")

# Actualiza el contador de monedas mostrado en la interfaz
def actualizar_monedas():
    global label_monedas, label_monedas_tienda 
    cargar_monedas()  # Carga las monedas actuales
    try: 
        if label_monedas and label_monedas.winfo_exists(): 
            label_monedas.config(text=f"Monedas: {monedas}")  # Actualiza en pantalla principal
    except TclError: 
        print("label_monedas no existe.") 
    
    try: 
        if label_monedas_tienda and label_monedas_tienda.winfo_exists(): 
            label_monedas_tienda.config(text=f"Monedas: {monedas}")  # Actualiza en tienda
    except TclError: 
        print("label_monedas_tienda no existe.") 
    window.after(500, actualizar_monedas)  # Configura actualización periódica

# Función para comprar una skin
def comprar_skin(skin, precio, color): 
    global monedas, skin_actual
    cargar_monedas()  # Asegura que se tengan las monedas actualizadas
    cargar_skins_compradas()  # Carga las skins previamente compradas
    
    if skin in skins_compradas:  # Si ya se tiene la skin
        messagebox.showinfo("Ya comprada", f"Ya tienes la skin {skin}.")
        return
    if monedas >= precio:  # Si tiene suficientes monedas
        monedas -= precio  # Descuenta el precio
        skins_compradas.append(skin)  # Añade la skin a las compradas
        skin_actual = color  # Cambia a la skin comprada
        guardar_monedas()  # Guarda el nuevo total de monedas
        guardar_skins_compradas()  # Guarda la lista actualizada de skins
        actualizar_monedas()  # Refleja los cambios en la interfaz
        messagebox.showinfo("Compra Exitosa", f"Has comprado la skin {skin}!")
        tienda()  # Actualiza la tienda
    else:
        messagebox.showinfo("Monedas Insuficientes", "No tienes suficientes monedas.")  # Mensaje si faltan monedas

def play():
    # Verifica si el mixer de Pygame no está inicializado, y si es así, lo inicializa
    if not pygame.mixer.get_init():
        pygame.mixer.init()  # Re-inicializa el mixer si no está inicializado
    # Carga el archivo de audio especificado en el mixer de Pygame
    pygame.mixer.music.load('Audio/cyberpunk_audio.mp3')
    # Reproduce la música en un bucle infinito (-1 significa bucle infinito)
    pygame.mixer.music.play(loops=-1)

def stop():
    # Verifica si el mixer de Pygame está inicializado
    if pygame.mixer.get_init():
        # Detiene la música actual que está sonando
        pygame.mixer.music.stop()
        # Finaliza la sesión del mixer de Pygame
        pygame.mixer.quit()

def set_volume(volume):
    # Establece el volumen de la música, normalizando el valor recibido (0-100) a un rango (0.0-1.0)
    pygame.mixer.music.set_volume(float(volume) / 100)

def toggle_mute():
    global is_muted  # Se declara la variable global is_muted para poder modificarla
    if is_muted:
        # Si está silenciado, se restablece el volumen a su valor anterior
        pygame.mixer.music.set_volume(current_volume)
        # Cambia el texto del botón a "MUTE"
        mute_button.config(text="MUTE")
    else:
        # Si no está silenciado, establece el volumen a 0 (silencio)
        pygame.mixer.music.set_volume(0)
        # Cambia el texto del botón a "UNMUTE"
        mute_button.config(text="UNMUTE")
    # Alterna el estado de silenciado
    is_muted = not is_muted

def mostrar_copyright():
    # Muestra una ventana emergente con la información de copyright
    messagebox.showinfo("Copyright", "Música: Cyberpunk Audio\nAutor: Karl Casey @ White Bat Audio\nLicencia: Usada con permiso del autor.")

def configuracion():
    global mute_button, current_volume, is_muted  # Se declaran variables globales para su uso en otras funciones

    # Elimina todos los widgets de la ventana antes de agregar los nuevos
    for widget in window.winfo_children():
        widget.destroy()

    is_muted = False  # Inicializa el estado de "no silenciado"
    current_volume = pygame.mixer.music.get_volume()  # Obtiene el volumen actual de la música

    window.title("Configuración")  # Cambia el título de la ventana
    # Crea un Label para mostrar el título "CONFIGURACIÓN"
    label = Label(window, text="CONFIGURACIÓN", font=("Press Start 2P", 30), fg="white", bg="#343030")
    label.pack(pady=40)

    # Crea un Label para la opción "Volumen de la Música"
    volume_label = Label(window, text="Volumen de la Música", font=("Press Start 2P", 14), fg="white", bg="#343030")
    volume_label.pack(pady=10)

    # Crea un control deslizante para ajustar el volumen, con valores de 0 a 100
    volume_slider = Scale(window, from_=0, to=100, orient=HORIZONTAL, command=set_volume, bg="#343030", fg="white",
                          font=("Press Start 2P", 12), length=300)
    volume_slider.set(pygame.mixer.music.get_volume() * 100)  # Establece el valor inicial del slider según el volumen actual
    volume_slider.pack(pady=10)

    # Crea un botón para alternar entre mute y no mute
    mute_button = Button(window, text="MUTE", command=toggle_mute, height=2, width=10, bg="#343030", fg="white",
                         font=("Press Start 2P", 12))
    mute_button.pack(pady=20)

    # Crea un botón para mostrar la información de copyright
    copyright_button = Button(window, text="Copyright", command=mostrar_copyright, height=2, width=15,
                              bg="#343030", fg="white", font=("Press Start 2P", 12))
    copyright_button.pack(pady=10)

    # Crea un botón para regresar a la pantalla de inicio
    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=pantalla_inicio, bg="#343030", fg="white",
                         font=("Press Start 2P", 14))
    boton_atras.pack(pady=20)
    # Agrega un efecto visual al pasar el mouse por encima del botón
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)


def seleccionar_tipo_juego(normal_mode, multi_mode):
    # Elimina todos los widgets de la ventana actual antes de cargar la nueva interfaz
    for widget in window.winfo_children():
        widget.destroy()

    # Cambia el título de la ventana
    window.title("Seleccionar Tipo de Juego")
    
    # Crea un Label para preguntar si el juego será en modo solo o multijugador
    nuevo_label = Label(window, text="¿SOLO / MULTIJUGADOR?", font=("Press Start 2P", 30), fg="white", bg="#343030")
    nuevo_label.config(font=("Press Start 2P", 30), fg="white", bg="#343030")
    nuevo_label.pack(pady=40)

    # Crea un botón para seleccionar el modo de juego solo (normal)
    boton_normal = Button(window, text="SOLO", height=10, width=20, command=lambda: iniciar_juego(normal_mode),
                          bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_normal.pack(pady=10)
    # Añade efectos visuales cuando el ratón entra o sale del botón
    boton_normal.bind("<Enter>", on_enter)
    boton_normal.bind("<Leave>", on_leave)

    # Crea un botón para seleccionar el modo de juego multijugador
    boton_multijugador = Button(window, text="MULTIJUGADOR", height=10, width=20, command=lambda: iniciar_juego(multi_mode),
                                bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_multijugador.pack(pady=10)
    # Añade efectos visuales cuando el ratón entra o sale del botón
    boton_multijugador.bind("<Enter>", on_enter)
    boton_multijugador.bind("<Leave>", on_leave)

    # Crea un botón de regreso que lleva a la pantalla anterior
    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=modos_de_juego,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    # Coloca el botón en una posición relativa en la ventana
    boton_atras.place(relx=0.1, rely=0.9, anchor='center')
    # Añade efectos visuales cuando el ratón entra o sale del botón
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)

def iniciar_juego(modo_juego):
    # Reproduce la música al comenzar el juego
    play()
    # Oculta la ventana actual (la de selección de juego)
    window.withdraw()
    # Llama a la función correspondiente para iniciar el juego según el modo seleccionado
    modo_juego(window)
    # Detiene la música al salir del juego
    pygame.mixer.music.stop()

def obstaculos():
    # Llama a la función seleccionar_tipo_juego con los modos de juego correspondientes para obstáculos
    seleccionar_tipo_juego(gameLoopObstaculos, gameLoopObstaculosMulti)

def clasico():
    # Llama a la función seleccionar_tipo_juego con los modos de juego correspondientes para clásico
    seleccionar_tipo_juego(gameLoopClasico, gameLoopClasicoMulti)

def extremo():
    # Llama a la función seleccionar_tipo_juego con los modos de juego correspondientes para extremo
    seleccionar_tipo_juego(gameLoopExtremo, gameLoopExtremoMulti)

def tienda():
    global label_monedas_tienda  # Se declara una variable global para la etiqueta de las monedas

    # Elimina todos los widgets de la ventana antes de cargar la nueva interfaz
    for widget in window.winfo_children():
        widget.destroy()

    # Cambia el título de la ventana
    window.title("Tienda de Skins")

    # Crea un Label que muestra el título de la tienda
    label_tienda = Label(window, text="Tienda de Skins", font=("Verdana", 24), fg="white", bg="#343030")
    label_tienda.pack(pady=20)

    # Muestra la cantidad actual de monedas en la tienda
    label_monedas_tienda = Label(window, text=f"monedas: {monedas}", font=("verdana", 14), fg="white", bg="#343030")
    label_monedas_tienda.pack(pady=10)

    # Crea un contenedor para los skins disponibles
    contenedor_skins = Frame(window, bg=BACKGROUND_COLOR)
    contenedor_skins.pack(pady=20)

    imagenes_tk = []  # Lista para almacenar las imágenes de los skins
    # Recorre los primeros 3 skins disponibles
    for i in range(3):
        # Crea un contenedor para cada skin
        frame_skin = Frame(contenedor_skins, bg="#212121", bd=2, relief="solid", width=400, height=800)
        frame_skin.pack_propagate(False)
        frame_skin.grid(row=0, column=i, padx=30, pady=(3, 20))

        # Crea una etiqueta para mostrar el nombre del skin
        label_skin = Label(frame_skin, text=skins[i], bg="#212121", fg="white", font=("Verdana", 14))
        label_skin.pack(pady=5)

        try:
            # Intenta cargar la imagen del skin
            imagen_skin = Image.open(imagenes_skins[i])
            imagen_skin = imagen_skin.resize((400, 500), Image.LANCZOS)  # Ajusta el tamaño de la imagen
            imagen_tk = ImageTk.PhotoImage(imagen_skin)  # Convierte la imagen a un formato compatible con Tkinter

            # Crea una etiqueta para mostrar la imagen del skin
            label_imagen = Label(frame_skin, image=imagen_tk, bg="#212121")
            label_imagen.image = imagen_tk  # Mantiene una referencia a la imagen
            label_imagen.pack(pady=10)

            # Añade la imagen a la lista para evitar que sea eliminada por el garbage collector
            imagenes_tk.append(imagen_tk)
        except Exception as e:
            # Si ocurre un error cargando la imagen, muestra un mensaje de error
            label_error = Label(frame_skin, text=f"Error loading image: {e}", bg="#212121", fg="red", font=("Verdana", 10))
            label_error.pack(pady=10)

        # Si el skin ya ha sido comprado, deshabilita el botón y agrega un botón para equipar
        if skins[i] in skins_compradas:
            boton_skin = Button(frame_skin, text="Comprada", state=DISABLED, bg="#343030", fg="white", font=("Verdana", 12), height=2, width=20)
            boton_skin.pack(pady=10)

            # Crea un botón para equipar el skin comprado
            boton_equipar = Button(frame_skin, text=f"Equipar {skins[i]}",
                                   command=lambda color=colores_skins[i]: equipar_skin(color),
                                   bg="#343030", fg="white", font=("Verdana", 12), height=2, width=20)
            boton_equipar.pack(pady=10)
        else: 
            # Si el skin no ha sido comprado, muestra el precio y un botón para comprarlo
            boton_skin = Button(frame_skin, text=f"Comprar {precios_skins[i]} monedas",
                                  command=lambda s=skins[i], precio=precios_skins[i], color=colores_skins[i]: comprar_skin(s, precio, color),
                                  bg="#343030", fg="white", font=("Verdana", 12), height=2, width=20)
            boton_skin.pack(pady=10)

    # Crea un botón de regreso que lleva a la pantalla principal
    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=pantalla_inicio, 
                        bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_atras.place(x=10, y=10)  # Coloca el botón en una posición específica de la ventana
    # Añade efectos visuales cuando el ratón entra o sale del botón
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)

    # Actualiza las monedas mostradas en la tienda
    actualizar_monedas()

def comprar_y_actualizar(skin, precio, color):
    # Llama a la función comprar_skin para realizar la compra del skin
    comprar_skin(skin, precio, color)
    # Llama a la función tienda para actualizar la tienda después de la compra
    tienda()

def equipar_skin(color):
    global skin_actual  # Utiliza la variable global skin_actual para cambiar el skin
    skin_actual = color  # Asigna el nuevo color de skin seleccionado
    guardar_skin_actual()  # Guarda el skin actual en un archivo
    # Muestra un mensaje indicando que el skin ha sido equipado
    messagebox.showinfo("Skin equipada", f"¡Has equipado la skin {color}!")
    # Llama a la función tienda para regresar a la pantalla de la tienda
    tienda()

def guardar_skin_actual():
    # Abre el archivo 'skin_actual.txt' en modo escritura para guardar el skin actual
    with open("skin_actual.txt", "w") as file:
        file.write(skin_actual)  # Escribe el color del skin actual en el archivo

def cargar_skin_actual():
    global skin_actual  # Utiliza la variable global skin_actual
    try:
        # Intenta abrir el archivo 'skin_actual.txt' para leer el skin guardado
        with open("skin_actual.txt", "r") as file:
            skin_actual = file.read().strip()  # Lee y elimina los espacios en blanco del skin guardado
    except FileNotFoundError:
        # Si el archivo no se encuentra, asigna un skin predeterminado (en este caso, "green")
        skin_actual = "green" 

def modos_de_juego():
    # Elimina todos los widgets de la ventana actual antes de cargar la nueva interfaz
    for widget in window.winfo_children():
        widget.destroy()

    # Cambia el título de la ventana
    window.title("Modos de Juego")
    
    # Crea un Label que muestra el título "MODO JUEGO"
    nuevo_label = Label(window, text="MODO JUEGO", font=("Press Start 2P", 30), fg="white", bg="#343030")
    nuevo_label.config(font=("Press Start 2P", 30), fg="white", bg="#343030")
    nuevo_label.pack()

    # Crea un botón para seleccionar el modo clásico
    boton_modo1 = Button(window, text="CLASSIC", height=10, width=20, command=clasico,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_modo1.place(relx=0.5, rely=0.25, anchor='center')
    # Añade efectos visuales cuando el ratón entra o sale del botón
    boton_modo1.bind("<Enter>", on_enter)
    boton_modo1.bind("<Leave>", on_leave)

    # Crea un botón para seleccionar el modo obstáculos
    boton_modo2 = Button(window, text="OBSTACULOS", height=10, width=20, command=obstaculos,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_modo2.place(relx=0.5, rely=0.5, anchor='center')
    # Añade efectos visuales cuando el ratón entra o sale del botón
    boton_modo2.bind("<Enter>", on_enter)
    boton_modo2.bind("<Leave>", on_leave)

    # Crea un botón para seleccionar el modo caos
    boton_modo3 = Button(window, text="CAOS", height=10, width=20, command=extremo,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_modo3.place(relx=0.5, rely=0.75, anchor='center')
    # Añade efectos visuales cuando el ratón entra o sale del botón
    boton_modo3.bind("<Enter>", on_enter)
    boton_modo3.bind("<Leave>", on_leave)

    # Crea un botón de regreso que lleva a la pantalla principal
    boton_atras = Button(window, text="ATRÁS", height=2, width=10, command=pantalla_inicio,
                         bg="#343030", fg="white", font=("Press Start 2P", 14))
    boton_atras.place(relx=0.1, rely=0.9, anchor='center')
    # Añade efectos visuales cuando el ratón entra o sale del botón
    boton_atras.bind("<Enter>", on_enter)
    boton_atras.bind("<Leave>", on_leave)

def pantalla_inicio():
    # Elimina todos los widgets de la ventana antes de cargar la nueva interfaz
    for widget in window.winfo_children():
        widget.destroy()

    # Cambia el título de la ventana
    window.title("SNAKE GAME")
    window.config(bg="#343030")

    # Crea un Label que muestra el título "SNAKE GAME"
    label = Label(window, text="SNAKE GAME", font=("Press Start 2P", 40), fg="white", bg="#343030")
    label.pack()

    global label_monedas  # Se declara una variable global para el label de monedas
    label_monedas = Label(window, text=f"Monedas: {monedas}", font=("Verdana", 14), fg="white", bg="#343030")
    label_monedas.pack(pady=10) 
    actualizar_monedas()  # Actualiza la cantidad de monedas mostradas

    # Crea un botón para iniciar el juego y mostrar los modos de juego
    botonplay = Button(window, text="JUGAR", height=10, width=20, command=modos_de_juego,
                       bg="#343030", fg="white", font=("Press Start 2P", 12))
    botonplay.place(relx=0.5, rely=0.5, anchor='center')
    # Añade efectos visuales cuando el ratón entra o sale del botón
    botonplay.bind("<Enter>", on_enter)
    botonplay.bind("<Leave>", on_leave)

    # Crea un botón para acceder a la tienda
    botontienda = Button(window, text="TIENDA", height=10, width=20, command=tienda, bg="#343030", fg="white", font=("Press Start 2P", 12))
    botontienda.place(relx=0.5, rely=0.25, anchor='center')
    # Añade efectos visuales cuando el ratón entra o sale del botón
    botontienda.bind("<Enter>", on_enter)
    botontienda.bind("<Leave>", on_leave)

    # Crea un botón para acceder a la configuración
    botonconfig = Button(window, text="CONFIGURACIÓN", height=10, width=20, command=configuracion,
                         bg="#343030", fg="white", font=("Press Start 2P", 12))
    botonconfig.place(relx=0.5, rely=0.75, anchor='center')
    # Añade efectos visuales cuando el ratón entra o sale del botón
    botonconfig.bind("<Enter>", on_enter)
    botonconfig.bind("<Leave>", on_leave)

def comer_fruta():
    global monedas  # Accede a la variable global de monedas
    monedas += 1  # Aumenta el contador de monedas
    guardar_monedas()  # Guarda el nuevo valor de monedas
    actualizar_monedas()  # Actualiza la visualización de monedas

def dibujar_serpiente(canvas, snake):
    canvas.delete("all")  # Elimina todos los elementos de la pantalla antes de redibujar
    # Dibuja cada segmento de la serpiente como un rectángulo en el canvas
    for segment in snake:
        canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill=skin_actual)  # Dibuja cada segmento con el color del skin actual

BACKGROUND_COLOR = "#212121"  # Define el color de fondo


# Crea la ventana principal del juego
window = Tk()
window.title("Juego de la serpiente")  # Establece el título de la ventana
width = window.winfo_screenwidth()  # Obtiene el ancho de la pantalla
height = window.winfo_screenheight()  # Obtiene la altura de la pantalla
window.geometry(f"{width}x{height}")  # Establece el tamaño de la ventana para que cubra toda la pantalla
window.resizable(False, False)  # Impide que la ventana sea redimensionable
pygame.mixer.init()  # Inicializa el mixer de Pygame para la reproducción de música y sonidos

# Carga la información de las monedas guardadas
cargar_monedas()
# Carga la información de los skins que ya han sido comprados
cargar_skins_compradas()
# Carga el skin actual seleccionado por el jugador
cargar_skin_actual()

# Muestra la pantalla de inicio del juego
pantalla_inicio()

# Llama a la función actualizar_monedas después de 500 milisegundos para actualizar la visualización de las monedas
window.after(500, actualizar_monedas)

# Inicia el bucle principal de la interfaz gráfica de la ventana
window.mainloop()

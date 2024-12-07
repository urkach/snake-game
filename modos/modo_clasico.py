import pygame
import random

monedas = 0  # Variable global que almacena la cantidad de monedas

# Función para cargar las monedas guardadas en un archivo
def cargar_monedas(): 
    global monedas
    try:
        with open("monedas.txt", "r") as file:  # Intenta abrir el archivo "monedas.txt" para leer las monedas
            monedas = int(file.read())  # Lee el valor y lo convierte a entero
    except FileNotFoundError:  # Si el archivo no se encuentra, inicializa las monedas en 0
        monedas = 0

# Función para guardar las monedas en un archivo
def guardar_monedas():
    with open("monedas.txt", "w") as file:  # Abre el archivo "monedas.txt" en modo escritura
        file.write(str(monedas))  # Escribe el valor de monedas como cadena de texto

# Función para actualizar las monedas (también guarda el nuevo valor en el archivo)
def actualizar_monedas():
    print(f"monedas: {monedas}")  # Muestra la cantidad de monedas en la consola
    guardar_monedas()  # Guarda las monedas actuales en el archivo

# Función que se llama cuando la serpiente come fruta
def comer_fruta():
    global monedas
    monedas += 1  # Incrementa las monedas en 1
    actualizar_monedas()  # Actualiza las monedas y las guarda

# Función para cargar el skin actual de la serpiente desde un archivo
def cargar_skin_actual():
    global skin_actual
    try:
        with open("skin_actual.txt", "r") as file:  # Intenta abrir el archivo "skin_actual.txt" para leer el color del skin
            skin_actual = file.read().strip()  # Lee el contenido y lo limpia de espacios en blanco
    except FileNotFoundError:  # Si el archivo no se encuentra, asigna un color predeterminado ("green")
        skin_actual = "green"

# Función principal del juego
def gameLoop(window):
    
    pygame.init()  # Inicializa todos los módulos de Pygame
    pygame.mixer.init()  # Inicializa el mezclador de sonidos de Pygame

    # Definición de los colores que se usarán en el juego
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    # Configura la ventana del juego en modo pantalla completa
    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()  # Obtiene las dimensiones de la pantalla

    pygame.display.set_caption('Snake Game')  # Título de la ventana

    clock = pygame.time.Clock()  # Inicializa el reloj para controlar la velocidad del juego
    BLOCK_SIZE = 30  # Tamaño del bloque que representa cada parte de la serpiente

    # Fuentes para mostrar texto en el juego
    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)
    moneda_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True) 

    # Función para mostrar mensajes en la pantalla
    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)  # Renderiza el mensaje con el color proporcionado
        game_display.blit(mesg, [x, y])  # Dibuja el mensaje en la pantalla

    # Función para dibujar la serpiente
    def draw_snake(block_size, snake_list, skin_color):
        for x in snake_list:  # Itera sobre todos los segmentos de la serpiente
            pygame.draw.rect(game_display, skin_color, [x[0], x[1], block_size, block_size])  # Dibuja cada segmento

    game_over = False  # Variable para controlar si el juego ha terminado
    game_close = False  # Variable para controlar si el jugador ha perdido

    # Posición inicial de la serpiente
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    # Velocidades de la serpiente (sin movimiento inicial)
    x1_change = 0
    y1_change = 0

    # Inicialización de la longitud de la serpiente y su lista de segmentos
    snake_length = 1
    snake_list = [[x1, y1]]

    score = 0  # Puntuación inicial

    direction = None  # Dirección inicial de movimiento de la serpiente

    # Función para generar la comida en una posición aleatoria dentro de la pantalla
    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    foodx, foody = generate_food()  # Genera la primera comida

    cargar_monedas()  # Carga las monedas guardadas
    cargar_skin_actual()  # Carga el skin actual de la serpiente

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()  # Detén la música al perder
            game_display.fill(BLACK)  # Limpia la pantalla con el color de fondo negro
            message("¡HAS PERDIDO!", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 5)  # Muestra el mensaje de derrota
            message(f"PUNTUACION: {score}", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5)  # Muestra la puntuación final
            message("C (INICIAR) / Q (SALIR)", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)  # Opciones para reiniciar o salir
            pygame.display.update()  # Actualiza la pantalla

            # Captura los eventos del teclado
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Si el jugador presiona Q, sale del juego
                        times = pygame.mixer.music.get_pos()  # Guarda la posición de la música
                        pygame.quit()  # Cierra Pygame
                        window.deiconify()  # Restaura la ventana principal
                        pygame.mixer.init()  # Inicializa el mezclador de música
                        pygame.mixer.music.load('Audio/cyberpunk_audio.mp3')  # Carga música de fondo
                        pygame.mixer.music.play(loops=-1)  # Reproduce la música en bucle
                        pygame.mixer.music.rewind()  # Reinicia la música
                        pygame.mixer.music.set_pos(times / 1000)  # Reproduce la música desde donde se detuvo
                        return  # Sale de la función
                    if event.key == pygame.K_c:  # Si el jugador presiona C, reinicia el juego
                        pygame.mixer.music.play(loops=-1)  # Reproduce la música en bucle
                        gameLoop(window)  # Llama a la función principal para reiniciar el juego

        # Captura los eventos del teclado para mover la serpiente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si el jugador cierra la ventana
                game_over = True
            if event.type == pygame.KEYDOWN:  # Si el jugador presiona una tecla
                # Controles para el movimiento de la serpiente
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change = -BLOCK_SIZE  # Mueve a la izquierda
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change = BLOCK_SIZE  # Mueve a la derecha
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y1_change = -BLOCK_SIZE  # Mueve hacia arriba
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y1_change = BLOCK_SIZE  # Mueve hacia abajo
                    x1_change = 0
                    direction = "DOWN"

        # Verifica si la serpiente ha salido de los límites de la pantalla
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change  # Actualiza la posición horizontal de la serpiente
        y1 += y1_change  # Actualiza la posición vertical de la serpiente
        game_display.fill(BLACK)  # Limpia la pantalla con el color de fondo negro

        # Dibuja la comida en pantalla
        pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x1, y1]  # Actualiza la cabeza de la serpiente
        snake_list.append(snake_head)  # Agrega la nueva cabeza al final de la lista

        # Si la longitud de la serpiente excede su tamaño, elimina el segmento más antiguo
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Verifica si la serpiente se ha mordido a sí misma
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Dibuja la serpiente
        draw_snake(BLOCK_SIZE, snake_list, skin_actual)

        # Verifica si la serpiente ha comido la comida
        if x1 - BLOCK_SIZE <= foodx <= x1 + BLOCK_SIZE and y1 - BLOCK_SIZE <= foody <= y1 + BLOCK_SIZE:
            foodx, foody = generate_food()  # Genera una nueva comida
            snake_length += 1  # Aumenta la longitud de la serpiente
            score += 1  # Incrementa la puntuación
            comer_fruta()  # Incrementa las monedas

        # Muestra la puntuación y las monedas en pantalla
        score_text = score_font.render("PUNTUACION: " + str(score), True, WHITE)
        monedas_text = moneda_font.render("Monedas: " + str(monedas), True, YELLOW)
        game_display.blit(score_text, [10, 10])  # Dibuja la puntuación en la parte superior
        game_display.blit(monedas_text, [10, 50])  # Dibuja las monedas en la parte inferior

        pygame.display.update()  # Actualiza la pantalla

        clock.tick(15)  # Controla la velocidad del juego

    pygame.quit()  # Finaliza el juego
    quit()  # Termina el programa

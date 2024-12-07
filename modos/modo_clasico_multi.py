import pygame
import random

# Inicialización de las variables globales
monedas = 0

# Funciones para manejar monedas y skins
def cargar_monedas(): 
    global monedas
    try:
        # Cargar las monedas guardadas desde un archivo
        with open("monedas.txt", "r") as file:
            monedas = int(file.read())
    except FileNotFoundError:
        # Si el archivo no existe, se inicia con 0 monedas
        monedas = 0
        
def guardar_monedas():
    # Guardar las monedas en un archivo
    with open("monedas.txt", "w") as file:
        file.write(str(monedas))

def actualizar_monedas():
    # Mostrar las monedas actuales en la consola para depuración
    print(f"Monedas: {monedas}")

def comer_fruta():
    global monedas
    # Aumentar las monedas al comer una fruta
    monedas += 1
    actualizar_monedas()

def cargar_skin_actual():
    global skin_actual1, skin_actual2
    skin_actual1 = (0, 255, 0)  # Verde para el jugador 1
    try:
        # Intentar cargar el skin del jugador 2 desde un archivo
        with open("skin_actual2.txt", "r") as file: 
            skin_actual2 = file.read().strip() 
    except FileNotFoundError: 
        # Si no se encuentra el archivo, se asigna un color azul por defecto
        skin_actual2 = (0, 0, 255)  # Azul para el jugador 2

# Función para verificar colisiones con tolerancia
def check_collision(pos1, pos2, tolerance=10):
    return abs(pos1[0] - pos2[0]) <= tolerance and abs(pos1[1] - pos2[1]) <= tolerance

def verificar_colision_serpientes(snake1, snake2, tolerance=10):
    # Verificar si hay colisión entre dos serpientes
    for segmento1 in snake1:
        for segmento2 in snake2:
            if check_collision(segmento1, segmento2, tolerance):
                return True
    return False

# Función principal del juego
def gameLoop(window):
    pygame.init()  # Inicializar pygame
    pygame.mixer.init()  # Inicializar mezclador de audio
    
    # Definición de los colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    # Configuración de la pantalla
    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    pygame.display.set_caption('Snake Game - Multijugador')

    clock = pygame.time.Clock()  # Controlador de velocidad del juego
    BLOCK_SIZE = 30  # Tamaño del bloque de la serpiente y la comida

    # Fuentes para los textos
    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)
    moneda_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)

    # Función para mostrar mensajes en la pantalla
    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    # Función para dibujar la serpiente
    def draw_snake(block_size, snake_list, skin_color):
        for x in snake_list:
            pygame.draw.rect(game_display, skin_color, [x[0], x[1], block_size, block_size])

    game_over = False  # Indica si el juego ha terminado
    game_close = False  # Indica si el jugador ha perdido

    # Inicialización de las posiciones de las serpientes
    x1, y1 = SCREEN_WIDTH * 3/ 4, SCREEN_HEIGHT / 2
    x1_change, y1_change = 0, 0
    snake1_length = 1
    snake1_list = [[x1, y1]]

    x2, y2 = SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2
    x2_change, y2_change = 0, 0
    snake2_length = 1
    snake2_list = [[x2, y2]]

    score1, score2 = 0, 0  # Puntuaciones de los jugadores
    direction1, direction2 = None, None  # Direcciones de las serpientes

    # Función para generar la comida en una posición aleatoria
    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    # Generar la primera comida
    foodx, foody = generate_food()

    cargar_monedas()  # Cargar las monedas desde el archivo
    cargar_skin_actual()  # Cargar los skins de los jugadores

    while not game_over:
        while game_close:
            # Mostrar la pantalla de fin de juego
            pygame.mixer.music.stop()  # Detener la música
            game_display.fill(BLACK)
            message("¡HAS PERDIDO!", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 5.5)
            message(f"PLAYER 1: {score1} PTS", skin_actual1, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2.5)
            message(f"PLAYER 2: {score2} PTS", skin_actual2, SCREEN_WIDTH * 3 / 4 - 200, SCREEN_HEIGHT / 2.5)
            message("C (INICIAR) / Q (SALIR)", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)
            pygame.display.update()

            # Esperar la interacción del usuario para reiniciar o salir
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        times = pygame.mixer.music.get_pos()
                        pygame.quit()
                        window.deiconify()
                        pygame.mixer.init()
                        pygame.mixer.music.load('Audio/cyberpunk_audio.mp3')
                        pygame.mixer.music.play(loops=-1)
                        pygame.mixer.music.rewind()
                        pygame.mixer.music.set_pos(times / 1000)
                        return
                    if event.key == pygame.K_c:
                        pygame.mixer.music.play(loops=-1)
                        gameLoop(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True  # Terminar el juego si se cierra la ventana
            if event.type == pygame.KEYDOWN:
                # Controles para la serpiente 1
                if event.key == pygame.K_LEFT and direction1 != "RIGHT":
                    x1_change, y1_change = -BLOCK_SIZE, 0
                    direction1 = "LEFT"
                elif event.key == pygame.K_RIGHT and direction1 != "LEFT":
                    x1_change, y1_change = BLOCK_SIZE, 0
                    direction1 = "RIGHT"
                elif event.key == pygame.K_UP and direction1 != "DOWN":
                    x1_change, y1_change = 0, -BLOCK_SIZE
                    direction1 = "UP"
                elif event.key == pygame.K_DOWN and direction1 != "UP":
                    x1_change, y1_change = 0, BLOCK_SIZE
                    direction1 = "DOWN"
                # Controles para la serpiente 2
                elif event.key == pygame.K_a and direction2 != "RIGHT":
                    x2_change, y2_change = -BLOCK_SIZE, 0
                    direction2 = "LEFT"
                elif event.key == pygame.K_d and direction2 != "LEFT":
                    x2_change, y2_change = BLOCK_SIZE, 0
                    direction2 = "RIGHT"
                elif event.key == pygame.K_w and direction2 != "DOWN":
                    x2_change, y2_change = 0, -BLOCK_SIZE
                    direction2 = "UP"
                elif event.key == pygame.K_s and direction2 != "UP":
                    x2_change, y2_change = 0, BLOCK_SIZE
                    direction2 = "DOWN"

        # Actualizar las posiciones de las serpientes
        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change

        # Verificar si alguna serpiente sale de la pantalla o colisiona
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0 or x2 >= SCREEN_WIDTH or x2 < 0 or y2 >= SCREEN_HEIGHT or y2 < 0:
            game_close = True

        # Actualizar la lista de segmentos de las serpientes
        snake1_head = [x1, y1]
        snake1_list.append(snake1_head)
        if len(snake1_list) > snake1_length:
            del snake1_list[0]

        snake2_head = [x2, y2]
        snake2_list.append(snake2_head)
        if len(snake2_list) > snake2_length:
            del snake2_list[0]

        # Verificación de colisión entre las dos serpientes
        if verificar_colision_serpientes(snake1_list, snake2_list):
            game_close = True

        # Verificar colisión con la comida para ambos jugadores
        if check_collision([x1, y1], [foodx, foody]):
            foodx, foody = generate_food()
            snake1_length += 1
            score1 += 1
            comer_fruta()

        if check_collision([x2, y2], [foodx, foody]):
            foodx, foody = generate_food()
            snake2_length += 1
            score2 += 1
            comer_fruta()

        # Dibujar el juego
        game_display.fill(BLACK)
        pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        draw_snake(BLOCK_SIZE, snake1_list, skin_actual1)
        draw_snake(BLOCK_SIZE, snake2_list, skin_actual2)

        # Mostrar las puntuaciones y las monedas
        score_text1 = score_font.render("JUGADOR 1: " + str(score1), True, skin_actual1)
        score_text2 = score_font.render("JUGADOR 2: " + str(score2), True, skin_actual2)
        monedas_text = moneda_font.render("Monedas: " + str(monedas), True, YELLOW)
        game_display.blit(score_text1, [10, 10])
        game_display.blit(score_text2, [10, 50])
        game_display.blit(monedas_text, [10, 90])

        pygame.display.update()  # Actualizar la pantalla
        clock.tick(15)  # Control de la velocidad del juego

    guardar_monedas()  # Guardar las monedas al finalizar el juego
    pygame.quit()  # Finalizar pygame
    quit()  # Salir del programa

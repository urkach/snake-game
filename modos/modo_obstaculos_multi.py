import pygame
import random

# Variables globales para manejar monedas y skins
monedas = 0

# Función para cargar las monedas guardadas desde un archivo
def cargar_monedas():
    global monedas
    try:
        with open("monedas.txt", "r") as file:
            monedas = int(file.read())  # Lee el archivo y convierte el valor a entero
    except FileNotFoundError:
        monedas = 0  # Si el archivo no existe, inicializa las monedas en 0

# Función para guardar el valor actual de monedas en un archivo
def guardar_monedas():
    with open("monedas.txt", "w") as file:
        file.write(str(monedas))  # Escribe las monedas actuales en el archivo

# Función para actualizar el conteo de monedas en consola
def actualizar_monedas():
    print(f"Monedas: {monedas}")

# Función para incrementar monedas al comer una fruta
def comer_fruta():
    global monedas
    monedas += 1  # Incrementa las monedas
    actualizar_monedas()

# Función para cargar las skins actuales de los jugadores
def cargar_skin_actual():
    global skin_actual1, skin_actual2
    skin_actual1 = (0, 255, 0)  # Verde por defecto para jugador 1
    try:
        with open("skin_actual2.txt", "r") as file:
            skin_actual2 = tuple(map(int, file.read().strip().split(",")))  # Lee la skin guardada para jugador 2
    except FileNotFoundError:
        skin_actual2 = (0, 0, 255)  # Azul por defecto para jugador 2

# Función para verificar si dos posiciones están dentro de un rango de tolerancia
def check_collision(pos1, pos2, tolerance=25):
    return abs(pos1[0] - pos2[0]) <= tolerance and abs(pos1[1] - pos2[1]) <= tolerance

# Función para detectar colisiones entre dos serpientes
def verificar_colision_serpientes(snake1, snake2, tolerance=10):
    for segmento1 in snake1:
        for segmento2 in snake2:
            if check_collision(segmento1, segmento2, tolerance):  # Compara cada segmento de ambas serpientes
                return True
    return False

# Función principal del juego
def gameLoop(window):
    # Inicialización de pygame
    pygame.init()
    pygame.mixer.init()

    # Cargar la música
    pygame.mixer.music.load("Audio/cyberpunk_audio.mp3")
    pygame.mixer.music.play(-1, 0.0)  # La música se repetirá infinitamente.

    # Definición de colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    # Configuración de pantalla
    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Pantalla completa
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    pygame.display.set_caption('Snake Game - Multijugador con Obstáculos')

    # Inicialización del reloj y tamaño de bloques
    clock = pygame.time.Clock()
    BLOCK_SIZE = 30
    OBSTACLE_SIZE = 40

    # Configuración de fuentes
    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)
    moneda_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)

    # Función para mostrar mensajes en pantalla
    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    # Función para dibujar las serpientes
    def draw_snake(block_size, snake_list, skin_color):
        for x in snake_list:
            pygame.draw.rect(game_display, skin_color, [x[0], x[1], block_size, block_size])

    # Variables de estado del juego
    game_over = False
    game_close = False

    # Posición inicial del jugador 1
    x1, y1 = SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 2
    x1_change, y1_change = 0, 0
    snake1_length = 1
    snake1_list = [[x1, y1]]

    # Posición inicial del jugador 2
    x2, y2 = SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2
    x2_change, y2_change = 0, 0
    snake2_length = 1
    snake2_list = [[x2, y2]]

    # Puntuaciones iniciales
    score1, score2 = 0, 0
    direction1, direction2 = None, None

    # Lista de obstáculos
    obstacles = []

    # Generación inicial de comida
    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    def generate_obstacle():
        return (
            round(random.randrange(0, SCREEN_WIDTH - OBSTACLE_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - OBSTACLE_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    foodx, foody = generate_food()

    # Cargar monedas y skins iniciales
    cargar_monedas()
    cargar_skin_actual()

    # Bucle principal del juego
    while not game_over:
        while game_close:
            pygame.mixer.music.stop()
            game_display.fill(BLACK)

            # Determinar el ganador
            ganador = None
            if (x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0) or any(block == [x1, y1] for block in snake1_list[:-1]):
                ganador = "PLAYER 2"  # Gana el jugador 2
            elif (x2 >= SCREEN_WIDTH or x2 < 0 or y2 >= SCREEN_HEIGHT or y2 < 0) or any(block == [x2, y2] for block in snake2_list[:-1]):
                ganador = "PLAYER 1"  # Gana el jugador 1

            if ganador:
                message(f"¡{ganador} HA GANADO LA PARTIDA!", YELLOW, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 5.5)

            # Mostrar puntuaciones y opciones
            message(f"PLAYER 1: {score1} PTS", skin_actual1, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2.5)
            message(f"PLAYER 2: {score2} PTS", skin_actual2, SCREEN_WIDTH * 3 / 4 - 200, SCREEN_HEIGHT / 2.5)
            message("C (INICIAR) / Q (SALIR)", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)
            pygame.display.update()

            # Manejo de eventos en pantalla de game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        # Salir del juego
                        pygame.quit()
                        window.deiconify()
                        return
                    if event.key == pygame.K_c:
                        # Reiniciar el juego
                        pygame.mixer.music.play(loops=-1)  # Reanuda la música
                        gameLoop(window)

        # Manejo de eventos durante el juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Controles del jugador 1
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
                # Controles del jugador 2
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

        # Actualización de posiciones
        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change

        # Verificar colisiones con los bordes, comida, y obstáculos
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0 or \
           x2 >= SCREEN_WIDTH or x2 < 0 or y2 >= SCREEN_HEIGHT or \
           verificar_colision_serpientes(snake1_list, snake2_list):
            game_close = True

        # Comprobar colisión con obstáculos
        for obs in obstacles:
            if check_collision([x1, y1], obs) or check_collision([x2, y2], obs):
                game_close = True

        game_display.fill(BLACK)

        # Dibujar comida, serpientes y obstáculos
        pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        draw_snake(BLOCK_SIZE, snake1_list, skin_actual1)
        draw_snake(BLOCK_SIZE, snake2_list, skin_actual2)

        for obs in obstacles:
            pygame.draw.rect(game_display, RED, [obs[0], obs[1], OBSTACLE_SIZE, OBSTACLE_SIZE])

        # Actualizar puntajes y monedas en pantalla
        score_text1 = score_font.render("JUGADOR 1: " + str(score1), True, skin_actual1)
        score_text2 = score_font.render("JUGADOR 2: " + str(score2), True, skin_actual2)
        monedas_text = moneda_font.render(f"MONEDAS: {monedas}", True, YELLOW)

        game_display.blit(score_text1, (20, 20))
        game_display.blit(score_text2, (20, 60))
        game_display.blit(monedas_text, (20, 100))

        # Crecimiento de las serpientes
        snake1_head = [x1, y1]
        snake2_head = [x2, y2]
        snake1_list.append(snake1_head)
        snake2_list.append(snake2_head)

        if len(snake1_list) > snake1_length:
            del snake1_list[0]
        if len(snake2_list) > snake2_length:
            del snake2_list[0]

        # Verificar colisiones internas
        for block in snake1_list[:-1]:
            if block == snake1_head:
                game_close = True
        for block in snake2_list[:-1]:
            if block == snake2_head:
                game_close = True

        # Comprobar si las serpientes han comido la comida
        if check_collision([x1, y1], [foodx, foody]):
            foodx, foody = generate_food()
            snake1_length += 1
            score1 += 1
            comer_fruta()
            obstacles.append(generate_obstacle())  # Agregar un nuevo obstáculo

        if check_collision([x2, y2], [foodx, foody]):
            foodx, foody = generate_food()
            snake2_length += 1
            score2 += 1
            comer_fruta()
            obstacles.append(generate_obstacle())  # Agregar un nuevo obstáculo

        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    guardar_monedas()  # Guardar monedas al finalizar el juego

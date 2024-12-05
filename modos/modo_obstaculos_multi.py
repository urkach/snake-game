import pygame
import random

monedas = 0

# Funciones para manejar monedas y skins
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

def actualizar_monedas():
    print(f"Monedas: {monedas}")

def comer_fruta():
    global monedas
    monedas += 1
    actualizar_monedas()

def cargar_skin_actual():
    global skin_actual1, skin_actual2
    # Forzar el color verde para la serpiente del jugador 1
    skin_actual1 = (0, 255, 0)  # Verde
    try:
        with open("skin_actual2.txt", "r") as file: 
            skin_actual2 = file.read().strip() 
    except FileNotFoundError: 
        skin_actual2 = (0, 0, 255)  # Azul predeterminado

# Función para verificar colisiones con tolerancia
def check_collision(pos1, pos2, tolerance=10):
    return abs(pos1[0] - pos2[0]) <= tolerance and abs(pos1[1] - pos2[1]) <= tolerance

def verificar_colision_serpientes(snake1, snake2, tolerance=10):
    for segmento1 in snake1:
        for segmento2 in snake2:
            if check_collision(segmento1, segmento2, tolerance):
                return True
    return False

# Función principal del juego
def gameLoop(window):
    pygame.init()
    pygame.mixer.init()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    pygame.display.set_caption('Snake Game - Multijugador con Obstáculos')

    clock = pygame.time.Clock()
    BLOCK_SIZE = 30
    OBSTACLE_SIZE = 40

    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)
    moneda_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True) 

    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    def draw_snake(block_size, snake_list, skin_color):
        for x in snake_list:
            pygame.draw.rect(game_display, skin_color, [x[0], x[1], block_size, block_size])

    game_over = False
    game_close = False

    x1, y1 = SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 2
    x1_change, y1_change = 0, 0
    snake1_length = 1
    snake1_list = [[x1, y1]]

    x2, y2 = SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2
    x2_change, y2_change = 0, 0
    snake2_length = 1
    snake2_list = [[x2, y2]]

    score1, score2 = 0, 0
    direction1, direction2 = None, None

    obstacles = []

    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    foodx, foody = generate_food()
    cargar_monedas()
    cargar_skin_actual()

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()
            game_display.fill(BLACK)
            message("¡HAS PERDIDO!", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 5.5)
            message(f"PLAYER 1: {score1} PTS", skin_actual1, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2.5)
            message(f"PLAYER 2: {score2} PTS", skin_actual2, SCREEN_WIDTH * 3 / 4 - 200, SCREEN_HEIGHT / 2.5)
            message("C (INICIAR) / Q (SALIR)", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)
            pygame.display.update()

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
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Controles para jugador 1
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
                # Controles para jugador 2
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

        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0 or x2 >= SCREEN_WIDTH or x2 < 0 or y2 >= SCREEN_HEIGHT or y2 < 0:
            game_close = True

        # Dibujar y verificar obstáculos
        game_display.fill(BLACK)
        for obstacle in obstacles:
            pygame.draw.rect(game_display, RED, [obstacle[0], obstacle[1], OBSTACLE_SIZE, OBSTACLE_SIZE])
            if (obstacle[0] <= x1 < obstacle[0] + OBSTACLE_SIZE and obstacle[1] <= y1 < obstacle[1] + OBSTACLE_SIZE) or \
               (obstacle[0] <= x2 < obstacle[0] + OBSTACLE_SIZE and obstacle[1] <= y2 < obstacle[1] + OBSTACLE_SIZE):
                game_close = True

        # Verificar colisiones entre serpientes
        if verificar_colision_serpientes(snake1_list, snake2_list):
            game_close = True

        # Verificar colisión con comida
        if check_collision([x1, y1], [foodx, foody]):
            foodx, foody = generate_food()
            snake1_length += 1
            score1 += 1
            comer_fruta()
            obstacles.append(generate_food())

        if check_collision([x2, y2], [foodx, foody]):
            foodx, foody = generate_food()
            snake2_length += 1
            score2 += 1
            comer_fruta()
            obstacles.append(generate_food())

        # Dibujar serpientes y comida
        pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        draw_snake(BLOCK_SIZE, snake1_list, skin_actual1)
        draw_snake(BLOCK_SIZE, snake2_list, skin_actual2)


        # Dibujar puntajes y monedas en la parte superior izquierda
        score_text1 = score_font.render("JUGADOR 1: " + str(score1), True, skin_actual1)
        score_text2 = score_font.render("JUGADOR 2: " + str(score2), True, skin_actual2)
        monedas_text = moneda_font.render(f"MONEDAS: {monedas}", True, YELLOW)

        # Posiciones ajustadas para la parte superior izquierda
        game_display.blit(score_text1, (20, 20))   # PLAYER 1 en la parte superior
        game_display.blit(score_text2, (20, 60))   # PLAYER 2 debajo de PLAYER 1
        game_display.blit(monedas_text, (20, 100)) # MONEDAS debajo de PLAYER 2



        # Mover y verificar colisión de la serpiente consigo misma
        snake1_head = [x1, y1]
        snake2_head = [x2, y2]
        snake1_list.append(snake1_head)
        snake2_list.append(snake2_head)

        if len(snake1_list) > snake1_length:
            del snake1_list[0]
        if len(snake2_list) > snake2_length:
            del snake2_list[0]

        for block in snake1_list[:-1]:
            if block == snake1_head:
                game_close = True
        for block in snake2_list[:-1]:
            if block == snake2_head:
                game_close = True

        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    guardar_monedas()

import pygame
import random
import time

monedas = 0  # Variable global para llevar el conteo de monedas

# Funciones para manejar las monedas
def cargar_monedas(): 
    global monedas
    try:
        # Intentamos cargar las monedas desde un archivo
        with open("monedas.txt", "r") as file:
            monedas = int(file.read())
    except FileNotFoundError:
        # Si el archivo no se encuentra, inicializamos las monedas a 0
        monedas = 0
        
def guardar_monedas():
    # Guardamos el valor de las monedas en un archivo
    with open("monedas.txt", "w") as file:
        file.write(str(monedas))

def actualizar_monedas():
    # Función que actualiza y guarda las monedas
    print(f"monedas:{monedas}")
    guardar_monedas()

def comer_fruta():
    # Función que se llama cuando la serpiente come una fruta
    global monedas
    monedas += 1
    actualizar_monedas()

# Cargar el skin actual de la serpiente desde un archivo
def cargar_skin_actual():
    global skin_actual
    try: 
        # Leemos el archivo donde está guardado el skin
        with open("skin_actual.txt", "r") as file: 
            skin_actual = file.read().strip() 
    except FileNotFoundError: 
        # Si el archivo no existe, asignamos el skin por defecto
        skin_actual = "green"


def gameLoop(window):
    pygame.init()  # Inicializamos Pygame
    pygame.mixer.init()  # Inicializamos el mezclador de sonidos

    # Definimos los colores que usaremos en el juego
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    # Establecemos la ventana de juego a pantalla completa
    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    # Título de la ventana
    pygame.display.set_caption('Snake Game')

    # Establecemos el reloj para controlar la tasa de refresco
    clock = pygame.time.Clock()
    BLOCK_SIZE = 30  # Tamaño de los bloques que forman la serpiente

    # Fuentes de texto para mostrar en la pantalla
    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)
    moneda_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True) 

    # Función para mostrar un mensaje en pantalla
    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    # Función para dibujar la serpiente en la pantalla
    def draw_snake(block_size, snake_list, skin_color):
        for x in snake_list:
            pygame.draw.rect(game_display, skin_color, [x[0], x[1], block_size, block_size])

    # Función para generar una posición aleatoria de la comida
    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    cargar_monedas()  # Cargamos las monedas al inicio
    cargar_skin_actual()  # Cargamos el skin de la serpiente

    # Nueva función para verificar colisiones exactas de la serpiente con la comida
    def check_collision(pos1, pos2, size=BLOCK_SIZE):
        """
        Verifica si dos rectángulos definidos por sus posiciones y tamaño se superponen.
        pos1 y pos2 son las esquinas superiores izquierdas de los rectángulos.
        """
        rect1_x, rect1_y = pos1
        rect2_x, rect2_y = pos2

        return (
            rect1_x < rect2_x + size and  # El borde derecho del rectángulo 1 no está a la izquierda del rectángulo 2
            rect1_x + size > rect2_x and  # El borde izquierdo del rectángulo 1 no está a la derecha del rectángulo 2
            rect1_y < rect2_y + size and  # El borde inferior del rectángulo 1 no está arriba del rectángulo 2
            rect1_y + size > rect2_y      # El borde superior del rectángulo 1 no está debajo del rectángulo 2
        )

    # Función para hacer vibrar la pantalla cuando el jugador pierde
    def vibrate_screen():
        offsets = [(-10, 0), (10, 0), (0, -10), (0, 10)]
        original = game_display.copy()
        vibration_duration = random.uniform(0.3, 0.7)  # Tiempo aleatorio entre 0.3 y 0.7 segundos
        vibration_start = time.time()
        while time.time() - vibration_start < vibration_duration:
            for dx, dy in offsets:
                game_display.blit(original, (dx, dy))
                pygame.display.update()
                pygame.time.wait(50)
                game_display.blit(original, (0, 0))
                pygame.display.update()

    game_over = False
    game_close = False

    # Posición inicial de la serpiente
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_length = 1  # Longitud inicial de la serpiente
    snake_list = [[x1, y1]]  # Lista que guarda las posiciones de los segmentos de la serpiente

    score = 0  # Puntuación inicial
    current_direction = None  # Dirección inicial de la serpiente

    food_positions = [generate_food()]  # Lista inicial de bloques de comida
    obstacle_positions = []  # Lista de posiciones de obstáculos
    obstacle_directions = []  # Lista de direcciones para cada obstáculo
    obstacle_tick = 0  # Contador para reducir la velocidad de movimiento de los obstáculos

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()  # Detenemos la música al perder
            game_display.fill(BLACK)
            message("¡HAS PERDIDO!", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 5)
            message(f"PUNTUACION: {score} PTS", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5)
            message("C (INICIAR) / Q (SALIR)", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        times = pygame.mixer.music.get_pos()  # Guardamos el tiempo de la música
                        pygame.quit()  # Terminamos el juego
                        window.deiconify()  # Restauramos la ventana principal
                        pygame.mixer.init()
                        pygame.mixer.music.load('Audio/cyberpunk_audio.mp3')  # Cargamos la música de fondo
                        pygame.mixer.music.play(loops=-1)  # Reproducimos la música en bucle
                        pygame.mixer.music.rewind()  # Rewind de la música
                        pygame.mixer.music.set_pos(times / 1000)  # Retornamos al tiempo guardado
                        return
                    if event.key == pygame.K_c:
                        pygame.mixer.music.play(loops=-1)  # Reanuda la música al reiniciar
                        gameLoop(window)  # Reiniciamos el juego

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                    current_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                    current_direction = "RIGHT"
                elif event.key == pygame.K_UP and current_direction != "DOWN":
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                    current_direction = "UP"
                elif event.key == pygame.K_DOWN and current_direction != "UP":
                    y1_change = BLOCK_SIZE
                    x1_change = 0
                    current_direction = "DOWN"

        # Verificamos si la serpiente choca con los límites de la pantalla
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        game_display.fill(BLACK)

        # Dibujamos los bloques de comida en pantalla
        for foodx, foody in food_positions:
            pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # Dibujamos los obstáculos
        for obsx, obsy in obstacle_positions:
            pygame.draw.rect(game_display, RED, [obsx, obsy, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Colisión con la propia serpiente (el jugador pierde)
        for segment in snake_list[:-1]:
            if check_collision(segment, snake_head):
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list, skin_actual)

        # Verificamos si la serpiente come la comida
        for foodx, foody in food_positions[:]:
            if check_collision((x1, y1), (foodx, foody)):
                food_positions.remove((foodx, foody))
                vibrate_screen()  # Hacemos vibrar la pantalla al comer una fruta
                snake_length += 1
                score += 1
                food_positions.append(generate_food())
                # Agregamos obstáculos nuevos
                new_obstacles = random.randint(1, 3)
                for _ in range(new_obstacles):
                    obstacle_positions.append(generate_food())
                    obstacle_directions.append(random.choice(["HORIZONTAL", "VERTICAL"]))

        # Movimiento de obstáculos (mitad de velocidad)
        obstacle_tick += 1
        if obstacle_tick >= 2:
            for i in range(len(obstacle_positions)):
                obsx, obsy = obstacle_positions[i]
                direction = obstacle_directions[i]
                if direction == "HORIZONTAL":
                    obsx += random.choice([-BLOCK_SIZE, BLOCK_SIZE])
                    obsx = max(0, min(obsx, SCREEN_WIDTH - BLOCK_SIZE))
                elif direction == "VERTICAL":
                    obsy += random.choice([-BLOCK_SIZE, BLOCK_SIZE])
                    obsy = max(0, min(obsy, SCREEN_HEIGHT - BLOCK_SIZE))
                obstacle_positions[i] = (obsx, obsy)
            obstacle_tick = 0

        # Colisión con obstáculos (el jugador pierde)
        for obsx, obsy in obstacle_positions:
            if check_collision((x1, y1), (obsx, obsy)):
                game_close = True

        # Mostrar la puntuación y las monedas en pantalla
        score_text = score_font.render("PUNTUACION: " + str(score), True, WHITE)
        monedas_text = moneda_font.render("Monedas: " + str(monedas), True, YELLOW)
        game_display.blit(score_text, [10, 10])
        game_display.blit(monedas_text, [10, 50])
        pygame.display.update()

        clock.tick(15)  # Establecemos la velocidad del juego (15 cuadros por segundo)

    pygame.quit()  # Terminamos Pygame
    quit()

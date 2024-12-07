import pygame
import random

monedas = 0  # Variable para almacenar las monedas

# Función para cargar las monedas guardadas desde un archivo
def cargar_monedas(): 
    global monedas
    try:
        with open("monedas.txt", "r") as file:
            monedas = int(file.read())  # Lee el valor y lo convierte a entero
    except FileNotFoundError:
        monedas = 0  # Si no existe el archivo, se establece en 0

# Función para guardar las monedas actuales en un archivo
def guardar_monedas():
    with open("monedas.txt", "w") as file:
        file.write(str(monedas))  # Escribe las monedas actuales como cadena

# Función para actualizar las monedas, imprimiéndolas y guardándolas
def actualizar_monedas():
    print(f"monedas: {monedas}")
    guardar_monedas()

# Función que se llama cuando el jugador come una fruta
def comer_fruta():
    global monedas
    monedas += 1  # Aumenta el contador de monedas
    actualizar_monedas()  # Actualiza y guarda las monedas

# Función para cargar el skin actual desde un archivo
def cargar_skin_actual():
    global skin_actual
    try: 
        with open("skin_actual.txt", "r") as file: 
            skin_actual = file.read().strip()  # Lee el skin y elimina espacios
    except FileNotFoundError: 
        skin_actual = "green"  # Si no existe el archivo, se establece el skin predeterminado

# Función principal del juego
def gameLoop(window):
    pygame.init()  # Inicializa Pygame
    pygame.mixer.init()  # Inicializa el mezclador de sonido de Pygame

    # Definición de colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    # Establecer el tamaño de la pantalla a pantalla completa
    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()  # Obtiene el tamaño de la pantalla

    pygame.display.set_caption('Snake Game')  # Título de la ventana

    clock = pygame.time.Clock()  # Inicializa el reloj para controlar la velocidad del juego
    BLOCK_SIZE = 30  # Tamaño de cada bloque de la serpiente y comida
    OBSTACLE_SIZE = 40  # Tamaño de los obstáculos

    # Fuentes para mostrar textos en el juego
    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)
    moneda_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True) 

    # Función para mostrar mensajes en pantalla
    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    # Función para dibujar la serpiente en pantalla
    def draw_snake(block_size, snake_list, skin_color):
        for x in snake_list:
            pygame.draw.rect(game_display, skin_color, [x[0], x[1], block_size, block_size])

    game_over = False
    game_close = False

    # Coordenadas iniciales de la serpiente
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    # Velocidad inicial de movimiento de la serpiente
    x1_change = 0
    y1_change = 0

    snake_length = 1  # Longitud inicial de la serpiente
    snake_list = [[x1, y1]]  # Lista que guarda los segmentos de la serpiente

    score = 0  # Puntuación inicial

    direction = None  # Dirección de la serpiente

    # Función para generar la comida de manera aleatoria
    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    foodx, foody = generate_food()  # Genera la primera comida
    cargar_monedas()  # Carga las monedas guardadas
    cargar_skin_actual()  # Carga el skin actual de la serpiente
    obstacles = []  # Lista de obstáculos

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()  # Detiene la música cuando el jugador pierde
            game_display.fill(BLACK)
            message("¡HAS PERDIDO!", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 5)  # Mensaje de pérdida
            message(f"PUNTUACION: {score}", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5)
            message("C (INICIAR) / Q (SALIR)", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Si presiona 'Q', sale del juego
                        times = pygame.mixer.music.get_pos()
                        pygame.quit()
                        window.deiconify()
                        pygame.mixer.init()
                        pygame.mixer.music.load('Audio/cyberpunk_audio.mp3')
                        pygame.mixer.music.play(loops=-1)
                        pygame.mixer.music.rewind()
                        pygame.mixer.music.set_pos(times / 1000)
                        return
                    if event.key == pygame.K_c:  # Si presiona 'C', reinicia el juego
                        pygame.mixer.music.play(loops=-1)  # Reanuda la música
                        gameLoop(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True  # Si se cierra la ventana, termina el juego
            if event.type == pygame.KEYDOWN:
    
                # Cambia la dirección de la serpiente según la tecla presionada
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y1_change = BLOCK_SIZE
                    x1_change = 0
                    direction = "DOWN"

        # Verifica si la serpiente choca con los bordes de la pantalla
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change  # Actualiza la posición de la serpiente
        y1 += y1_change
        game_display.fill(BLACK)  # Limpia la pantalla

        # Dibuja los obstáculos
        for obstacle in obstacles:
            pygame.draw.rect(game_display, RED, [obstacle[0], obstacle[1], OBSTACLE_SIZE, OBSTACLE_SIZE])
            if obstacle[0] <= x1 < obstacle[0] + OBSTACLE_SIZE and obstacle[1] <= y1 < obstacle[1] + OBSTACLE_SIZE:
                game_close = True  # Si la serpiente choca con un obstáculo, termina el juego

        pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])  # Dibuja la comida

        # Agrega un nuevo segmento a la serpiente
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        # Elimina el segmento más antiguo si la longitud de la serpiente supera su tamaño
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Verifica si la serpiente se choca consigo misma
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list, skin_actual)  # Dibuja la serpiente con el color actual
        if x1 - BLOCK_SIZE <= foodx <= x1 + BLOCK_SIZE and y1 - BLOCK_SIZE <= foody <= y1 + BLOCK_SIZE:  # Verifica si la serpiente come la comida
            foodx, foody = generate_food()  # Genera nueva comida
            snake_length += 1  # Aumenta la longitud de la serpiente
            score += 1  # Aumenta la puntuación

            # Añade un nuevo obstáculo aleatorio
            new_obstacle = [
                round(random.randrange(0, SCREEN_WIDTH - OBSTACLE_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
                round(random.randrange(0, SCREEN_HEIGHT - OBSTACLE_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            ]
            obstacles.append(new_obstacle)

        # Muestra la puntuación y las monedas en pantalla
        score_text = score_font.render("PUNTUACION: " + str(score), True, WHITE)
        monedas_text = moneda_font.render("Monedas: " + str(monedas), True, YELLOW)
        game_display.blit(score_text, [10, 10])
        game_display.blit(monedas_text, [10, 50])
        pygame.display.update()  # Actualiza la pantalla

        clock.tick(15)  # Controla la velocidad del juego

    pygame.quit()  # Finaliza Pygame
    quit()

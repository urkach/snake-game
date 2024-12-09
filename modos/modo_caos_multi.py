import pygame
import random
import time

# Variable global para almacenar las monedas
monedas = 0

# Función para cargar el número de monedas desde un archivo
def cargar_monedas():
    global monedas
    try:
        with open("monedas.txt", "r") as file:
            monedas = int(file.read())  # Lee el número de monedas
    except FileNotFoundError:
        monedas = 0  # Si no se encuentra el archivo, inicializa las monedas a 0

# Función para guardar el número de monedas en un archivo
def guardar_monedas():
    with open("monedas.txt", "w") as file:
        file.write(str(monedas))  # Escribe el número de monedas en el archivo

# Función para actualizar las monedas y guardarlas
def actualizar_monedas():
    print(f"monedas:{monedas}")  # Muestra el número de monedas en la consola
    guardar_monedas()  # Guarda las monedas en el archivo

# Función que incrementa las monedas al "comer fruta"
def comer_fruta():
    global monedas
    monedas += 1  # Aumenta el número de monedas
    actualizar_monedas()  # Actualiza y guarda las monedas

# Función para cargar el skin actual desde un archivo
def cargar_skin_actual():
    global skin_actual
    try:
        with open("skin_actual.txt", "r") as file:
            skin_actual = file.read().strip()  # Lee el skin y lo limpia de espacios
    except FileNotFoundError:
        skin_actual = "green"  # Si no se encuentra el archivo, se usa el skin por defecto "green"

# Función principal del juego
def gameLoop(window):
    pygame.init()  # Inicializa pygame
    pygame.mixer.init()  # Inicializa el mezclador de audio

    # Definición de colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    colors = [GREEN, BLUE]  # Lista de colores disponibles para los jugadores

    # Configura la ventana del juego para pantalla completa
    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    pygame.display.set_caption('Snake Game Multiplayer')  # Título de la ventana

    clock = pygame.time.Clock()  # Reloj para controlar la tasa de refresco
    BLOCK_SIZE = 30  # Tamaño de los bloques (serpiente, comida, obstáculos)

    # Fuentes para mostrar textos en pantalla
    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)
    moneda_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)

    # Función para mostrar mensajes en pantalla
    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    # Función para dibujar la serpiente
    def draw_snake(block_size, snake_list, skin_color):
        for x in snake_list:
            pygame.draw.rect(game_display, skin_color, [x[0], x[1], block_size, block_size])

    # Función para generar la comida en una posición aleatoria
    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    # Función para verificar colisiones entre dos objetos (rectángulos)
    def check_collision(pos1, pos2, size=BLOCK_SIZE):
        rect1_x, rect1_y = pos1
        rect2_x, rect2_y = pos2
        return (
            rect1_x < rect2_x + size and
            rect1_x + size > rect2_x and
            rect1_y < rect2_y + size and
            rect1_y + size > rect2_y
        )

    # Función para simular una vibración de pantalla
    def vibrate_screen():
        offsets = [(-10, 0), (10, 0), (0, -10), (0, 10)]  # Movimientos aleatorios para la vibración
        original = game_display.copy()  # Guarda una copia de la pantalla
        vibration_duration = random.uniform(0.3, 0.7)  # Duración de la vibración
        vibration_start = time.time()  # Marca el inicio de la vibración
        while time.time() - vibration_start < vibration_duration:
            for dx, dy in offsets:
                game_display.blit(original, (dx, dy))  # Dibuja la copia desplazada
                pygame.display.update()
                pygame.time.wait(50)
                game_display.blit(original, (0, 0))  # Vuelve a dibujar la pantalla original
                pygame.display.update()

    # Función que se llama cuando el jugador pierde
    def end_game(winner):
        pygame.mixer.music.stop()  # Detiene la música
        game_display.fill(BLACK)  # Rellena la pantalla de negro
        message(f"¡HA GANADO JUGADOR {winner}!", YELLOW, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 5)  # Muestra mensaje de victoria
        message("Para reiniciar presiona C", YELLOW, SCREEN_WIDTH / 2.8, SCREEN_HEIGHT / 2)
        message("Para salir presiona Q", YELLOW, SCREEN_WIDTH / 2.8, SCREEN_HEIGHT / 2 + 40)
        pygame.display.update()

        while True:  # Bucle para esperar que el jugador elija qué hacer
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()  # Cierra el juego
                        window.deiconify()
                        return
                    if event.key == pygame.K_c:
                        pygame.mixer.music.play(loops=-1)  # Reanuda la música al reiniciar
                        gameLoop(window)

    cargar_monedas()  # Carga las monedas al inicio del juego
    cargar_skin_actual()  # Carga el skin del jugador

    # Datos de los jugadores (en este caso, 2 jugadores)
    players = [
        {
            "x": SCREEN_WIDTH / 4,
            "y": SCREEN_HEIGHT / 2,
            "x_change": 0,
            "y_change": 0,
            "snake_list": [],
            "snake_length": 1,
            "score": 0,
            "color": colors[0],
            "current_direction": None
        },
        {
            "x": (SCREEN_WIDTH / 4) * 3,
            "y": SCREEN_HEIGHT / 2,
            "x_change": 0,
            "y_change": 0,
            "snake_list": [],
            "snake_length": 1,
            "score": 0,
            "color": colors[1],
            "current_direction": None
        }
    ]

    # Inicializa la comida y obstáculos
    food_positions = [generate_food()]
    obstacle_positions = []
    obstacle_directions = []
    obstacle_tick = 0

    game_over = False  # Variable para controlar el fin del juego

    while not game_over:  # Bucle principal del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                keys = [
                    (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s),  # Teclas para jugador 1
                    (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)  # Teclas para jugador 2
                ]
                for i, (left, right, up, down) in enumerate(keys):
                    if event.key == left and players[i]["current_direction"] != "RIGHT":
                        players[i]["x_change"] = -BLOCK_SIZE
                        players[i]["y_change"] = 0
                        players[i]["current_direction"] = "LEFT"
                    elif event.key == right and players[i]["current_direction"] != "LEFT":
                        players[i]["x_change"] = BLOCK_SIZE
                        players[i]["y_change"] = 0
                        players[i]["current_direction"] = "RIGHT"
                    elif event.key == up and players[i]["current_direction"] != "DOWN":
                        players[i]["y_change"] = -BLOCK_SIZE
                        players[i]["x_change"] = 0
                        players[i]["current_direction"] = "UP"
                    elif event.key == down and players[i]["current_direction"] != "UP":
                        players[i]["y_change"] = BLOCK_SIZE
                        players[i]["x_change"] = 0
                        players[i]["current_direction"] = "DOWN"

        game_display.fill(BLACK)  # Rellena la pantalla de negro

        # Movimiento de los jugadores
        for player in players:
            player["x"] += player["x_change"]
            player["y"] += player["y_change"]

            # Verifica si el jugador se salió de la pantalla
            if (
                player["x"] >= SCREEN_WIDTH or player["x"] < 0 or
                player["y"] >= SCREEN_HEIGHT or player["y"] < 0
            ):
                # Si un jugador sale de la pantalla, el otro jugador gana
                winner = 1 if players[1]["score"] > players[0]["score"] else 2
                end_game(winner)  # Termina el juego
                return

            # Actualiza la serpiente
            snake_head = [player["x"], player["y"]]
            player["snake_list"].append(snake_head)
            if len(player["snake_list"]) > player["snake_length"]:
                del player["snake_list"][0]

            # Verifica colisiones con el cuerpo de la serpiente
            for segment in player["snake_list"][:-1]:
                if check_collision(segment, snake_head):
                    # Si el jugador colide con su propio cuerpo, el otro jugador gana
                    winner = 1 if players[1]["score"] > players[0]["score"] else 2
                    end_game(winner)  # Termina el juego
                    return

            draw_snake(BLOCK_SIZE, player["snake_list"], player["color"])  # Dibuja la serpiente

        # Comprobación de colisión entre jugadores
        for i, player in enumerate(players):
            for j, other_player in enumerate(players):
                if i != j:  # No comprobar colisión consigo mismo
                    for segment in other_player["snake_list"]:
                        if check_collision((player["x"], player["y"]), segment):
                            # Si un jugador colide con otro, el otro jugador gana
                            winner = 1 if players[1]["score"] > players[0]["score"] else 2
                            end_game(winner)  # Termina el juego
                            return

        # Dibujar comida
        for foodx, foody in food_positions:
            pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # Dibujar y mover obstáculos
        obstacle_tick += 1
        if obstacle_tick >= 2:  # Movimiento de obstáculos cada dos ciclos
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

        for obsx, obsy in obstacle_positions:
            pygame.draw.rect(game_display, RED, [obsx, obsy, BLOCK_SIZE, BLOCK_SIZE])  # Dibuja los obstáculos

        # Colisión con comida
        for player in players:
            for foodx, foody in food_positions[:]:
                if check_collision((player["x"], player["y"]), (foodx, foody)):
                    food_positions.remove((foodx, foody))  # Elimina la comida
                    vibrate_screen()  # Realiza una vibración en la pantalla
                    player["snake_length"] += 1  # Aumenta el tamaño de la serpiente
                    player["score"] += 1  # Aumenta la puntuación
                    food_positions.append(generate_food())  # Genera nueva comida

                    # Genera nuevos obstáculos
                    new_obstacles = random.randint(1, 3)
                    for _ in range(new_obstacles):
                        obstacle_positions.append(generate_food())
                        obstacle_directions.append(random.choice(["HORIZONTAL", "VERTICAL"]))

        # Colisión con obstáculos
        for player in players:
            for obsx, obsy in obstacle_positions:
                if check_collision((player["x"], player["y"]), (obsx, obsy)):
                    # Si un jugador choca con un obstáculo, el otro jugador gana
                    winner = 1 if players[1]["score"] > players[0]["score"] else 2
                    end_game(winner)  # Termina el juego
                    return

        # Dibujar puntuación de los jugadores
        for i, player in enumerate(players):
            score_text = score_font.render(f"P{i + 1}: {player['score']}", True, player["color"])
            game_display.blit(score_text, [10, 10 + i * 40])

        pygame.display.update()  # Actualiza la pantalla
        clock.tick(15)  # Controla la tasa de refresco

    pygame.quit()  # Cierra pygame
    quit()

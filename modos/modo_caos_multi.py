import pygame
import random
import time

monedas = 0

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
    print(f"monedas:{monedas}")
    guardar_monedas()

def comer_fruta():
    global monedas
    monedas += 1
    actualizar_monedas()

def cargar_skin_actual():
    global skin_actual
    try:
        with open("skin_actual.txt", "r") as file:
            skin_actual = file.read().strip()
    except FileNotFoundError:
        skin_actual = "green"

def gameLoop(window):
    pygame.init()
    pygame.mixer.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    colors = [GREEN, BLUE]

    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    pygame.display.set_caption('Snake Game Multiplayer')

    clock = pygame.time.Clock()
    BLOCK_SIZE = 30

    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)
    moneda_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)

    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    def draw_snake(block_size, snake_list, skin_color):
        for x in snake_list:
            pygame.draw.rect(game_display, skin_color, [x[0], x[1], block_size, block_size])

    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    def check_collision(pos1, pos2, size=BLOCK_SIZE):
        rect1_x, rect1_y = pos1
        rect2_x, rect2_y = pos2
        return (
            rect1_x < rect2_x + size and
            rect1_x + size > rect2_x and
            rect1_y < rect2_y + size and
            rect1_y + size > rect2_y
        )

    def vibrate_screen():
        offsets = [(-10, 0), (10, 0), (0, -10), (0, 10)]
        original = game_display.copy()
        vibration_duration = random.uniform(0.3, 0.7)
        vibration_start = time.time()
        while time.time() - vibration_start < vibration_duration:
            for dx, dy in offsets:
                game_display.blit(original, (dx, dy))
                pygame.display.update()
                pygame.time.wait(50)
                game_display.blit(original, (0, 0))
                pygame.display.update()

    def end_game(player_score):
        pygame.mixer.music.stop()
        game_display.fill(BLACK)
        message("¡HAS PERDIDO!", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 5)
        message(f"PUNTUACION: {player_score} PTS", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5)
        message("C (INICIAR) / Q (SALIR)", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        window.deiconify()
                        return
                    if event.key == pygame.K_c:
                        pygame.mixer.music.play(loops=-1)  # Reanudar la música al reiniciar
                        gameLoop(window)

    cargar_monedas()
    cargar_skin_actual()

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

    food_positions = [generate_food()]
    obstacle_positions = []
    obstacle_directions = []
    obstacle_tick = 0

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                keys = [
                    (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s),
                    (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
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

        game_display.fill(BLACK)

        for player in players:
            player["x"] += player["x_change"]
            player["y"] += player["y_change"]

            if (
                player["x"] >= SCREEN_WIDTH or player["x"] < 0 or
                player["y"] >= SCREEN_HEIGHT or player["y"] < 0
            ):
                end_game(player["score"])
                return

            snake_head = [player["x"], player["y"]]
            player["snake_list"].append(snake_head)
            if len(player["snake_list"]) > player["snake_length"]:
                del player["snake_list"][0]

            for segment in player["snake_list"][:-1]:
                if check_collision(segment, snake_head):
                    end_game(player["score"])
                    return

            draw_snake(BLOCK_SIZE, player["snake_list"], player["color"])
        # Comprobación de colisión entre jugadores
        for i, player in enumerate(players):
            for j, other_player in enumerate(players):
                if i != j:  # No comprobar colisión consigo mismo
                    for segment in other_player["snake_list"]:
                        if check_collision((player["x"], player["y"]), segment):
                            end_game(player["score"])
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
            pygame.draw.rect(game_display, RED, [obsx, obsy, BLOCK_SIZE, BLOCK_SIZE])

        # Colisión con comida
        for player in players:
            for foodx, foody in food_positions[:]:
                if check_collision((player["x"], player["y"]), (foodx, foody)):
                    food_positions.remove((foodx, foody))
                    vibrate_screen()
                    player["snake_length"] += 1
                    player["score"] += 1
                    food_positions.append(generate_food())

                    # Generar nuevos obstáculos
                    new_obstacles = random.randint(1, 3)
                    for _ in range(new_obstacles):
                        obstacle_positions.append(generate_food())
                        obstacle_directions.append(random.choice(["HORIZONTAL", "VERTICAL"]))

        # Colisión con obstáculos
        for player in players:
            for obsx, obsy in obstacle_positions:
                if check_collision((player["x"], player["y"]), (obsx, obsy)):
                    end_game(player["score"])
                    return

        # Dibujar puntuación
        for i, player in enumerate(players):
            score_text = score_font.render(f"P{i + 1}: {player['score']}", True, player["color"])
            game_display.blit(score_text, [10, 10 + i * 40])

        # Actualizar pantalla
        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()

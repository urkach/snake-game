import pygame
import random
import time

def gameLoop(window):
    pygame.init()
    pygame.mixer.init()

    # Colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    # Configuración de pantalla
    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    pygame.display.set_caption('Snake Game Multiplayer')

    clock = pygame.time.Clock()
    BLOCK_SIZE = 30

    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)

    # Función para mostrar mensajes
    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    # Dibujar serpiente
    def draw_snake(block_size, snake_list, color):
        for x in snake_list:
            pygame.draw.rect(game_display, color, [x[0], x[1], block_size, block_size])

    # Generar comida en posiciones aleatorias
    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    # Verificar colisiones exactas
    def check_collision(pos1, pos2, size=BLOCK_SIZE):
        return (
            pos1[0] < pos2[0] + size and
            pos1[0] + size > pos2[0] and
            pos1[1] < pos2[1] + size and
            pos1[1] + size > pos2[1]
        )

    # Vibrar pantalla
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

    # Variables iniciales
    game_over = False
    game_close = False

    # Configuración inicial para dos jugadores
    players = [
        {
            "color": GREEN,
            "x": SCREEN_WIDTH / 4,
            "y": SCREEN_HEIGHT / 2,
            "x_change": 0,
            "y_change": 0,
            "snake_list": [[SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2]],
            "snake_length": 1,
            "score": 0,
            "direction": None,
            "controls": {
                "UP": pygame.K_w,
                "DOWN": pygame.K_s,
                "LEFT": pygame.K_a,
                "RIGHT": pygame.K_d
            }
        },
        {
            "color": BLUE,
            "x": (3 * SCREEN_WIDTH) / 4,
            "y": SCREEN_HEIGHT / 2,
            "x_change": 0,
            "y_change": 0,
            "snake_list": [[(3 * SCREEN_WIDTH) / 4, SCREEN_HEIGHT / 2]],
            "snake_length": 1,
            "score": 0,
            "direction": None,
            "controls": {
                "UP": pygame.K_UP,
                "DOWN": pygame.K_DOWN,
                "LEFT": pygame.K_LEFT,
                "RIGHT": pygame.K_RIGHT
            }
        }
    ]

    # Comida y obstáculos
    food_positions = [generate_food()]
    obstacle_positions = []
    obstacle_directions = []
    obstacle_tick = 0

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()  # Detén la música al perder
            game_display.fill(BLACK)
            message("¡FIN DEL JUEGO!", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 4)
            for i, player in enumerate(players):
                message(f"PLAYER {i + 1}: {player['score']} PTS", player["color"], SCREEN_WIDTH / 2.85,
                        SCREEN_HEIGHT / 2.5 + i * 40)
            message("C (INICIAR) / Q (SALIR)", RED,  SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)
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
                        pygame.mixer.music.play(loops=-1)  # Reanuda la música al reiniciar
                        gameLoop(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                for player in players:
                    controls = player["controls"]
                    if event.key == controls["LEFT"] and player["direction"] != "RIGHT":
                        player["x_change"] = -BLOCK_SIZE
                        player["y_change"] = 0
                        player["direction"] = "LEFT"
                    elif event.key == controls["RIGHT"] and player["direction"] != "LEFT":
                        player["x_change"] = BLOCK_SIZE
                        player["y_change"] = 0
                        player["direction"] = "RIGHT"
                    elif event.key == controls["UP"] and player["direction"] != "DOWN":
                        player["y_change"] = -BLOCK_SIZE
                        player["x_change"] = 0
                        player["direction"] = "UP"
                    elif event.key == controls["DOWN"] and player["direction"] != "UP":
                        player["y_change"] = BLOCK_SIZE
                        player["x_change"] = 0
                        player["direction"] = "DOWN"

        game_display.fill(BLACK)

        # Dibujar comida y obstáculos
        for foodx, foody in food_positions:
            pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        for obsx, obsy in obstacle_positions:
            pygame.draw.rect(game_display, RED, [obsx, obsy, BLOCK_SIZE, BLOCK_SIZE])

        # Movimiento y lógica para cada jugador
        for player in players:
            player["x"] += player["x_change"]
            player["y"] += player["y_change"]

            if player["x"] >= SCREEN_WIDTH or player["x"] < 0 or player["y"] >= SCREEN_HEIGHT or player["y"] < 0:
                game_close = True

            snake_head = [player["x"], player["y"]]
            player["snake_list"].append(snake_head)

            if len(player["snake_list"]) > player["snake_length"]:
                del player["snake_list"][0]

            for segment in player["snake_list"][:-1]:
                if check_collision(segment, snake_head):
                    game_close = True

            draw_snake(BLOCK_SIZE, player["snake_list"], player["color"])

            for foodx, foody in food_positions[:]:
                if check_collision((player["x"], player["y"]), (foodx, foody)):
                    food_positions.remove((foodx, foody))
                    vibrate_screen()
                    player["snake_length"] += 1
                    player["score"] += 1
                    food_positions.append(generate_food())

                    # Generar un obstáculo cada vez que un jugador coma comida
                    if len(obstacle_positions) < 5:  # Limitar el número de obstáculos en pantalla
                        obstacle_positions.append(generate_food())
                        obstacle_directions.append(random.choice(["HORIZONTAL", "VERTICAL"]))

        # Mover obstáculos a mitad de velocidad
        obstacle_tick += 1
        if obstacle_tick >= 2:  # Controlamos la velocidad de movimiento de los obstáculos
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

        # Colisión con obstáculos
        for obsx, obsy in obstacle_positions:
            for player in players:
                if check_collision((player["x"], player["y"]), (obsx, obsy)):
                    game_close = True

        # Mostrar puntuación
        for i, player in enumerate(players):
            score_text = score_font.render(f"PLAYER {i + 1}: {player['score']}", True, WHITE)
            game_display.blit(score_text, [10, 40 * i])

        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()

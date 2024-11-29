import pygame
import random
import time

def gameLoop(window):
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()
    BLOCK_SIZE = 30

    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)

    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    def draw_snake(block_size, snake_list):
        for x in snake_list:
            pygame.draw.rect(game_display, GREEN, [x[0], x[1], block_size, block_size])

    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    # Nueva función para verificar colisiones exactas
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

    # Modificar la función de vibración
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

    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_length = 1
    snake_list = [[x1, y1]]

    score = 0
    current_direction = None  

    food_positions = [generate_food()]  # Lista inicial de bloques de comida
    obstacle_positions = []  # Lista de posiciones de obstáculos
    obstacle_directions = []  # Lista de direcciones para cada obstáculo
    obstacle_tick = 0  # Contador para reducir la velocidad de movimiento de los obstáculos

    while not game_over:
        while game_close:
            game_display.fill(BLACK)
            message("¡HAS PERDIDO!", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5)
            message(f"PUNTUACION:: {score}", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5)
            message("C (INICIAR) / Q (SALIR)", RED, SCREEN_WIDTH / 2.85, SCREEN_HEIGHT / 1.75)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        window.deiconify()  
                        return
                    if event.key == pygame.K_c:
                        gameLoop(window)

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

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        game_display.fill(BLACK)

        for foodx, foody in food_positions:
            pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        for obsx, obsy in obstacle_positions:
            pygame.draw.rect(game_display, RED, [obsx, obsy, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Colisión con la propia serpiente
        for segment in snake_list[:-1]:
            if check_collision(segment, snake_head):
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)

        for foodx, foody in food_positions[:]:
            if check_collision((x1, y1), (foodx, foody)):
                food_positions.remove((foodx, foody))
                vibrate_screen()
                snake_length += 1
                score += 1
                food_positions.append(generate_food())
                new_obstacles = random.randint(1, 3)
                for _ in range(new_obstacles):
                    obstacle_positions.append(generate_food())
                    obstacle_directions.append(random.choice(["HORIZONTAL", "VERTICAL"]))

        # Movimiento de obstáculos a mitad de velocidad
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

        # Colisión con obstáculos
        for obsx, obsy in obstacle_positions:
            if check_collision((x1, y1), (obsx, obsy)):
                game_close = True

        score_text = score_font.render("PUNTUACION: " + str(score), True, WHITE)
        game_display.blit(score_text, [10, 10])
        pygame.display.update()

        clock.tick(15)

    pygame.quit()
    quit()

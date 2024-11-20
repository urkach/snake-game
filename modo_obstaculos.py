import pygame
import random

def gameLoop():
    pygame.init()

    # Colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (213, 50, 80)
    YELLOW = (255, 255, 102)

    # Dimensiones de la pantalla
    game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.get_surface()
    SCREEN_WIDTH, SCREEN_HEIGHT = surface.get_width(), surface.get_height()

    pygame.display.set_caption('Snake Game')

    # FPS (frames por segundo)
    clock = pygame.time.Clock()

    # Tamaño de los bloques de la serpiente
    BLOCK_SIZE = 30

    # Tamaño de los obstáculos
    OBSTACLE_SIZE = 40

    # Fuentes
    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)

    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    def draw_snake(block_size, snake_list):
        for x in snake_list:
            pygame.draw.rect(game_display, GREEN, [x[0], x[1], block_size, block_size])

    # Variables del juego
    game_over = False
    game_close = False

    # Coordenadas de la serpiente
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    # Movimiento de la serpiente
    x1_change = 0
    y1_change = 0

    # Lista de la serpiente y su longitud inicial
    snake_length = 1
    snake_list = [[x1, y1]]

    # Puntuación
    score = 0

    # Posición de la fruta
    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    foodx, foody = generate_food()

    # Obstáculos
    obstacles = []

    # Bucle principal del juego
    while not game_over:
        while game_close:
            game_display.fill(BLACK)
            message("Q - Salir || C - Jugar de nuevo", RED, SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Controlar los eventos de teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # Verificar si la serpiente ha chocado con los límites de la pantalla
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        # Movimiento de la serpiente
        x1 += x1_change
        y1 += y1_change
        game_display.fill(BLACK)

        # Dibujar los obstáculos
        for obstacle in obstacles:
            pygame.draw.rect(game_display, RED, [obstacle[0], obstacle[1], OBSTACLE_SIZE, OBSTACLE_SIZE])
            # Verificar colisión con obstáculos
            if obstacle[0] <= x1 < obstacle[0] + OBSTACLE_SIZE and obstacle[1] <= y1 < obstacle[1] + OBSTACLE_SIZE:
                game_close = True

        # Dibujar la fruta
        pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # Actualizar la lista de la serpiente
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Comprobar colisión con el propio cuerpo
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        # Verificar si la serpiente ha comido la fruta
        if x1 - BLOCK_SIZE <= foodx <= x1 + BLOCK_SIZE and y1 - BLOCK_SIZE <= foody <= y1 + BLOCK_SIZE:
            foodx, foody = generate_food()
            snake_length += 1
            score += 10

            # Añadir un nuevo obstáculo
            new_obstacle = [
                round(random.randrange(0, SCREEN_WIDTH - OBSTACLE_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
                round(random.randrange(0, SCREEN_HEIGHT - OBSTACLE_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            ]
            obstacles.append(new_obstacle)

        # Dibujar la puntuación
        score_text = score_font.render("Puntuación: " + str(score), True, WHITE)
        game_display.blit(score_text, [10, 10])
        pygame.display.update()

        # Controlar la velocidad del juego
        clock.tick(15)

    pygame.quit()
    quit()

if __name__ == '__main__':
    gameLoop()

import pygame
import random
import time

# Funciones auxiliares
def gameLoop():
    pygame.init()

    # Colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (213, 50, 80)
    BLUE = (50, 153, 213)
    YELLOW = (255, 255, 102)

    # Dimensiones de la pantalla
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    game_display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    # FPS (frames por segundo)
    clock = pygame.time.Clock()

    # Tamaño de los bloques de la serpiente
    BLOCK_SIZE = 10

    # Fuentes
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)

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
    snake_list = []
    snake_length = 1

    # Puntuación
    score = 0

    # Posición de la fruta
    foodx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    # Power-up de velocidad
    speed_powerupx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    speed_powerupy = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
    speed_active = False
    speed_time = 0

    # Obstáculos (bloques)
    obstacles = [(200, 150), (300, 250), (400, 100)]  # Pueden ser más

    # Bucle principal del juego
    while not game_over:
        while game_close:
            game_display.fill(BLUE)
            message("You Lost! Press Q-Quit or C-Play Again", RED, SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3)
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

        x1 += x1_change
        y1 += y1_change
        game_display.fill(BLUE)

        # Dibujar los obstáculos
        for obstacle in obstacles:
            pygame.draw.rect(game_display, RED, [obstacle[0], obstacle[1], BLOCK_SIZE, BLOCK_SIZE])

        # Dibujar la fruta
        pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # Dibujar el power-up de velocidad
        pygame.draw.rect(game_display, (255, 0, 255), [speed_powerupx, speed_powerupy, BLOCK_SIZE, BLOCK_SIZE])

        # Actualizar la lista de la serpiente
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Comprobar colisión con el propio cuerpo
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)

        # Verificar si la serpiente ha comido la fruta
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            snake_length += 1
            score += 10

        # Verificar si la serpiente ha comido el power-up de velocidad
        if x1 == speed_powerupx and y1 == speed_powerupy:
            speed_active = True
            speed_time = pygame.time.get_ticks()  # Marcamos el tiempo en el que se activó
            speed_powerupx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            speed_powerupy = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

        # Activar la velocidad extra durante un tiempo
        if speed_active:
            if pygame.time.get_ticks() - speed_time > 5000:  # 5000 ms = 5 segundos
                speed_active = False
            else:
                clock.tick(20)  # Aumento la velocidad del juego
        else:
            clock.tick(15)

        score_text = score_font.render("Score: " + str(score), True, WHITE)
        game_display.blit(score_text, [0, 0])
        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == '__main__':
    gameLoop()

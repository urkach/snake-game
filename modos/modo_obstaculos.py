import pygame
import random


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
    OBSTACLE_SIZE = 40

    font_style = pygame.font.SysFont("Cascadia Code PL, monospace", 25, bold=True)
    score_font = pygame.font.SysFont("Cascadia Code PL, monospace", 35, bold=True)

    def message(msg, color, x, y):
        mesg = font_style.render(msg, True, color)
        game_display.blit(mesg, [x, y])

    def draw_snake(block_size, snake_list):
        for x in snake_list:
            pygame.draw.rect(game_display, GREEN, [x[0], x[1], block_size, block_size])

    game_over = False
    game_close = False

    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_length = 1
    snake_list = [[x1, y1]]

    score = 0

    direction = None  

    def generate_food():
        return (
            round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        )

    foodx, foody = generate_food()
    obstacles = []

    while not game_over:
        while game_close:
            game_display.fill(BLACK)
            message("¡HAS PERDIDO!", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 5)
            message(f"PUNTUACION: {score}", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5)
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

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        game_display.fill(BLACK)

        for obstacle in obstacles:
            pygame.draw.rect(game_display, RED, [obstacle[0], obstacle[1], OBSTACLE_SIZE, OBSTACLE_SIZE])
            if obstacle[0] <= x1 < obstacle[0] + OBSTACLE_SIZE and obstacle[1] <= y1 < obstacle[1] + OBSTACLE_SIZE:
                game_close = True

        pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        if x1 - BLOCK_SIZE <= foodx <= x1 + BLOCK_SIZE and y1 - BLOCK_SIZE <= foody <= y1 + BLOCK_SIZE:
            foodx, foody = generate_food()
            snake_length += 1
            score += 1

            new_obstacle = [
                round(random.randrange(0, SCREEN_WIDTH - OBSTACLE_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
                round(random.randrange(0, SCREEN_HEIGHT - OBSTACLE_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
            ]
            obstacles.append(new_obstacle)

        score_text = score_font.render("PUNTUACION: " + str(score), True, WHITE)
        game_display.blit(score_text, [10, 10])
        pygame.display.update()

        clock.tick(15)

    pygame.quit()
    quit()

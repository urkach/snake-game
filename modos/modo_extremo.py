import pygame
import random
import rotatescreen

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

    # Inicializar rotatescreen
    screen = rotatescreen.get_primary_display()

    def vibrate_screen():
        if screen:
            screen.rotate_to(90)
            screen.rotate_to(270)
            screen.rotate_to(0)

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

    food_positions = [generate_food()]  # Lista inicial de bloques de comida

    while not game_over:
        while game_close:
            game_display.fill(BLACK)
            message("¡HAS PERDIDO!", RED, SCREEN_HEIGHT / 1.25, SCREEN_HEIGHT / 5.5)
            message(f"Tu puntuación ha sido: {score}", RED, SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5)
            message("Pulsa C para iniciar otra partida o Q para salir al menu principal.", RED, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 1.5)
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

        for foodx, foody in food_positions:
            pygame.draw.rect(game_display, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)

        for foodx, foody in food_positions[:]:
            if x1 == foodx and y1 == foody:
                food_positions.remove((foodx, foody))
                vibrate_screen()
                snake_length += 1
                score += 1
                new_blocks = random.randint(1, 3)
                for _ in range(new_blocks):
                    food_positions.append(generate_food())

        if len(snake_list) > 2:  # Reducción de la serpiente
            reduction_rate = max(1, score // 10)  # Incrementa la reducción según la puntuación
            if len(snake_list) > snake_length - reduction_rate:
                del snake_list[0]

        score_text = score_font.render("Puntuación: " + str(score), True, WHITE)
        game_display.blit(score_text, [10, 10])
        pygame.display.update()

        clock.tick(15)

    pygame.quit()
    quit()

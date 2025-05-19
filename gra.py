import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
grey = (128, 128, 128)

display_width = 1200
display_height = 600

block_size = 20

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake - Pygame')
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

apple_img = pygame.image.load("C:/Users/48660/Desktop/apple.png")
apple_img = pygame.transform.scale(apple_img, (block_size + 10, block_size + 10))

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    rect = mesg.get_rect(center=(display_width / 2, display_height / 3 + y_offset))
    screen.blit(mesg, rect)

def score_display(score):
    value = score_font.render("Wynik: " + str(score), True, black)
    screen.blit(value, [0, 0])

def draw_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], block, block])

def generate_walls(count, avoid_positions):
    walls = []
    while len(walls) < count:
        x = random.randint(1, (display_width // block_size) - 2) * block_size
        y = random.randint(1, (display_height // block_size) - 2) * block_size
        if (x, y) not in avoid_positions and (x, y) not in walls:
            walls.append((x, y))
    return walls

def difficulty_selection():
    selecting = True
    while selecting:
        screen.fill(blue)
        message("Wybierz poziom trudności:", white, -60)
        message("1 - Łatwy", white, 0)
        message("2 - Średni", white, 40)
        message("3 - Trudny", white, 80)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "łatwy"
                elif event.key == pygame.K_2:
                    return "średni"
                elif event.key == pygame.K_3:
                    return "trudny"

def game_loop(difficulty):
    if difficulty == "łatwy":
        snake_speed = 13
    elif difficulty == "średni":
        snake_speed = 13
    elif difficulty == "trudny":
        snake_speed = 18
    else:
        snake_speed = 13
    
    game_over = False
    game_close = False

    x = display_width / 2
    y = display_height / 2

    x_change = 0
    y_change = 0

    snake_list = []
    length = 1

    food_x = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0

    walls = []
    if difficulty == 'średni':
        walls = generate_walls(20, [(food_x, food_y)])
    elif difficulty == 'trudny':
        walls = generate_walls(30, [(food_x, food_y)])

    while not game_over:

        while game_close:
            screen.fill(blue)
            message("Przegrałeś! Naciśnij C aby grać dalej, Q aby wyjść", red)
            score_display(length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop(difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = block_size
                    x_change = 0

        if x >= display_width or x < 0 or y >= display_height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(blue)

        screen.blit(apple_img, (food_x, food_y))

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(block_size, snake_list)
        score_display(length - 1)

        for wall in walls:
            pygame.draw.rect(screen, grey, [wall[0], wall[1], block_size, block_size])

        if x in range(int(food_x), int(food_x) + block_size + 10) and y in range(int(food_y), int(food_y) + block_size + 10):
            food_x = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0
            length += 1

        if (x, y) in walls:
            game_close = True

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

def main():
    difficulty = difficulty_selection()
    game_loop(difficulty)

if __name__ == "__main__":
    main()

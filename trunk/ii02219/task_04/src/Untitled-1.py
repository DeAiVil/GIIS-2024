import pygame
import random
import sys
import os

pygame.init()
game_over_flag = False

WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

background_image = pygame.image.load('C:/Users/dende/Desktop/task_04_05/clouds.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

dino_width, dino_height = 145, 145  
dino_x, dino_y = 40, HEIGHT - dino_height - 40  
dino_dy = 0
gravity = 0.8
is_jumping = False

obstacle_width, obstacle_height = 100, 100
obstacle_x, obstacle_y = WIDTH, HEIGHT - obstacle_height - 30
obstacle_speed = 5.5 

obstacle_images = []

obstacle_images_folder = 'C:/Users/dende/Desktop/task_04_05/enemy_images'

for filename in os.listdir(obstacle_images_folder):
    image_path = os.path.join(obstacle_images_folder, filename)
    image = pygame.image.load(image_path)
    scaled_image = pygame.transform.scale(image, (obstacle_width, obstacle_height))
    obstacle_images.append(scaled_image)

score = 0
num_skin =0

font = pygame.font.SysFont(None, 30)
pygame.mixer.music.load('C:/Users/dende/Desktop/task_04_05/Yoari - TRUE.mp3')
pygame.mixer.music.play(-1)   
capybara_images_folder = 'C:/Users/dende/Desktop/task_04_05/capybara_images'
target_size = (145, 145)  
capybara_images = []
for filename in os.listdir(capybara_images_folder):
    image_path = os.path.join(capybara_images_folder, filename)
    image = pygame.image.load(image_path)
    scaled_image = pygame.transform.scale(image, target_size)
    capybara_images.append(scaled_image)

current_capybara_image = capybara_images[0]

def draw_capybara():
    win.blit(current_capybara_image, (dino_x, dino_y))

def draw_obstacle():
    global obstacle_images
    obstacle_image = obstacle_images[score%2]
    obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))
    win.blit(obstacle_image, (obstacle_x, obstacle_y))

def update():
    global dino_y, dino_dy, is_jumping, obstacle_x, score

    win.blit(background_image, (0, 0))
 
    dino_y += dino_dy
    dino_dy += gravity

   
    if dino_y > HEIGHT - dino_height - 30:
        dino_y = HEIGHT - dino_height - 30
        dino_dy = 0
        is_jumping = False

    obstacle_x -= obstacle_speed
    
    if obstacle_x + obstacle_width < 0:
        global current_capybara_image
        obstacle_x = WIDTH
        score += 1
        num_skin=score%4
        current_capybara_image=capybara_images[num_skin]

    if (dino_x + dino_width - 50 > obstacle_x and
    dino_y < obstacle_y + obstacle_height and
    dino_y + dino_height - 60 > obstacle_y):
    game_over() # type: ignore

    draw_capybara()
    draw_obstacle()
    text = font.render("Score: " + str(score), True, BLACK)
    win.blit(text, (10, 10))
    pygame.display.update()

def jump():
    global is_jumping, dino_dy
    if not is_jumping:
        dino_dy = -15
        is_jumping = True

def game_over():
    global game_over_flag
    pygame.mixer.music.stop()
    game_over_flag = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if game_over_flag:
                        pygame.mixer.music.play(-1)
                        reset_game()
                        game_over_flag = False
                    else:
                        jump()

        if game_over_flag:
            game_over_text = font.render("Game Over! Press SPACE to restart.", True, BLACK)
            win.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
            pygame.display.update()
            continue

        update()
        clock.tick(30)

def reset_game():
    global dino_y, dino_dy, is_jumping, obstacle_x, score
    dino_y, dino_dy, is_jumping = 0, 0, False
   
    obstacle_x, score = WIDTH, 0

global clock
clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump()

    update()
    clock.tick(30)



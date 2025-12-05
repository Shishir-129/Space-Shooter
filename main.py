import pygame
import random
import math
from pygame import mixer

# Initializing the game
pygame.init()

# Screen dimensions
screen_width = 700
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and icon
pygame.display.set_caption("Cosmic Crusaders")
icon = pygame.image.load("PYGAME_PROJECT/spaceship_icon.png")
pygame.display.set_icon(icon)

# Fonts
title_font = pygame.font.Font("freesansbold.ttf", 70)
button_font = pygame.font.Font("freesansbold.ttf", 30)
font = pygame.font.Font("freesansbold.ttf", 30)
game_over_font = pygame.font.Font("freesansbold.ttf", 70)

# Levels
current_level = 1

# Homepage
def render_text_centered(text, font, color, y):
    render = font.render(text, True, color)
    x = (screen_width - render.get_width()) // 2
    screen.blit(render, (x, y))

def render_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_render = button_font.render(text, True, text_color)
    text_x = x + (width - text_render.get_width()) // 2
    text_y = y + (height - text_render.get_height()) // 2
    screen.blit(text_render, (text_x, text_y))
    return pygame.Rect(x, y, width, height)

def homepage():
    global current_level

    # Background for homepage
    background = pygame.image.load("PYGAME_PROJECT/background.jpg")
    
    # Play background music for the homepage
    mixer.music.load("PYGAME_PROJECT/background_sound.wav")
    mixer.music.play(-1)  # Loop the music indefinitely

    # Button click sound effect
    click_sound = mixer.Sound("PYGAME_PROJECT/click_sound.wav")
    
    running = True
    while running:
        screen.fill((10, 10, 40))
        screen.blit(background, (0, 0))
        render_text_centered("Cosmic Crusaders", title_font, (255, 255, 255), 80)
        render_text_centered(f"Level: {current_level}", font, (255, 255, 255), 200)

        start_button = render_button("Start Game", 250, 300, 200, 50, (0, 128, 0), (255, 255, 255))
        quit_button = render_button("Quit", 250, 400, 200, 50, (128, 0, 0), (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    click_sound.play()  # Play click sound
                    return "start_game"
                if quit_button.collidepoint(event.pos):
                    click_sound.play()  # Play click sound
                    return "quit"

        pygame.display.update()

# Gameplay
def gameplay():
    global current_level

    # Background
    background = pygame.image.load("PYGAME_PROJECT/background.jpg")

    # Sound Effects
    mixer.music.load("PYGAME_PROJECT/background_sound.wav")
    mixer.music.play(-1)

    # Player
    playerImg = pygame.image.load("PYGAME_PROJECT/player.png")
    playerX = 310
    playerX_change = 0
    playerY = 500

    def player(x, y):
        screen.blit(playerImg, (x, y))

    # Enemy
    enemyImg = []
    enemyX = []
    enemyX_change = []
    enemyY = []
    enemyY_change = []
    no_of_enemies = 7

    for i in range(no_of_enemies):
        enemyImg.append(pygame.image.load("PYGAME_PROJECT/enemy.png"))
        enemyX.append(random.randint(0, 636))
        enemyX_change.append(0.2)
        enemyY.append(random.randint(40, 250))
        enemyY_change.append(50)

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    # Bullet
    bulletImg = pygame.image.load("PYGAME_PROJECT/bullet.png")
    bulletX = 0
    bulletX_change = 0
    bulletY = playerY
    bulletY_change = 1
    bullet_state = "ready"
    score_value = 0

    def bullet(x, y):
        nonlocal bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 23, y - 25))

    def collision(enemyX, enemyY, bulletX, bulletY):
        d = math.sqrt(pow(enemyX - bulletX, 2) + pow(enemyY - bulletY, 2))
        return d < 27

    def scoring(x, y):
        score = font.render(f"Score : {score_value}", True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_screen():
        restart_button = render_button("Restart", 250, 350, 200, 50, (0, 128, 0), (255, 255, 255))
        quit_button = render_button("Quit", 250, 450, 200, 50, (128, 0, 0), (255, 255, 255))

        while True:
            render_text_centered("Game Over", game_over_font, (255, 255, 255), 200)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        return "restart"
                    if quit_button.collidepoint(event.pos):
                        return "quit"

    is_running = True
    while is_running:
        screen.fill((10, 10, 40))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.5
                if event.key == pygame.K_UP:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound("PYGAME_PROJECT/laser.wav")
                        bullet_sound.play()
                        bulletX = playerX
                        bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX > 636:
            playerX = 636

        for i in range(no_of_enemies):
            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                result = game_over_screen()
                if result == "restart":
                    return "restart"
                elif result == "quit":
                    pygame.quit()
                    exit()

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.35
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] > 636:
                enemyX_change[i] = -0.35
                enemyY[i] += enemyY_change[i]

            if collision(enemyX[i], enemyY[i], bulletX, bulletY):
                collision_sound = mixer.Sound("PYGAME_PROJECT/explode.wav")
                collision_sound.play()
                bulletY = playerY
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 636)
                enemyY[i] = random.randint(40, 250)

            enemy(enemyX[i], enemyY[i], i)

        if bullet_state == "fire":
            bulletY -= bulletY_change
            bullet(bulletX, bulletY)
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        player(playerX, playerY)
        scoring(15, 15)
        pygame.display.update()

# Main Program
while True:
    action = homepage()
    if action == "start_game":
        result = gameplay()
        if result == "restart":
            continue
    elif action == "quit":
        pygame.quit()
        break

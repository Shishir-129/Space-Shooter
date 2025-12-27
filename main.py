import pygame
import random
import math
from pygame import mixer

# Initializing the game
pygame.init()
clock = pygame.time.Clock()

# Screen dimensions
screen_width = 700
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and icon
pygame.display.set_caption("Cosmic Crusaders")
icon = pygame.image.load("spaceship_icon.png")
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

    background = pygame.image.load("background.jpg")
    mixer.music.load("background_sound.wav")
    mixer.music.play(-1)
    click_sound = mixer.Sound("click_sound.wav")

    while True:
        screen.fill((10, 10, 40))
        screen.blit(background, (0, 0))

        render_text_centered("Cosmic Crusaders", title_font, (255, 255, 255), 80)
        render_text_centered(f"Level: {current_level}", font, (255, 255, 255), 200)

        start_button = render_button("Start Game", 250, 300, 200, 50, (0, 128, 0), (255, 255, 255))
        quit_button = render_button("Quit", 250, 400, 200, 50, (128, 0, 0), (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    click_sound.play()
                    return "start_game"
                if quit_button.collidepoint(event.pos):
                    click_sound.play()
                    return "quit"

        pygame.display.update()
        clock.tick(60)

# Gameplay
def gameplay():
    global current_level

    background = pygame.image.load("background.jpg")
    mixer.music.load("background_sound.wav")
    mixer.music.play(-1)

    playerImg = pygame.image.load("player.png")
    playerX = 310
    playerX_change = 0
    playerY = 500

    def player(x, y):
        screen.blit(playerImg, (x, y))

    enemyImg = []
    enemyX = []
    enemyX_change = []
    enemyY = []
    enemyY_change = []
    no_of_enemies = 7

    for i in range(no_of_enemies):
        enemyImg.append(pygame.image.load("enemy.png"))
        enemyX.append(random.randint(0, 636))
        enemyX_change.append(0.8)  # Increased from 0.2 to 0.8
        enemyY.append(random.randint(40, 250))
        enemyY_change.append(50)

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    bulletImg = pygame.image.load("bullet.png")
    bulletX = 0
    bulletY = playerY
    bulletY_change = 5  # Changed from 1 to 5 for faster bullet movement
    bullet_state = "ready"
    score_value = 0

    def bullet(x, y):
        nonlocal bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 23, y - 25))

    def collision(enemyX, enemyY, bulletX, bulletY):
        return math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2) < 27

    def scoring(x, y):
        score = font.render(f"Score : {score_value}", True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_screen():
        while True:
            screen.fill((10, 10, 40))

            restart_button = render_button("Restart", 250, 350, 200, 50, (0, 128, 0), (255, 255, 255))
            quit_button = render_button("Quit", 250, 450, 200, 50, (128, 0, 0), (255, 255, 255))
            render_text_centered("Game Over", game_over_font, (255, 255, 255), 200)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        return "restart"
                    if quit_button.collidepoint(event.pos):
                        return "quit"

            pygame.display.update()
            clock.tick(60)

    while True:
        screen.fill((10, 10, 40))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -1.5  # Increased from -0.5 to -1.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 1.5  # Increased from 0.5 to 1.5
                if event.key == pygame.K_UP and bullet_state == "ready":
                    mixer.Sound("laser.wav").play()
                    bulletX = playerX
                    # Don't call bullet() here, just set the state
                    bullet_state = "fire"

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    playerX_change = 0

        playerX += playerX_change
        playerX = max(0, min(playerX, 636))

        for i in range(no_of_enemies):
            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                mixer.music.stop()  # Stop music before game over
                return game_over_screen()

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= 636:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]

            if collision(enemyX[i], enemyY[i], bulletX, bulletY):
                mixer.Sound("explode.wav").play()
                bulletY = playerY
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 636)
                enemyY[i] = random.randint(40, 250)

            enemy(enemyX[i], enemyY[i], i)

        if bullet_state == "fire":
            bulletY -= bulletY_change  # Now moves faster upward
            bullet(bulletX, bulletY)
            if bulletY <= 0:
                bulletY = playerY
                bullet_state = "ready"

        player(playerX, playerY)
        scoring(15, 15)

        pygame.display.update()
        clock.tick(60)

# Main Program
while True:
    action = homepage()
    if action == "start_game":
        result = gameplay()
        if result == "quit":
            pygame.quit()
            break
    elif action == "quit":
        pygame.quit()
        break

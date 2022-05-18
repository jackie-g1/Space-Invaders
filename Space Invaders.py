import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
# 800 is width, 600 is height

# background
# background = pygame.image.load('background.jpg')
background = pygame.image.load("background.jpg").convert_alpha()
background = pygame.transform.smoothscale(background, (800, 600))

# Background sound
mixer.music.load('background_music.mp3')
mixer.music.set_volume(0.25)
mixer.music.play(-1)
# -1 in play makes it loop instead of just playing it once

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.smoothscale(player_img, (64, 64))
player_X = 370
player_Y = 480
player_X_change = 0
player_Y_change = 0

# Enemy
enemy_img = []
enemy_X = []
enemy_Y = []
enemy_X_change = []
enemy_Y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("enemy_2.png"))
    enemy_X.append(random.randint(0, 736))
    enemy_Y.append(random.randint(50, 150))
    enemy_X_change.append(0.1)
    enemy_Y_change.append(40)

# Bullet
# Ready State - Cannot see bullet on screen
# Fire - Bullet is moving
bullet_img = pygame.image.load('bullet.png').convert_alpha()
bullet_img = pygame.transform.smoothscale(bullet_img, (24, 24))
bullet_X = player_X
bullet_Y = player_Y  # change to follow ship
bullet_X_change = 0
bullet_Y_change = 0.4
bullet_state = 'ready'

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_X = 10
text_Y = 10

# Game over text
gameover_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(x, y):
    gameover_text = gameover_font.render("GAMEOVER", True, (255, 255, 255))
    screen.blit(gameover_text, (x, y))

def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 19.5, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 30:
        return True


# Game loop
running = True
while running:
    # in this while loop, the background color will be changed; color will be changed to purple
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # movements to keybinds
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_X_change = -0.3
            if event.key == pygame.K_RIGHT:
                player_X_change = 0.3
            if event.key == pygame.K_UP:
                player_Y_change = -0.2
            if event.key == pygame.K_DOWN:
                player_Y_change = 0.2
            if event.key == pygame.K_SPACE:
                # if there is no bullet currently on the screen
                if bullet_state == 'ready':
                    # Gets the current X coords of the player
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_X = player_X
                    fire_bullet(bullet_X, bullet_Y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_X_change = 0
                player_Y_change = 0

    # Boundaries
    player_X += player_X_change
    player_Y += player_Y_change

    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736
    if player_Y <= 0:
        player_Y = 0
    elif player_Y >= 536:
        player_Y = 536

    # Enemy movements
    for i in range(num_of_enemies):

        # Gameover
        if enemy_Y[i] > player_Y:
            for j in range(num_of_enemies):
                enemy_Y[j] = 2000
            game_over_text(200, 250)
            break

        enemy_X[i] += enemy_X_change[i]
        if enemy_X[i] <= 0:
            enemy_X_change[i] = 0.17
            enemy_Y[i] += enemy_Y_change[i]
        elif enemy_X[i] >= 736:
            enemy_X_change[i] = -0.17
            enemy_Y[i] += enemy_Y_change[i]
        if enemy_Y[i] <= 0:
            enemy_Y[i] = 0
        elif enemy_Y[i] >= 536:
            enemy_Y[i] = 536

        # Collision
        collision = is_collision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if collision:
            bullet_sound = mixer.Sound('explosion.wav')
            bullet_sound.play()
            bullet_Y = player_Y
            bullet_state = 'ready'
            score_value += 1
            enemy_X[i] = random.randint(0, 736)
            enemy_Y[i] = random.randint(50, 150)

        enemy(enemy_X[i], enemy_Y[i], i)

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = player_Y
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_change

    player(player_X, player_Y)

    show_score(text_X, text_Y)
    # this needs to be updated so the code under provides that; whenever we want to update anything, we will have to place the same code everytime we add something new.
    pygame.display.update()

import pygame
import random
import math
from pygame import mixer

pygame.init()
# creating a screen,icon and caption
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# player
playerImg = pygame.image.load("space-invaders.png")
playerImg_x = 370
playerImg_y = 480
playerImg_x_change = 0
# background image and music
background = pygame.image.load("10838001_19333449.jpg")
mixer.music.load('background.wav')
mixer.music.play(-1)

# creating multiple enemies
enemyImg = []
enemyImg_x = []
enemyImg_y = []
enemyImg_x_change = []
enemyImg_y_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load("character.png"))
    enemyImg_x.append(random.randint(0, 735))
    enemyImg_y.append(random.randint(50, 150))
    enemyImg_x_change.append(5)
    enemyImg_y_change.append(20)
# bullet
bulletImg = pygame.image.load("bullet.png")
bulletImg_x = 0
bulletImg_y = 480
bulletImg_x_change = 0
bulletImg_y_change = 15
bullet_state = "ready"
score = 0
# creating font object for text
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


# function to draw the player on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# fuction to draw enemy on the screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# function to fire bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# function to detect collusion
def is_collision(enemyImg_x, enemyImg_y, bulletImg_x, bulletImg_y):
    distance = math.sqrt(math.pow((enemyImg_x - bulletImg_x), 2) + math.pow((enemyImg_y - bulletImg_y), 2))
    if distance < 27:
        return True
    else:
        return False


# function to display score on the screen
def display_score(x, y):
    score_img = font.render("score:" + str(score), True, (64, 224, 208))
    screen.blit(score_img, (x, y))


def game_over():
    game_over_img = game_over_font.render("GAME OVER !!!", True, (255, 255, 255))
    screen.blit(game_over_img, (200, 250))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerImg_x_change = -5
            if event.key == pygame.K_RIGHT:
                playerImg_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletImg_x = playerImg_x
                    fire_bullet(bulletImg_x, bulletImg_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerImg_x_change = 0

    playerImg_x += playerImg_x_change
    if playerImg_x <= 0:
        playerImg_x = 0
    elif playerImg_x >= 736:
        playerImg_x = 736
    for i in range(number_of_enemies):
        if enemyImg_y[i] > 420:
            for j in range(number_of_enemies):
                enemyImg_y[j] = 2000
            game_over()
            break

        enemyImg_x[i] += enemyImg_x_change[i]
        if enemyImg_x[i] <= 0:
            enemyImg_x_change[i] = 2
            enemyImg_y[i] += enemyImg_y_change[i]
        elif enemyImg_x[i] >= 736:
            enemyImg_x_change[i] = -2
            enemyImg_y[i] += enemyImg_y_change[i]

        collision = is_collision(enemyImg_x[i], enemyImg_y[i], bulletImg_x, bulletImg_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletImg_y = 480
            bullet_state = "ready"
            score += 1
            enemyImg_x[i] = random.randint(0, 735)
            enemyImg_y[i] = random.randint(50, 150)
        enemy(enemyImg_x[i], enemyImg_y[i], i)

    if bulletImg_y <= 0:
        bulletImg_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletImg_x, bulletImg_y)
        bulletImg_y -= bulletImg_y_change

    player(playerImg_x, playerImg_y)
    display_score(text_x, text_y)

    pygame.display.update()

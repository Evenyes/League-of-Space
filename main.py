import random
import math
import pygame
from pygame import mixer

# Il faut initialisé pygame sinon bug
pygame.init()

# Creation de la fenetre           w    h
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('img/BackgroundZgame.jpg')

# Background Sounds
mixer.music.load('song/background.mp3')
mixer.music.get_volume()
mixer.music.set_volume(0.05)
mixer.music.play(10)

# Title and Icon
pygame.display.set_caption("League of Space")
icon = pygame.image.load('img/icone.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('img/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_alien = 8
w = 2

for i in range(num_of_alien):
    alienImg.append(pygame.image.load('img/alien.png'))
    alienX.append(random.randint(0, 700))
    alienY.append(random.randint(50, 150))
    alienX_change.append(w)
    alienY_change.append(40)

# Bullet
bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Scores & Life
score_value = 0
life_value = 3
font = pygame.font.Font('font/font.ttf', 32)
scoreX = 10
scoreY = 550
lifeX = 680
lifeY = 550

# game over text
over_font = pygame.font.Font('font/font.ttf', 100)
game_over_statut = "winning"

# Boss
boss_statut = "offline"
bossImg = pygame.image.load('img/demon.png')
boss_hpImg = pygame.image.load('img/hpvide.png')
bossX = 100
bossY = 50
bossX_change = random.randint(5, 10)
bossY_change = 0
boss_hp = 10

boss_bar = []
for i in range(10):
    boss_bar.append(pygame.image.load('img/hpbar.png'))


# Boss Weapon
fireballImg = pygame.image.load('img/fireball.png.png')

def boss(x, y):
    screen.blit(bossImg, (x, y))
    screen.blit(boss_hpImg, (300, 510))

def fireballShot(x, y):
    screen.blit(bulletImg, (x, y))

def bar1(hp):
    if hp >= 10:
        screen.blit(boss_bar[9], (300, 510))
    if hp >= 9:
        screen.blit(boss_bar[8], (317, 510))
    if hp >= 8:
        screen.blit(boss_bar[7], (334, 510))
    if hp >= 7:
        screen.blit(boss_bar[6], (351, 510))
    if hp >= 6:
        screen.blit(boss_bar[5], (369, 510))
    if hp >= 5:
        screen.blit(boss_bar[4], (387, 510))
    if hp >= 4:
        screen.blit(boss_bar[3], (403, 510))
    if hp >= 3:
        screen.blit(boss_bar[2], (420, 510))
    if hp >= 2:
        screen.blit(boss_bar[1], (438, 510))
    if hp >= 1:
        screen.blit(boss_bar[0], (455, 510))


def score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def life(x, y):
    life = font.render("Life :  " + str(life_value), True, (255, 255, 255))
    screen.blit(life, (x, y))


def game_over_text():
    over = over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over, (150, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y - 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    # https://fr.wikihow.com/calculer-la-distance-entre-deux-points
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance <= 27:
        return True
    else:
        return False


def isCollisionBoss(alienX, alienY, bulletX, bulletY):
    alienX += 35
    alienY += 35
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance <= 50:
        return True
    else:
        return False


# Clock
clock = pygame.time.Clock()

# Game Loop
running = True
while running:
    # background color
    # screen.fill((0, 0, 70))

    # background image
    screen.blit(background, (0, 0))
    pygame.draw.line(screen, (0, 255, 255), (0, 460), (800, 460))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Touches/event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('song/laser.wav')
                    bullet_Sound.get_volume()
                    bullet_Sound.set_volume(0.1)
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if score_value >= 2:
        boss_statut = "online"
        w2 = random.randint(5, 10)
        bossX += bossX_change
        if bossX <= 0:
            bossX_change = w2
            bossY += bossY_change
        elif bossX >= 672:
            bossX_change = -w2
            bossY += bossY_change
        boss(bossX, bossY)
        collision2 = isCollisionBoss(bossX, bossY, bulletX, bulletY)
        bar1(boss_hp)
        if boss_statut == "online":

        if collision2:
            bulletY = 480
            bullet_state = "ready"
            boss_hp -= 1
            bullet_Sound = mixer.Sound('song/explosion.mp3')
            bullet_Sound.get_volume()
            bullet_Sound.set_volume(0.01)
            bullet_Sound.play()
            print("toucher")

            # Bordure de la fenetre // le player sort pas des pixel donner
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_alien):
        # game over
        if alienY[i] > 400:
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)
            if life_value >= 1:
                life_value -= 1
            if life_value == 0:
                game_over_statut = "lose"
                for j in range(num_of_alien):
                    alienY[j] = 2000
                game_over_text()
                break
        # Alien bordure
        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = w
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -w
            alienY[i] += alienY_change[i]

            # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            bullet_Sound = mixer.Sound('song/explosion.mp3')
            bullet_Sound.get_volume()
            bullet_Sound.set_volume(0.01)
            bullet_Sound.play()
            if game_over_statut == "winning":
                alienX[i] = random.randint(0, 735)
                alienY[i] = random.randint(50, 150)
        alien(alienX[i], alienY[i], i)

    # bullet deplacement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    life(lifeX, lifeY)
    player(playerX, playerY)
    score(scoreX, scoreY)
    pygame.display.update()
    clock.tick(60)

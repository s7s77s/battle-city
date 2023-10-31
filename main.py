import pygame
import os
import sys
import random

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('battle city')
lvl = "menu"
font = pygame.font.SysFont('aria', 30)

from load import *


def lvlgame():
    sc.fill("black")
    brick_group.update()
    brick_group.draw(sc)
    iron_group.update()
    iron_group.draw(sc)
    water_group.update()
    water_group.draw(sc)
    enemy_group.update()
    enemy_group.draw(sc)
    player_group.update()
    player_group.draw(sc)
    flag_group.update()
    flag_group.draw(sc)
    bullet_player_group.update()
    bullet_player_group.draw(sc)
    bullet_enemy_group.update()
    bullet_enemy_group.draw(sc)
    bush_group.update()
    bush_group.draw(sc)
    pygame.display.update()


def drawMaps(nameFile):
    maps = []
    source = "game lvl/" + str(nameFile)
    with open(source, "r") as file:
        for i in range(0, 20):
            maps.append(file.readline().replace("\n", "").split(",")[0: -1])

    pos = [0, 0]
    for i in range(0, len(maps)):
        pos[1] = i * 40
        for j in range(0, len(maps[0])):
            pos[0] = 40 * j
            if maps[i][j] == '1':
                brick = Brick(brick_image, pos)
                brick_group.add(brick)
            elif maps[i][j] == '2':
                bush = Bush(bush_image, pos)
                bush_group.add(bush)
            elif maps[i][j] == '3':
                iron = Iron(iron_image, pos)
                iron_group.add(iron)
            elif maps[i][j] == '4':
                water = Water(water_image, pos)
                water_group.add(water)
            elif maps[i][j] == '6':
                enemy = Enemy(enemy_image, pos)
                enemy_group.add(enemy)
            elif maps[i][j] == '5':
                flag = Flag(flag_image, pos)
                flag_group.add(flag)


def startMenu():
    sc.fill('grey')
    button_group.draw(sc)
    button_group.update()
    pygame.display.update()


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, next_lvl, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.next_lvl = next_lvl
        self.text = text

    def update(self):
        global lvl
        text_render = font.render(self.text, True, 'white')
        sc.blit(text_render, (self.rect.x + 80, self.rect.y + 5))
        click = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.rect.left < click[0] < self.rect.right and self.rect.top < click[1] < self.rect.bottom:
                lvl = self.next_lvl


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "top":
                player.rect.top = self.rect.bottom
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top
        pygame.sprite.groupcollide(bullet_player_group, brick_group, True, True)
        pygame.sprite.groupcollide(bullet_enemy_group, brick_group, True, True)


class Bush(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Iron(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "top":
                player.rect.top = self.rect.bottom
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top
        pygame.sprite.groupcollide(bullet_player_group, iron_group, True, False)
        pygame.sprite.groupcollide(bullet_enemy_group, iron_group, True, False)


class Water(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "top":
                player.rect.top = self.rect.bottom
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 5
        self.dir = "top"
        self.timer_shoot = 0

    def update(self):
        self.timer_shoot += 1
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.image = pygame.transform.rotate(player_image, 90)
            self.rect.x = self.rect.x - self.speed
            self.dir = "left"
        elif key[pygame.K_d]:
            self.image = pygame.transform.rotate(player_image, 270)
            self.rect.x = self.rect.x + self.speed
            self.dir = "right"
        elif key[pygame.K_w]:
            self.image = pygame.transform.rotate(player_image, 360)
            self.rect.y = self.rect.y - self.speed
            self.dir = "top"
        elif key[pygame.K_s]:
            self.image = pygame.transform.rotate(player_image, 180)
            self.rect.y = self.rect.y + self.speed
            self.dir = "bottom"
        if key[pygame.K_SPACE] and self.timer_shoot / FPS > 1:
            bullet = Bullet_player(player_bullet, self.rect.center, self.dir)
            bullet_player_group.add(bullet)
            self.timer_shoot = 0
        pygame.sprite.groupcollide(bullet_enemy_group, player_group, True, True)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 2
        self.dir = "top"
        self.timer_movie = 0
        self.timer_shoot = 0

    def update(self):
        self.timer_shoot += 1
        self.timer_movie += 1
        if self.timer_movie / FPS > 2:
            if random.randint(1, 4) == 1:
                self.dir = "top"
                self.timer_movie = 0
            elif random.randint(1, 4) == 2:
                self.dir = "bottom"
                self.timer_movie = 0
            elif random.randint(1, 4) == 3:
                self.dir = "left"
                self.timer_movie = 0
            elif random.randint(1, 4) == 4:
                self.dir = "right"
                self.timer_movie = 0

        if self.dir == "top":
            self.image = pygame.transform.rotate(enemy_image, 0)
            self.rect.y = self.rect.y - self.speed
        elif self.dir == "bottom":
            self.image = pygame.transform.rotate(enemy_image, 180)
            self.rect.y = self.rect.y + self.speed
        elif self.dir == "left":
            self.image = pygame.transform.rotate(enemy_image, 90)
            self.rect.x = self.rect.x - self.speed
        elif self.dir == "right":
            self.image = pygame.transform.rotate(enemy_image, 270)
            self.rect.x = self.rect.x + self.speed

        if pygame.sprite.spritecollide(self, brick_group, False):
            self.timer_movie = 0
            if self.dir == "top":
                self.dir = "bottom"
            elif self.dir == "bottom":
                self.dir = "top"
            elif self.dir == "left":
                self.dir = "right"
            elif self.dir == "right":
                self.dir = "left"

        if pygame.sprite.spritecollide(self, water_group, False):
            self.timer_movie = 0
            if self.dir == "top":
                self.dir = "bottom"
            elif self.dir == "bottom":
                self.dir = "top"
            elif self.dir == "left":
                self.dir = "right"
            elif self.dir == "right":
                self.dir = "left"

        if pygame.sprite.spritecollide(self, iron_group, False):
            self.timer_movie = 0
            if self.dir == "top":
                self.dir = "bottom"
            elif self.dir == "bottom":
                self.dir = "top"
            elif self.dir == "left":
                self.dir = "right"
            elif self.dir == "right":
                self.dir = "left"
        if self.timer_shoot / FPS > 1.5:
            bullet_enemy = Bullet_enemy(enemy_bullet, self.rect.center, self.dir)
            bullet_enemy_group.add(bullet_enemy)
            self.timer_shoot = 0
        pygame.sprite.groupcollide(bullet_player_group, enemy_group, True, True)


class Flag(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        pygame.sprite.groupcollide(bullet_player_group, flag_group, True, True)
        pygame.sprite.groupcollide(bullet_enemy_group, flag_group, True, True)


class Bullet_player(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir
        self.speed = 6

    def update(self):
        if self.dir == "left":
            self.rect.x = self.rect.x - self.speed
        elif self.dir == "right":
            self.rect.x = self.rect.x + self.speed
        elif self.dir == "top":
            self.rect.y = self.rect.y - self.speed
        elif self.dir == "bottom":
            self.rect.y = self.rect.y + self.speed


class Bullet_enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir
        self.speed = 5

    def update(self):
        if self.dir == "left":
            self.rect.x = self.rect.x - self.speed
        elif self.dir == "right":
            self.rect.x = self.rect.x + self.speed
        elif self.dir == "top":
            self.rect.y = self.rect.y - self.speed
        elif self.dir == "bottom":
            self.rect.y = self.rect.y + self.speed


brick_group = pygame.sprite.Group()
bush_group = pygame.sprite.Group()
iron_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
player = Player(player_image, (200, 640))
player_group.add(player)
bullet_player_group = pygame.sprite.Group()
bullet_enemy_group = pygame.sprite.Group()
drawMaps('1.txt')
button_group = pygame.sprite.Group()

button_start = Button(button_image, (500, 100), 'game', 'start')
button_group.add(button_start)

button_exit = Button(button_image, (500, 180), 'exit', 'exit')
button_group.add(button_exit)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if lvl == "game":
        lvlgame()
    elif lvl == 'menu':
        startMenu()
    elif lvl == 'exit':
        pygame.quit()
        sys.exit()
    clock.tick(FPS)

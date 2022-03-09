import colorsys
import math
import pygame
import random
import sys
import time
from pygame.locals import *

from background import Background
from banana import Banana
from button import Button
from player import Player
from utils import checkCollisions
from utils import clamp
banana = []


def main():
    global banana
    pygame.init()
    DISPLAY = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('BANANA BAN')
    pygame.display.set_icon(Banana().sprite)
    # получаем шрифты (пишу коменты фор галочка)
    font = pygame.font.Font('data/fonts/font.ttf', 100)
    font_small = pygame.font.Font('data/fonts/font.ttf', 26)
    font_20 = pygame.font.Font('data/fonts/font.ttf', 20)
    # получаем изображения
    shop = pygame.image.load('data/gfx/shop.png')
    shop_bg = pygame.image.load('data/gfx/shop_bg.png')
    retry_button = pygame.image.load('data/gfx/retry_button.png')
    logo = pygame.image.load('data/gfx/logo.png')
    title_bg = pygame.image.load('data/gfx/bg.png')
    title_bg.fill((255, 30.599999999999998, 0.0), special_flags=pygame.BLEND_ADD)
    shadow = pygame.image.load('data/gfx/shadow.png')
    # получаем звуки
    flapfx = pygame.mixer.Sound("data/sfx/flap.wav")
    upgradefx = pygame.mixer.Sound("data/sfx/upgrade.wav")
    benanafx = pygame.mixer.Sound("data/sfx/banana.wav")
    deadfx = pygame.mixer.Sound("data/sfx/dead.wav")
    # цвета
    WHITE = (255, 255, 255)  # constant
    # переменные
    rotOffset = -5
    # создание объекта игрока
    player = Player()
    bananas = []
    buttons = []
    # добавляем кнопочки
    for i in range(3):
        buttons.append(Button())
    # загрузка имагов на основе идексов
    buttons[0].typeIndicatorSprite = pygame.image.load('data/gfx/flap_indicator.png')
    buttons[0].price = 5
    buttons[1].typeIndicatorSprite = pygame.image.load('data/gfx/speed_indicator.png')
    buttons[1].price = 5
    buttons[2].typeIndicatorSprite = pygame.image.load('data/gfx/banana_ind.png')
    buttons[2].price = 30
    # получаем 5 бананов
    for i in range(5):
        bananas.append(Banana())
    # смотрим список бананов
    for banana in bananas:
        banana.position.xy = random.randrange(0, DISPLAY.get_width() - banana.sprite.get_width()), bananas.index(
            banana) * -200 - player.position.y
    # список фонов где каждый индекс объект
    bg = [Background(), Background(), Background()]
    # так надо
    bananaCount = 0
    startingHeight = player.position.y
    height = 0
    health = 100
    flapForce = 3
    bananaMultiplier = 5
    dead = False
    last_time = time.time()
    splashScreenTimer = 0
    # заставка
    # играем звук
    pygame.mixer.Sound.play(flapfx)
    while splashScreenTimer < 100:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        splashScreenTimer += dt

        for event in pygame.event.get():
            # если юзер жмакнул на кнопку
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((231, 205, 183))
        startMessage = font_small.render("VINOGRADOV", True, (171, 145, 123))
        DISPLAY.blit(startMessage, (DISPLAY.get_width() / 2 - startMessage.get_width() / 2,
                                    DISPLAY.get_height() / 2 - startMessage.get_height() / 2))

        # обнова дисплея
        pygame.display.update()
        # вайт 10 секонд
        pygame.time.delay(10)

    titleScreen = True
    pygame.mixer.Sound.play(flapfx)
    while titleScreen:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # получить позицию мыши
        mouseX, mouseY = pygame.mouse.get_pos()
        # получаем жмаканье
        clicked = False
        # чекаем события
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            # если игрок ливнул
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if (clicked and checkCollisions(mouseX, mouseY, 3, 3, DISPLAY.get_width() / 2 - retry_button.get_width() / 2,
                                        288, retry_button.get_width(), retry_button.get_height())):
            pygame.mixer.Sound.play(upgradefx)
            titleScreen = False

        DISPLAY.fill(WHITE)
        DISPLAY.blit(title_bg, (0, 0))
        DISPLAY.blit(shadow, (0, 0))
        DISPLAY.blit(logo, (DISPLAY.get_width() / 2 - logo.get_width() / 2,
                            DISPLAY.get_height() / 2 - logo.get_height() / 2 + math.sin(time.time() * 5) * 5 - 25))
        DISPLAY.blit(retry_button, (DISPLAY.get_width() / 2 - retry_button.get_width() / 2, 288))
        startMessage = font_small.render("ИГРАТЬ", True, (0, 0, 0))
        DISPLAY.blit(startMessage, (DISPLAY.get_width() / 2 - startMessage.get_width() / 2, 292))

        pygame.display.update()
        pygame.time.delay(10)

    # основной цикл игры
    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # снова получаем позицию
        mouseX, mouseY = pygame.mouse.get_pos()

        jump = False
        clicked = False
        # чек событий
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                jump = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouseY < DISPLAY.get_height() - 90:
                jump = True
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        camOffset = -player.position.y + DISPLAY.get_height() / 2 - player.currentSprite.get_size()[1] / 2

        DISPLAY.fill(WHITE)
        for o in bg:
            o.setSprite(((player.position.y / 50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))

        color = colorsys.hsv_to_rgb(((player.position.y / 50) % 100) / 100, 0.5, 0.5)
        currentHeightMarker = font.render(str(height), True, (color[0] * 255, color[1] * 255, color[2] * 255, 50))
        DISPLAY.blit(currentHeightMarker, (DISPLAY.get_width() / 2 - currentHeightMarker.get_width() / 2,
                                           camOffset + round((
                                                                     player.position.y - startingHeight) / DISPLAY.get_height()) * DISPLAY.get_height() + player.currentSprite.get_height() - 40))

        for banana in bananas:
            DISPLAY.blit(banana.sprite, (banana.position.x, banana.position.y + camOffset))

        DISPLAY.blit(pygame.transform.rotate(player.currentSprite, clamp(player.velocity.y, -10, 5) * rotOffset),
                     (player.position.x, player.position.y + camOffset))
        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY, (81, 48, 20), (21, 437, 150 * (health / 100), 25))
        DISPLAY.blit(shop, (0, 0))

        for button in buttons:
            DISPLAY.blit(button.sprite, (220 + (buttons.index(button) * 125), 393))
            priceDisplay = font_small.render(str(button.price), True, (0, 0, 0))
            DISPLAY.blit(priceDisplay, (262 + (buttons.index(button) * 125), 408))
            levelDisplay = font_20.render('ЛВЛ. ' + str(button.level), True, (200, 200, 200))
            DISPLAY.blit(levelDisplay, (234 + (buttons.index(button) * 125), 441))
            DISPLAY.blit(button.typeIndicatorSprite, (202 + (buttons.index(button) * 125), 377))
        bananaCountDisplay = font_small.render(str(bananaCount).zfill(7), True, (0, 0, 0))
        DISPLAY.blit(bananaCountDisplay, (72, 394))
        if dead:
            DISPLAY.blit(retry_button, (4, 4))
            deathMessage = font_small.render("Заново", True, (0, 0, 0))
            DISPLAY.blit(deathMessage, (24, 8))

        height = round(-(player.position.y - startingHeight) / DISPLAY.get_height())

        player.position.x += player.velocity.x * dt
        if player.position.x + player.currentSprite.get_size()[0] > 640:
            player.velocity.x = -abs(player.velocity.x)
            player.currentSprite = player.leftSprite
            rotOffset = 5
        if player.position.x < 0:
            player.velocity.x = abs(player.velocity.x)
            player.currentSprite = player.rightSprite
            rotOffset = -5
        if jump and not dead:
            player.velocity.y = -flapForce
            pygame.mixer.Sound.play(flapfx)
        player.position.y += player.velocity.y * dt
        player.velocity.y = clamp(player.velocity.y + player.acceleration * dt, -99999999999, 50)

        health -= 0.2 * dt
        if health <= 0 and not dead:
            dead = True
            pygame.mixer.Sound.play(deadfx)

        for banana in bananas:
            if banana.position.y + camOffset + 90 > DISPLAY.get_height():
                banana.position.y -= DISPLAY.get_height() * 2
                banana.position.x = random.randrange(0, DISPLAY.get_width() - banana.sprite.get_width())
            if (checkCollisions(player.position.x, player.position.y, player.currentSprite.get_width(),
                                player.currentSprite.get_height(), banana.position.x, banana.position.y,
                                banana.sprite.get_width(), banana.sprite.get_height())):
                dead = False
                pygame.mixer.Sound.play(benanafx)
                bananaCount += 1
                health = 100
                banana.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                banana.position.x = random.randrange(0, DISPLAY.get_width() - banana.sprite.get_width())

        for button in buttons:
            buttonX, buttonY = 220 + (buttons.index(button) * 125), 393
            if clicked and not dead and checkCollisions(mouseX, mouseY, 3, 3, buttonX, buttonY,
                                                        button.sprite.get_width(), button.sprite.get_height()):
                if bananaCount >= button.price:
                    pygame.mixer.Sound.play(upgradefx)
                    button.level += 1
                    bananaCount -= button.price
                    button.price = round(button.price * 2.5)
                    if buttons.index(button) == 0:
                        flapForce *= 1.5
                    if buttons.index(button) == 1:
                        player.velocity.x *= 1.5
                    if buttons.index(button) == 2:
                        bananaMultiplier += 10
                        for i in range(bananaMultiplier):
                            bananas.append(Banana())
                            bananas[-1].position.xy = random.randrange(0,
                                                                       DISPLAY.get_width() - banana.sprite.get_width()), player.position.y - DISPLAY.get_height() - random.randrange(
                                0, 200)

        if dead and clicked and checkCollisions(mouseX, mouseY, 3, 3, 4, 4, retry_button.get_width(),
                                                retry_button.get_height()):
            health = 100
            player.velocity.xy = 3, 0
            player.position.xy = 295, 100
            player.currentSprite = player.rightSprite
            bananaCount = 0
            height = 0
            flapForce = 3
            bananaMultiplier = 5
            buttons = []
            for i in range(3):
                buttons.append(Button())
            buttons[0].typeIndicatorSprite = pygame.image.load('data/gfx/flap_indicator.png')
            buttons[0].price = 5
            buttons[1].typeIndicatorSprite = pygame.image.load('data/gfx/speed_indicator.png')
            buttons[1].price = 5
            buttons[2].typeIndicatorSprite = pygame.image.load('data/gfx/bananaup_indicator.png')
            buttons[2].price = 30
            bananas = []
            for i in range(5):
                bananas.append(banana())
            for banana in bananas:
                banana.position.xy = random.randrange(0,
                                                      DISPLAY.get_width() - banana.sprite.get_width()), bananas.index(
                    banana) * -200 - player.position.y
            pygame.mixer.Sound.play(upgradefx)
            dead = False

        bg[0].position = camOffset + round(player.position.y / DISPLAY.get_height()) * DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height()
        bg[2].position = bg[0].position - DISPLAY.get_height()

        pygame.display.update()
        pygame.time.delay(10)


if __name__ == "__main__":
    main()

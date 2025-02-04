import os
import sys
import pygame
import random

pygame.init()
pygame.key.set_repeat(100, 70)

FPS = 60
WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
coll_sprites = pygame.sprite.Group()
pole = pygame.sprite.Group()
walls = pygame.sprite.Group()
wallandbarries = pygame.sprite.Group()
grass = pygame.sprite.Group()
pygame.mixer.init()
dif = 1
volsound = 10


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global dif
    global volsound
    slide = 0
    while True:
        with open("data/records.txt", "r", encoding="utf-8") as file:
            r = file.readlines()
        pygame.display.set_caption("Меню")
        cb = (0, 0, 0)
        cw = (255, 255, 255)
        font = pygame.font.Font("data/cs.ttf", 37)
        fontfortext = pygame.font.Font("data/cs.ttf", 20)
        texta1 = font.render("Играть", 1, cb)
        texta2 = font.render("Результаты", 1, cb)
        texta3 = font.render("Правила", 1, cb)
        texta4 = font.render("Назад", 1, cb)
        texta5 = fontfortext.render("Ваша задача собрать все шестеренки", 1, cb)
        texta6 = fontfortext.render("и не умереть от голода и призраков", 1, cb)
        texta7 = fontfortext.render("На колесико мыши вверх или вниз", 1, cb)
        texta9 = fontfortext.render(f"Каждые {20 - dif * 2} секунд происходит смена дня и ночи", 1, cb)
        texta8 = fontfortext.render(f"можно менять сложность игры. Текущая сложность: {dif}", 1, cb)
        texta10 = font.render("Последний результат", 1, cb)
        texta11 = fontfortext.render(f"Громкость звуков: {volsound // 1}", 1, cb)
        texta12 = fontfortext.render(f"(Изменение на колесико мыши)", 1, cb)

        screen.blit(load_image("fon.png"), (0, 0))
        if slide == 0:
            pygame.draw.rect(screen, cw, ((230, 100), (texta1.get_width(), texta1.get_height())))
            pygame.draw.rect(screen, cw, ((190, 200), (texta2.get_width(), texta2.get_height())))
            pygame.draw.rect(screen, cw, ((210, 300), (texta3.get_width(), texta3.get_height())))
            pygame.draw.rect(screen, cb, ((230, 100), (texta1.get_width(), texta1.get_height())), 2)
            pygame.draw.rect(screen, cb, ((190, 200), (texta2.get_width(), texta2.get_height())), 2)
            pygame.draw.rect(screen, cb, ((210, 300), (texta3.get_width(), texta3.get_height())), 2)
            screen.blit(texta1, (230, 100))
            screen.blit(texta2, (190, 200))
            screen.blit(texta3, (210, 300))
            screen.blit(texta11, (50, 370))
            screen.blit(texta12, (260, 370))
        if slide == 1:
            pygame.draw.rect(screen, cw, ((60, 300), (texta4.get_width(), texta4.get_height())))
            pygame.draw.rect(screen, cb, ((60, 300), (texta4.get_width(), texta4.get_height())), 2)
            screen.blit(texta4, (60, 300))
            screen.blit(texta5, (60, 20))
            screen.blit(texta6, (60, 50))
            screen.blit(texta7, (60, 120))
            screen.blit(texta8, (60, 140))
            screen.blit(texta9, (60, 160))
        if slide == 2:
            pygame.draw.rect(screen, cw, ((60, 300), (texta4.get_width(), texta4.get_height())))
            pygame.draw.rect(screen, cb, ((60, 300), (texta4.get_width(), texta4.get_height())), 2)
            screen.blit(texta4, (60, 300))
            screen.blit(texta10, (60, 20))
            ycount = 60
            for i in r:
                ycount += 20
                screen.blit(fontfortext.render(i.strip(), 1, cb), (60, ycount))
        button1 = Button(texta1, 230, 100)
        button2 = Button(texta2, 190, 200)
        button3 = Button(texta3, 210, 300)
        button4 = Button(texta4, 60, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if button1.check(x, y) and slide == 0:
                    return
                if button2.check(x, y) and slide == 0:
                    slide = 2
                if button3.check(x, y) and slide == 0:
                    slide = 1
                if button4.check(x, y) and (slide == 1 or slide == 2):
                    slide = 0
            if event.type == pygame.MOUSEBUTTONDOWN and slide == 1 and event.button == 4:
                dif += 1
                if dif > 5:
                    dif = 5
            if event.type == pygame.MOUSEBUTTONDOWN and slide == 1 and event.button == 5:
                dif -= 1
                if dif < 1:
                    dif = 1
            if event.type == pygame.MOUSEBUTTONDOWN and slide == 0 and event.button == 4:
                volsound += 1
                if volsound > 10:
                    volsound = 10
            if event.type == pygame.MOUSEBUTTONDOWN and slide == 0 and event.button == 5:
                volsound -= 1
                if volsound < 0:
                    volsound = 0
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(value):
    while True:
        pygame.display.set_caption('Конец')
        screen.blit(load_image(f"gameover{value}.png"), (0, 0))
        font = pygame.font.Font("data/cs.ttf", 26)
        text2b = font.render("Нажмите на любую клавишу чтобы выйти", 1, (255, 0, 0))
        if value == 2:
            text1b = font.render("Вы умерли. Ваш результат не записан", 1, (255, 0, 0))
        if value == 1:
            text1b = font.render("Вы выжили. Ваш результат записан", 1, (255, 0, 0))
        screen.blit(text1b, (50, 20))
        screen.blit(text2b, (50, 50))
        pygame.display.flip()
        clock.tick(FPS)
        pygame.time.wait(3000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                return


class Camera:
    def __init__(self, w, h):
        self.camera = pygame.Rect(0, 0, w, h)
        self.dx = w
        self.dy = h

    def apply(self, obj):
        x, y = self.camera.topleft
        obj.rect.x += x
        obj.rect.y += y

    def update(self, target):
        x = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        y = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
        self.camera = pygame.Rect(x, y, self.dx, self.dy)


class SH(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(coll_sprites)
        self.image = load_image("meh.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-600, 570, 10)
        self.rect.y = random.randrange(-300, 810, 10)


class Apple(pygame.sprite.Sprite):
    def __init__(self, obj):
        super().__init__(coll_sprites)
        self.image = load_image("apple.png", -1)
        self.rect = self.image.get_rect()
        flag = False
        x0 = obj.rect.x + obj.rect.w // 2
        y0 = obj.rect.y + obj.rect.h // 2
        while flag is False:
            self.rect.x = random.randrange(x0 - 50, x0 + 50)
            self.rect.y = random.randrange(y0 - 50, y0 + 50)
            if (self.rect.x - x0) ** 2 + (self.rect.y - y0) ** 2 <= 2500:
                flag = True


class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(wallandbarries)
        self.ranim = random.randrange(1, 3)
        self.image = load_image(f"tree{self.ranim}.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-600, 570, 10)
        self.rect.y = random.randrange(-300, 810, 10)

class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(grass)
        self.image = load_image("grass.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall(pygame.sprite.Sprite):
    def __init__(self, s1, s2):
        super().__init__(walls)
        if s1 == 0:
            self.image = load_image("wwall.png")
            self.rect = self.image.get_rect()
            if s2 == 0:
                self.rect.y -= 600
                self.rect.x -= 600
            if s2 == 1:
                self.rect.y += 900
                self.rect.x -= 600
        if s1 == 1:
            self.image = load_image("hwall.png")
            self.rect = self.image.get_rect()
            if s2 == 0:
                self.rect.y -= 700
                self.rect.x -= 1200
            if s2 == 1:
                self.rect.y -= 700
                self.rect.x += 600


class Darkness(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pole)
        self.image = load_image("notdark.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.count = 0
        self.day = True

    def target1(self, obj):
        self.rect.x = obj.rect.x - WIDTH // 2
        self.rect.y = obj.rect.y - HEIGHT // 2

    def cicle(self, time):
        if time // (20 - dif * 2) > self.count and self.day is True:
            self.count += 1
            self.day = False
            self.image = load_image("dark.png", -1)
        elif time // (20 - dif * 2) > self.count and self.day is False:
            self.count += 1
            self.day = True
            self.image = load_image("notdark.png", -1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        global sound1
        self.image = load_image("player.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = 280
        self.rect.y = 180
        self.collected = 100 - dif * 4
        self.collectedmeha = 0
        self.countwalks = 0
        self.collectedapples = 0

    def update(self, key):
        tmp_rect = self.rect.copy()
        if key == pygame.K_LEFT:
            self.rect.x -= 10
            self.image = load_image("player3.png", -1)
            self.countwalks += 1
        if key == pygame.K_RIGHT:
            self.rect.x += 10
            self.image = load_image("player4.png", -1)
            self.countwalks += 1
        if key == pygame.K_UP:
            self.rect.y -= 10
            self.image = load_image("player2.png", -1)
            self.countwalks += 1
        if key == pygame.K_DOWN:
            self.rect.y += 10
            self.image = load_image("player.png", -1)
            self.countwalks += 1
        colli = pygame.sprite.spritecollide(player, coll_sprites, True)
        if "Apple" in str(colli):
            self.collected += 16 - dif
            self.collectedapples += 1
            if self.collected > 100 - (dif * 4):
                self.collected = 100 - (dif * 4)
            sound2.play()
        if "SH" in str(colli):
            self.collectedmeha += 1
            sound1.play()
        if pygame.sprite.spritecollideany(self, wallandbarries):
            self.rect = tmp_rect
            self.countwalks -= 1
        if pygame.sprite.spritecollideany(self, walls):
            self.rect = tmp_rect
            self.countwalks -= 1


class Button:
    def __init__(self, obj, x=0, y=0):
        self.rect = obj.get_rect()
        self.x1 = x
        self.y1 = y

    def check(self, x, y):
        if self.x1 < x < self.rect.w + self.x1 and self.y1 < y < self.rect.h + self.y1:
            return True
        else:
            return False

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("ghost1.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-600, 570, 10)
        self.rect.y = random.randrange(-300, 810, 10)
        self.objx = 0
        self.objy = 0

    def update(self):
        if self.rect.x < self.objx:
            self.rect.x += 1
            self.image = load_image("ghost1.png", -1)
            return
        if self.rect.x > self.objx:
            self.rect.x -= 1
            self.image = load_image("ghost2.png", -1)
            return
        if self.rect.y < self.objy:
            self.rect.y += 1
            return
        if self.rect.y > self.objy:
            self.rect.y -= 1
            return

    def target(self, obj):
        self.objx, self.objy = obj.rect.x, obj.rect.y



start_screen()
cong = 0
sound1 = pygame.mixer.Sound('data/Mehacoll.wav')
sound1.set_volume(volsound / 10)
sound2 = pygame.mixer.Sound('data/Applecoll.mp3')
sound2.set_volume(volsound / 10)
sound3 = pygame.mixer.Sound('data/winsound.mp3')
sound3.set_volume(volsound / 10)
sound4 = pygame.mixer.Sound('data/losesound.mp3')
sound4.set_volume(volsound / 10)
pygame.mixer.music.load('data/backgroundmusic.wav')
pygame.mixer.music.set_volume(volsound / 10)
pygame.mixer.music.play(-1)
while cong < 1:
    ghost = Ghost()
    cong += 1
    if len(pygame.sprite.spritecollide(ghost, all_sprites, False)) > 1:
        ghost.kill()
        cong -= 1
count = 0
player = Player()
while count < 100:
    trees = Tree()
    count += 1
    if len(pygame.sprite.spritecollide(trees, all_sprites, False)) > 0:
        trees.kill()
        count -= 1
    if len(pygame.sprite.spritecollide(trees, wallandbarries, False)) > 1:
        trees.kill()
        count -= 1
    if len(pygame.sprite.spritecollide(trees, walls, False)) > 0:
        trees.kill()
        count -= 1
count1 = 0
while count1 < 20 - dif:
    randomtree = random.choice(wallandbarries.sprites())
    apple = Apple(randomtree)
    count1 += 1
    if len(pygame.sprite.spritecollide(apple, all_sprites, False)) > 1:
        apple.kill()
        count1 -= 1
    elif len(pygame.sprite.spritecollide(apple, coll_sprites, False)) > 1:
        apple.kill()
        count1 -= 1
    elif len(pygame.sprite.spritecollide(apple, wallandbarries, False)) > 1:
        apple.kill()
        count1 -= 1
    elif len(pygame.sprite.spritecollide(apple, walls, False)) > 1:
        apple.kill()
        count1 -= 1
count2 = 0
while count2 < 5 + dif:
    meha = SH()
    count2 += 1
    if len(pygame.sprite.spritecollide(meha, all_sprites, False)) > 1:
        meha.kill()
        count2 -= 1
    if len(pygame.sprite.spritecollide(meha, wallandbarries, False)) > 0:
        meha.kill()
        count2 -= 1
    if len(pygame.sprite.spritecollide(meha, walls, False)) > 0:
        meha.kill()
        count2 -= 1
    if len(pygame.sprite.spritecollide(meha, coll_sprites, False)) > 1:
        meha.kill()
        count2 -= 1
for y1 in range(-600, 601, 300):
    for x1 in range(-600, 601, 300):
        Gr = Grass(x1, y1)
running = True
dark = Darkness()
camera = Camera(WIDTH, HEIGHT)
wall1 = Wall(0, 0)
wall2 = Wall(0, 1)
wall3 = Wall(1, 0)
wall4 = Wall(1, 1)
start_time = pygame.time.get_ticks()
RED = (180, 0, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.update(event.key)
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            for sprite in coll_sprites:
                camera.apply(sprite)
            for sprite in wallandbarries:
                camera.apply(sprite)
            for sprite in walls:
                camera.apply(sprite)
            for sprite in grass:
                camera.apply(sprite)
    pygame.display.set_caption("Игра")
    player.collected -= 0.019 * dif
    dark.target1(player)
    ghost.target(player)
    ghost.update()
    f1 = pygame.font.Font("data/cs.ttf", 20)
    current_time = pygame.time.get_ticks() - start_time
    seconds = current_time // 1000
    dark.cicle(seconds)
    ct = seconds - (dark.count * (20 - dif * 2))
    text1 = f1.render(f'Голод:{int(player.collected // 1)}/{100 - dif * 4}', True, RED)
    if dark.day == True:
        text2 = f1.render(f"Время:{seconds}, (Ночь через:{(20 - dif * 2) - ct})", True, RED)
    else:
        text2 = f1.render(f"Время:{seconds}, (День через:{(20 - dif * 2) - ct})", True, RED)
    text3 = f1.render(f"Шестеренки:{player.collectedmeha}/{5 + dif}", True, RED)
    grass.draw(screen)
    wallandbarries.draw(screen)
    walls.draw(screen)
    coll_sprites.draw(screen)
    all_sprites.draw(screen)
    pole.draw(screen)
    screen.blit(text1, (10, 350))
    screen.blit(text2, (10, 300))
    screen.blit(text3, (10, 250))
    pygame.display.flip()
    clock.tick(FPS)
    if player.collectedmeha == 5 + dif:
        pygame.mixer.music.stop()
        sound3.play()
        end_screen(1)
        with open("data/records.txt", "w", encoding="utf-8") as file:
            file.write(f"Сложность игры: {dif}\n")
            file.write(f"Собрано всего яблок: {player.collectedapples}\n")
            file.write(f"Время: {seconds}\n")
            file.write(f"Сделано шагов: {player.countwalks}\n")
        running = False
    if player.collected < 0:
        pygame.mixer.music.stop()
        sound4.play()
        end_screen(2)
        running = False
    if len(pygame.sprite.spritecollide(ghost, all_sprites, False)) > 1:
        pygame.mixer.music.stop()
        sound4.play()
        end_screen(2)
        running = False
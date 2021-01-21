import pygame
from random import randint, randrange
from win32api import GetSystemMetrics
from PyQt5.QtWidgets import QApplication


app = QApplication([])
app.quit()


FPS = 64
width = GetSystemMetrics(0) # Ширина экрана
height = GetSystemMetrics(1) # Высота экрана
h_size = 50 # Горизонтальный размер объекта
v_size = 50 # Вертикаьный размер объекта
a = 0.35 # Ускорение
N = 6 # Кол-во экземпляров каждого элемента


interval = 100 # Радиус интервала без ускорения

BLACK = (0, 0, 0)


class Sq(pygame.sprite.Sprite):
    """Класс для квадратов"""


    def __init__(self, picture):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = picture
        self.image_orig.set_colorkey((255, 255, 255))
        self.image_orig = pygame.transform.scale(self.image_orig, (h_size, v_size))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (width//2, height//2)
        self.rect = self.rect.move(randint(-10, 10), randint(-10, 10))
        self.ax = 0
        self.ay = 0
        self.speed_x = randrange(-1, 2, 2) * randint(2, 14)
        self.speed_y = randrange(-1, 2, 2) * randint(2, 14)
        self.rot = 0
        self.rot_speed = randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()


    def rotate(self):
        '''Функция для вращения объектов'''
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        '''Обновление картинки'''
        self.rotate()
        self.rect.y += int(self.speed_y)
        self.rect.x += int(self.speed_x)

        if self.rect.center[0] > width//2 + interval:
            self.ax = -a
        elif self.rect.center[0] < width//2 - interval:
            self.ax = a
        else:
            self.ax = 0

        if self.rect.center[1] > height//2 + interval:
            self.ay = -a
        elif self.rect.center[1] < height//2 - interval:
            self.ay = a
        else:
            self.ay = 0

        self.speed_x += self.ax
        self.speed_y += self.ay


pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("Amimation")

clock = pygame.time.Clock()

# Загрузка всех изображений
white_sq = pygame.image.load('IMG/Белый.png').convert()
red_sq = pygame.image.load('IMG/Красный.png').convert()
blue_sq = pygame.image.load('IMG/Синий.png').convert()
yellow_sq = pygame.image.load('IMG/Желтый.png').convert()
green_sq = pygame.image.load('IMG/Зеленый.png').convert()
orange_sq = pygame.image.load('IMG/Оранжевый.png').convert()

elements = [white_sq, red_sq, blue_sq, yellow_sq, green_sq, orange_sq]

all_sprites = pygame.sprite.Group()

print(width, height)

# Создание экземпляров класса
for element in elements:
    for i in range(N):
        body = Sq(element)
        all_sprites.add(body)

finish = False

while not finish:
    '''Основной цикл'''
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finish = True

    screen.fill(BLACK)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
		
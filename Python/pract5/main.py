import TKinter as tk
import math
import random
from copy import copy
from models import ImageInfo, SpaceShip, Sprite
from util import dist
from imagelogic import ImageStorage

# Константы
WIDTH, HEIGHT = (800,)*2
SCORE = 0
LIVES = 5
TIME = 0
GAME_STARTED = False

#Задний фон
background = ImageStorage(ImageInfo([400, 400], [800, 800]), tk.load_image("./img/background.png"))
#Эта штука анимируетсяя еще (на переднем плане)
frontground = ImageStorage(ImageInfo([400, 400], [800, 800]), tk.load_image("./img/frontground.png"))
#Логотип при запуске
logo = ImageStorage(ImageInfo([200, 150], [400, 300]), tk.load_image("./img/logo.png"))
#Космический корабль
catship_img = ImageStorage(ImageInfo([45, 45], [90, 90], 35), tk.load_image("./img/ship.png"))
#Кама-пуля
bullet = ImageStorage(ImageInfo([5, 5], [10, 10], 3, 50), tk.load_image("./img/bullet.png"))
#Астероид
asteroid = ImageStorage(ImageInfo([45, 45], [90, 90], 40), tk.load_image("./img/asteroid.png"))
#Взрыв (анимация)
explosion = ImageStorage(ImageInfo([64, 64], [128, 128], 17, 24, True), tk.load_image("./img/explosion.png"))

#Множества объектов
asteroidsgroup_set = set({})
bulletsgroup_set = set({})
explosionsgroup_set = set({})

def click(pos):
    """Обработка нажатия на начало игры"""
    global GAME_STARTED, LIVES, SCORE

    center = [WIDTH / 2, HEIGHT / 2]
    size = logo.info.size
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    
    if (not GAME_STARTED) and inwidth and inheight:
        GAME_STARTED = True
        LIVES = 5
        SCORE = 0

def asteroids_spawner():
    """Таймер, который отвечает за спавн метеоритов"""
    global asteroidsgroup_set, catship

    #Рандомное место спавна для астероида
    asteroid_sprite = Sprite([random.choice(range(WIDTH)), random.choice(range(HEIGHT))],[1, 1],0.1,random.choice([-0.01, 0.01]),asteroid.image,asteroid.info,)

    #Кол-во метеоритов на карте одновременно
    if (len(asteroidsgroup_set) < 50 and dist(asteroid_sprite.position, catship.position) > 70 and GAME_STARTED):
        asteroidsgroup_set.add(asteroid_sprite)


def draw(canvas):
    """Отрисовщик интерфейса"""
    global TIME, SCORE, asteroidsgroup_set, LIVES, catship, bulletsgroup_set, GAME_STARTED

    #Анимация бекграунда кадра
    TIME += 3
    wtime = (TIME / 4) % WIDTH
    center = frontground.info.center
    size = frontground.info.size
    #Отрисовка бекграунда
    canvas.draw_image(background.image,background.info.center,background.info.size,[WIDTH / 2, HEIGHT / 2],[WIDTH, HEIGHT],)
    
    #Отрисовка анимации поверх бекграунда (она в png)
    canvas.draw_image(frontground.image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(frontground.image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    #Статистика текущей игры
    str1 = "Счёт: " + str(SCORE)
    str2 = "Жизни: " + str(LIVES)
    canvas.draw_text(str(str2), [40, 40], 20, "white")
    canvas.draw_text(str(str1), [40, 80], 20, "white")

    #Отрисовка корабля и спрайтов
    catship.draw(canvas)

    #Обновление корабля и спрайтов
    catship.update()

    #Если мы проиграли
    if LIVES <= 0:
        GAME_STARTED = False
        catship = SpaceShip([WIDTH / 2, HEIGHT / 2], [0, 0], 0, catship_img.image, catship_img.info)
        catship.ismove = False

        #Удаляем все элементы игры, которые были
        for sprite in set(asteroidsgroup_set):
            asteroidsgroup_set.remove(sprite)

        for sprite in set(bulletsgroup_set):
            bulletsgroup_set.remove(sprite)

        for element in set(explosionsgroup_set):
            explosionsgroup_set.remove(element)

    #Если еще не начали игру
    if not GAME_STARTED:
        #Отрисовываем лого игры
        canvas.draw_image(logo.image, logo.info.center, logo.info.size, [WIDTH / 2, HEIGHT / 2], logo.info.size)

    #Если уже начали игру
    if GAME_STARTED:
        process_sprite_group(asteroidsgroup_set, canvas)
        process_sprite_group(bulletsgroup_set, canvas)
        process_sprite_group(explosionsgroup_set, canvas)

    #Если врезался в нас метеорит - отнимаем жизни
    if group_collide(asteroidsgroup_set, catship):
        LIVES -= 1

    # Если мы убили метеорит - у нас прибавились очки
    SCORE += group_group_collide(asteroidsgroup_set, bulletsgroup_set)



def process_sprite_group(s, canvas):

    for sprite in set(s):
        sprite.draw(canvas)
        if sprite.update():
            s.remove(sprite)

def group_collide(s, other_object):

    for sprite in set(s):

        #Если попали в другой объект
        if sprite.collide(other_object):
            s.remove(sprite)
            explosion_pos = sprite.position
            explosion_vel = [0, 0]
            explosion_avel = 0
            #Показываем взрыв
            explosion_sprite = Sprite(explosion_pos,explosion_vel, 0, explosion_avel, explosion.image, explosion.info)
            #Добавляем взрыв в группу взрывов
            explosionsgroup_set.add(explosion_sprite)
            return True

    return False


def group_group_collide(group1, group2):

    counter = 0
    for sprite in copy(group1):

        if group_collide(group2, sprite):
            group1.discard(sprite)
            counter += 1
    return counter



def keydown(button_id):
    """Метод отрабатывает, когда кнопки нажимаются"""
    global bulletsgroup_set

    #Если еще не начали игру
    if not GAME_STARTED:
        return

    #Поворот влево
    if button_id == 37 or button_id == 65:
        catship.incAv()

    #Поворот вправо
    if button_id == 39 or button_id == 68:
        catship.decAv()

    #Перемещение вперед
    if button_id == 38 or button_id == 87:
        catship.ismove = True

    #Выстрел
    if button_id == 32:
        bulletsgroup_set = catship.shoot(GAME_STARTED, bulletsgroup_set, bullet.image, bullet.info)


def keyup(button_id):
    """Метод отрабатывает, когда кнопки перестают нажиматься"""
    #Если еще не начали игру
    if not GAME_STARTED:
        return

    #Перемещение влево/вправо
    if button_id == 37 or button_id == 39 or button_id == 65 or button_id == 68:
        catship.setAv()

    #Перемещение вперед
    if button_id == 38 or button_id == 87:
        catship.ismove = False


localeframe = tk.create_frame("Практика 5. Астероиды", WIDTH, HEIGHT)
catship = SpaceShip([WIDTH / 2, HEIGHT / 2], [0, 0], 0, catship_img.image, catship_img.info)

#Выставляем обработчики
localeframe.set_draw_handler(draw)
localeframe.set_keydown_handler(keydown)
localeframe.set_keyup_handler(keyup)
localeframe.set_mouseclick_handler(click)
#Таймер для спавна метеоритов
timer = tk.create_timer(1000.0, asteroids_spawner)

#Старт таймеров и т д
timer.start()
localeframe.start()
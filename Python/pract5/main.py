import TkinterWrapper as tkinter
import math
import random
from copy import copy
from models import ImageInfo, SpaceShip, Sprite
from util import dist

# Константы
WIDTH = 800
HEIGHT = 800
SCORE = 0
LIVES = 10
TIME = 0
GAME_STARTED = False


debris_info = ImageInfo([400, 400], [800, 800])
debris_image = tkinter.load_image("./img/frontground.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 400], [800, 800])
nebula_image = tkinter.load_image("./img/background.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = tkinter.load_image("./img/splash.png")

#
catship_info = ImageInfo([45, 45], [90, 90], 35)
catship_image = tkinter.load_image("./img/double_ship.png")

#Пуля
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = tkinter.load_image("./img/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = tkinter.load_image("./img/asteroid.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = tkinter.load_image("./img/explosion_alpha.png")


asteroidsgroup_set = set({})
bulletsgroup_set = set({})
explosionsgroup_set = set({})


def draw(canvas):
    """Отрисовщик интерфейса"""
    global TIME, SCORE, asteroidsgroup_set, LIVES, catship, bulletsgroup_set, GAME_STARTED

    #Анимация бекграунда кадра
    TIME += 3
    wtime = (TIME / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(
        nebula_image,
        nebula_info.get_center(),
        nebula_info.get_size(),
        [WIDTH / 2, HEIGHT / 2],
        [WIDTH, HEIGHT],
    )
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    str1 = "Счёт: " + str(SCORE)
    str2 = "Жизни: " + str(LIVES)
    canvas.draw_text(str(str2), [40, 40], 20, "white")
    canvas.draw_text(str(str1), [40, 80], 20, "white")

    #Отрисовка корабля и спрайтов
    catship.draw(canvas)

    #Обновление корабля и спрайтов
    catship.update()

    #Проиграли
    if LIVES <= 0:
        GAME_STARTED = False
        catship = SpaceShip([WIDTH / 2, HEIGHT / 2], [0, 0], 0, catship_image, catship_info)
        catship.setThrustOn(False)

        #Удаляем все элементы игры, которые были
        for sprite in set(asteroidsgroup_set):
            asteroidsgroup_set.remove(sprite)

        for sprite in set(bulletsgroup_set):
            bulletsgroup_set.remove(sprite)

        for element in set(explosionsgroup_set):
            explosionsgroup_set.remove(element)

    #Если еще не начали игру
    if not GAME_STARTED:
        canvas.draw_image(
            splash_image,
            splash_info.get_center(),
            splash_info.get_size(),
            [WIDTH / 2, HEIGHT / 2],
            splash_info.get_size(),
        )

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

def rock_spawner():
    """Таймер, который отвечает за спавн метеоритов"""
    global asteroidsgroup_set, catship

    a_rock = Sprite(
        #Рандомное место спавна 
        [random.choice(range(WIDTH)), random.choice(range(HEIGHT))],
        [1, 1],
        0.1,
        random.choice([-0.3, 0.3]),
        asteroid_image,
        asteroid_info,
    )

    if (
        #Кол-во метеоритов на карте одновременно
        len(asteroidsgroup_set) < 50
        and dist(a_rock.getPosition(), catship.getPosition()) > 70
        and GAME_STARTED
    ):
        asteroidsgroup_set.add(a_rock)


def click(pos):
    """Обработка нажатия на начало игры"""
    global GAME_STARTED, LIVES, SCORE

    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not GAME_STARTED) and inwidth and inheight:
        GAME_STARTED = True
        LIVES = 3
        SCORE = 0


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
            explosion_pos = sprite.getPosition()
            explosion_vel = [0, 0]
            explosion_avel = 0
            #Показываем взрыв
            explosion = Sprite(
                explosion_pos,
                explosion_vel,
                0,
                explosion_avel,
                explosion_image,
                explosion_info,
            )
            #Добавляем взрыв в группу взрывов
            explosionsgroup_set.add(explosion)
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
        catship.setThrustOn(True)

    #Выстрел
    if button_id == 32:
        bulletsgroup_set = catship.shoot(GAME_STARTED, bulletsgroup_set, missile_image, missile_info)


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
        catship.setThrustOn(False)


localeframe = tkinter.create_frame("Практика 5. Астероиды", WIDTH, HEIGHT)
catship = SpaceShip([WIDTH / 2, HEIGHT / 2], [0, 0], 0, catship_image, catship_info)

#Выставляем обработчики
localeframe.set_draw_handler(draw)
localeframe.set_keydown_handler(keydown)
localeframe.set_keyup_handler(keyup)
localeframe.set_mouseclick_handler(click)
#Таймер для спавна метеоритов
timer = tkinter.create_timer(1000.0, rock_spawner)

#Старт таймеров и т д
timer.start()
localeframe.start()

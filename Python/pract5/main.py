import TkinterWrapper as tkinter
import math
import random
from copy import copy
from models import ImageInfo, SpaceShip, Sprite
from util import dist

# Константы
WIDTH = 800
HEIGHT = 800
score = 0
lives = 3
time = 0
started = False


# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = tkinter.load_image(
    "./img/debris2_blue.png"
)

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 400], [800, 800])
nebula_image = tkinter.load_image(
    "./img/background.png"
)

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = tkinter.load_image(
    "./img/splash.png"
)

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = tkinter.load_image(
    "./img/double_ship.png"
)

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = tkinter.load_image(
    "./img/shot2.png"
)

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = tkinter.load_image(
    "./img/asteroid.png"
)

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = tkinter.load_image(
    "./img/explosion_alpha.png"
)


rock_group = set({})
missile_group = set({})
explosion_group = set({})


def draw(canvas):
    global time, score, rock_group, lives, my_ship, missile_group, started

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
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

    str1 = "Счёт: " + str(score)
    str2 = "Жизни: " + str(lives)
    canvas.draw_text(str(str2), [40, 40], 20, "white")
    canvas.draw_text(str(str1), [40, 80], 20, "white")

    #Отрисовка корабля и спрайтов
    my_ship.draw(canvas)

    #Обновление корабля и спрайтов
    my_ship.update()
    # a_rock.update()
    # a_missile.update()

    #Проиграли
    if lives <= 0:
        started = False
        my_ship = SpaceShip([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        my_ship.setThrustOn(False)

        for sprite in set(rock_group):
            rock_group.remove(sprite)

        for sprite in set(missile_group):
            missile_group.remove(sprite)

        for element in set(explosion_group):
            explosion_group.remove(element)

    if not started:
        canvas.draw_image(
            splash_image,
            splash_info.get_center(),
            splash_info.get_size(),
            [WIDTH / 2, HEIGHT / 2],
            splash_info.get_size(),
        )

    if started:
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)

    if group_collide(rock_group, my_ship):
        lives -= 1

    score += group_group_collide(rock_group, missile_group)

def rock_spawner():
    """Таймер, который отвечает за спавн метеоритов"""
    global rock_group, my_ship

    a_rock = Sprite(
        [random.choice(range(WIDTH)), random.choice(range(HEIGHT))],
        [1, 1],
        0.1,
        random.choice([-0.1, 0.1]),
        asteroid_image,
        asteroid_info,
    )

    if (
        len(rock_group) < 13
        and dist(a_rock.getPosition(), my_ship.getPosition()) > 70
        and started
    ):
        rock_group.add(a_rock)


def click(pos):
    """Обработка нажатия на начало игры"""
    global started, lives, score

    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0


def process_sprite_group(s, canvas):

    for sprite in set(s):
        sprite.draw(canvas)
        if sprite.update():
            s.remove(sprite)


def group_collide(s, other_object):

    for sprite in set(s):

        if sprite.collide(other_object):
            s.remove(sprite)
            explosion_pos = sprite.getPosition()
            explosion_vel = [0, 0]
            explosion_avel = 0
            explosion = Sprite(
                explosion_pos,
                explosion_vel,
                0,
                explosion_avel,
                explosion_image,
                explosion_info,
            )
            explosion_group.add(explosion)
            return True

    return False


def group_group_collide(group1, group2):

    count = 0
    for sprite in copy(group1):

        if group_collide(group2, sprite):
            group1.discard(sprite)
            count += 1

    return count



def keydown(button_id):
    """Метод отрабатывает, когда кнопки нажимаются"""
    global missile_group

    #Если еще не начали игру
    if not started:
        return

    #Поворот влево
    if button_id == 37 or button_id == 65:
        my_ship.incAv()

    #Поворот вправо
    if button_id == 39 or button_id == 68:
        my_ship.decAv()

    #Перемещение вперед
    if button_id == 38 or button_id == 87:
        my_ship.setThrustOn(True)

    #Выстрел
    if button_id == 32:
        missile_group = my_ship.shoot(
            started, missile_group, missile_image, missile_info
        )


def keyup(button_id):
    """Метод отрабатывает, когда кнопки перестают нажиматься"""
    #Если еще не начали игру
    if not started:
        return

    #Перемещение влево/вправо
    if button_id == 37 or button_id == 39 or button_id == 65 or button_id == 68:
        my_ship.setAv()

    #Перемещение вперед
    if button_id == 38 or button_id == 87:
        my_ship.setThrustOn(False)



# initialize frame
frame = tkinter.create_frame("Практика 5. Астероиды", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = SpaceShip([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0.1, -0.1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
#Таймер для астероидов
timer = tkinter.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

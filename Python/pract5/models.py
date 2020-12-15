"""Модуль с основными моделями для игры"""

import math
from util import angle_to_vector
WIDTH, HEIGHT = (800,)*2

class ImageInfo:
    """
    Класс с информацией об изображении
    Аргументы: центр, размер, радиус, 
    """

    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self._center = center
        self._size = size
        self._radius = radius
        if lifespan:
            self._lifespan = lifespan
        else:
            self._lifespan = float("inf")
        self._animated = animated

    @property
    def center(self):
        return self._center

    @property
    def size(self):
        return self._size

    @property
    def radius(self):
        return self._radius

    @property
    def lifespan(self):
        return self._lifespan

    @property
    def animated(self):
        return self._animated

class Sprite:
    """
    Класс спрайта
    Используется для всех объектов
    """

    def __init__(self, pos, vel, ang, ang_vel, image, info):
        self._pos = [pos[0], pos[1]]
        self._vel = [vel[0], vel[1]]
        self._angle = ang
        self._angle_vel = ang_vel
        self._image = image
        self._image_center = info.center
        self._image_size = info.size
        self._radius = info.radius
        self._lifespan = info.lifespan
        self._animated = info.animated
        self._age = 0

    @property
    def position(self):
        return self._pos

    @property
    def radius(self):
        return self._radius
    

    def draw(self, canvas):

        #Если анимировано
        if self._animated:
            canvas.draw_image(self._image,[self._image_center[0] + self._age * self._image_size[0],self._image_center[1],],self._image_size,self._pos,self._image_size,self._angle)
        else:
            canvas.draw_image(self._image, self._image_center, self._image_size, self._pos, self._image_size, self._angle)

    def update(self):
        self._angle += self._angle_vel

        self._pos[0] = (self._pos[0] + self._vel[0]) % WIDTH
        self._pos[1] = (self._pos[1] + self._vel[1]) % HEIGHT

        self._age += 1

        if self._age > self._lifespan:
            return True
        else:
            return False

    def collide(self, other_object):
        """Столкновение с другим объектом"""
        dist = math.pow((self.position[0] - other_object.position[0]), 2) + math.pow((self.position[1] - other_object.position[1]), 2)
        dist = math.pow(dist, 0.5)
        if self._radius + other_object.radius > dist:
            return True
        return False

class SpaceShip:
    """Класс космического корабля"""

    def __init__(self, pos, vel, angle, image, info):
        self._pos = [pos[0], pos[1]]
        self._vel = [vel[0], vel[1]]
        self._angle = angle
        self._angle_vel = 0
        self._image = image
        self._image_center = info.center
        self._image_size = info.size
        self._radius = info.radius
        self._thrust = False

    def draw(self, canvas):

        if self._thrust:
            t = 90
            canvas.draw_image(self._image, (self._image_center[0] + t, self._image_center[1]), self._image_size, self._pos, self._image_size, self._angle)

        else:
            canvas.draw_image(self._image, self._image_center, self._image_size, self._pos, self._image_size, self._angle)

    def update(self):

        self._angle += self._angle_vel

        self._pos[0] = (self._pos[0] + self._vel[0]) % WIDTH
        self._pos[1] = (self._pos[1] + self._vel[1]) % HEIGHT

        fv = angle_to_vector(self._angle)

        if self._thrust:
            self._vel[0] += fv[0] / 10
            self._vel[1] += fv[1] / 10

        self._vel[0] *= 1 - 0.01
        self._vel[1] *= 1 - 0.01

    def incAv(self):

        self._angle_vel -= 0.1

    def decAv(self):

        self._angle_vel += 0.1

    def setAv(self):
        self._angle_vel = 0

    @property
    def ismove(self):
        return self._thrust
    
    @ismove.setter
    def ismove(self, val):
        self._thrust = val

    @property
    def position(self):
        return self._pos
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = value

    def shoot(self, started, missile_group, missile_image, missile_info):
        """Стрельба"""

        if not started:
            return
        vel = [0, 0]
        fw = angle_to_vector(self._angle)
        vel[0] = self._vel[0] + fw[0] * 5
        vel[1] = self._vel[0] + fw[1] * 5
        missile_pos = [self._pos[0] + fw[0] * 40, self._pos[1] + fw[1] * 40]
        a_missile = Sprite(missile_pos, vel, 0, 0, missile_image, missile_info)
        missile_group.add(a_missile)
        return missile_group
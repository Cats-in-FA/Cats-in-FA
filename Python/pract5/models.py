"""Модуль с основными моделями для игры"""
#TODO реализовать геттеры-сеттеры через property

import math
from util import angle_to_vector
WIDTH, HEIGHT =  (800,)*2

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
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.center
        self.image_size = info.size
        self._radius = info.radius
        self.lifespan = info.lifespan
        self.animated = info.animated
        self.age = 0

    @property
    def position(self):
        return self.pos

    @property
    def radius(self):
        return self._radius
    

    def draw(self, canvas):

        if self.animated:
            canvas.draw_image(
                self.image,
                [
                    self.image_center[0] + self.age * self.image_size[0],
                    self.image_center[1],
                ],
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )
        else:
            canvas.draw_image(
                self.image,
                self.image_center,
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )

    def update(self):
        self.angle += self.angle_vel

        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        self.age += 1

        if self.age > self.lifespan:
            return True
        else:
            return False

    def collide(self, other_object):
        dist = math.pow(
            (self.position[0] - other_object.position[0]), 2
        ) + math.pow((self.position[1] - other_object.position[1]), 2)
        dist = math.pow(dist, 0.5)
        if self._radius + other_object.radius > dist:
            return True
        return False

class SpaceShip:
    """Класс космического корабля"""

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.center
        self.image_size = info.size
        self._radius = info.radius
        self.thrust = False

    def draw(self, canvas):

        if self.thrust:

            t = 90

            canvas.draw_image(
                self.image,
                (self.image_center[0] + t, self.image_center[1]),
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )

        else:
            canvas.draw_image(
                self.image,
                self.image_center,
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )

    def update(self):

        self.angle += self.angle_vel

        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        fv = angle_to_vector(self.angle)

        if self.thrust:
            self.vel[0] += fv[0] / 10
            self.vel[1] += fv[1] / 10

        self.vel[0] *= 1 - 0.01
        self.vel[1] *= 1 - 0.01

    def incAv(self):

        self.angle_vel -= 0.1

    def decAv(self):

        self.angle_vel += 0.1

    def setAv(self):
        self.angle_vel = 0

    @property
    def ismove(self):
        return self.thrust
    
    @ismove.setter
    def ismove(self, val):
        self.thrust = val

    @property
    def position(self):
        return self.pos
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
        fw = angle_to_vector(self.angle)
        vel[0] = self.vel[0] + fw[0] * 5
        vel[1] = self.vel[0] + fw[1] * 5
        missile_pos = [self.pos[0] + fw[0] * 40, self.pos[1] + fw[1] * 40]
        a_missile = Sprite(missile_pos, vel, 0, 0, missile_image, missile_info)
        missile_group.add(a_missile)
        return missile_group
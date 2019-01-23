# coding=utf-8
# coding=utf-8
# coding=utf-8
from itertools import cycle
from math import radians

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class ColonelBullet0(EnemyBullet):
    def __init__(self, game, pos, size, angle, speed=5):
        super().__init__(game, pos)
        self.speed = speed
        self.images = cycle((pygame.transform.scale(x, (size, size)) for x in (GFX['e_bt3'], GFX['e_bt4'])))
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.direction = PVector(0, 0).project(radians(angle), self.speed)

    def update_img(self):
        if self.frame % 4 == 0:
            self.image = next(self.images)

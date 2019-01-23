# coding=utf-8
from itertools import cycle
from math import radians

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class BossBullet3(EnemyBullet):
    size = 15
    speed = 4

    def __init__(self, game, pos, angle):
        super().__init__(game, pos)
        self.images = cycle((GFX['ebt3'], GFX['ebt4']))
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.direction = PVector(0, 0).project(radians(angle), self.speed)

    def update_img(self):
        if self.frame % 4 == 0:
            self.image = next(self.images)

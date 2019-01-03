# coding=utf-8
from functools import partial
from itertools import cycle

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class PrivateBullet(EnemyBullet):
    size = 20
    speed = 6

    def __init__(self, pos, target, game):
        super().__init__(pos, game)
        angle = self.pos.angle_to(target)
        self.direction = PVector(0, 0).project(angle, self.speed)
        self.images = cycle((pygame.transform.scale(x, (self.size, self.size)) for x in
                             [GFX['e_bt1'], GFX['e_bt2']]))
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=tuple(self.pos))

    def move(self):
        self.pos += self.direction
        self.rect.center = tuple(self.pos)

    def update_img(self):
        if self.frame % 4 == 1:
            self.image = next(self.images)

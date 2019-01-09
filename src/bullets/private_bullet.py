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

    def __init__(self, game, pos, target):
        super().__init__(game, pos)
        angle = self.pos.angle_to(target)
        self.direction = PVector(0, 0).project(angle, self.speed)
        self.image = pygame.transform.scale(GFX['ebt3'], (self.size, self.size))
        self.rect = self.image.get_rect(center=tuple(self.pos))

    def move(self):
        self.pos += self.direction
        self.rect.center = tuple(self.pos)

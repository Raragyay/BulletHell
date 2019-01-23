# coding=utf-8
# coding=utf-8
# coding=utf-8
from itertools import cycle
from math import radians

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class CaptainBullet1(EnemyBullet):
    size = 10
    speed = 4

    def __init__(self, game, pos, angle):
        super().__init__(game, pos)
        self.image = pygame.transform.scale(GFX['ebt3'], (self.size, self.size))
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.direction = PVector(0, 0).project(radians(angle), self.speed)

    def update_img(self):
        self.image = pygame.transform.scale(GFX['ebt3'], (self.size, self.size))
        self.rect = self.image.get_rect(center=tuple(self.pos))

    def custom_action(self):
        if self.frame % 4 == 1:
            self.size += 1

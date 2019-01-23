# coding=utf-8
from math import radians
from random import randint

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class BossBullet2(EnemyBullet):
    size = 30
    speed = 5

    def __init__(self, game, pos, angle):
        super().__init__(game, pos)
        self.image = pygame.transform.scale(GFX['ebt3'], (self.size, self.size))
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.direction = PVector(0, 0).project(radians(angle), self.speed)

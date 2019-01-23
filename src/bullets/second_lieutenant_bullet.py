# coding=utf-8
from math import radians

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class SecondLieutenantBullet(EnemyBullet):
    speed = 5

    def __init__(self, game, pos, angle, size=20):
        super().__init__(game, pos)
        self.direction = PVector(0, 0).project(radians(angle), self.speed)
        self.image = pygame.transform.scale(GFX['ebt3'], (size, size))
        self.rect = self.image.get_rect(center=tuple(self.pos))

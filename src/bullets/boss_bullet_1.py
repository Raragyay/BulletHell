from math import radians
from random import randint

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class BossBullet1(EnemyBullet):
    size = 15

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.angle = randint(-110, -70)
        self.speed = randint(5, 10)
        self.image = pygame.transform.scale(GFX['ebt3'], (self.size, self.size))
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.direction = PVector(0, 0).project(radians(self.angle), self.speed)

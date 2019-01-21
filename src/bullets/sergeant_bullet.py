from math import degrees, radians

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class SergeantBullet(EnemyBullet):
    speed = 5

    def __init__(self, offset, target, game, pos):  # Offset is the offset from the angle to target.
        super().__init__(game, pos)
        self.angle = degrees(self.pos.angle_to(target)) + offset
        self.direction = PVector(0, 0).project(radians(self.angle), self.speed)
        self.image = pygame.transform.rotate(GFX['e_bt101'], self.angle - 90)
        self.rect = self.image.get_rect(center=tuple(self.pos))

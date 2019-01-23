from math import radians

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class FirstLieutenantBullet(EnemyBullet):
    speed = 5

    def __init__(self, game, pos, radius, angle, target, size, circle_radius_delta):
        super().__init__(game, pos)
        self.circle_center = pos
        self.circle_radius = radius
        self.angle = angle
        self.circle_radius_delta = circle_radius_delta
        angle_to_enemy = self.circle_center.angle_to(target)
        self.direction = PVector(0, 0).project(angle_to_enemy, self.speed)
        self.pos = self.circle_center.project(radians(self.angle), self.circle_radius)
        self.image = pygame.transform.scale(GFX['ebt3'], (size, size))
        self.rect = self.image.get_rect(center=tuple(self.pos))

    def move(self):
        self.angle += 10
        self.circle_radius += self.circle_radius_delta
        self.circle_center += self.direction
        self.pos = self.circle_center.project(radians(self.angle), self.circle_radius)
        self.rect.center = tuple(self.pos)

# coding=utf-8
from itertools import cycle
from math import radians

import pygame

from src.bullets.enemy_bullet import EnemyBullet
from src.components.PVector import PVector
from src.constants import GFX


class CorporalBullet(EnemyBullet):
    """
    Corporal shoots a circular blast that attempts to envelop the player.
    Each bullet is "radius" pixels away from the center.
    Radius increases, meaning that the circle grows larger and larger.
    """
    speed = 5

    def __init__(self, game, pos, angle, target):
        super().__init__(game, pos)
        self.circle_center = pos
        self.circle_radius = 0
        self.target = target
        angle_to_target = self.circle_center.angle_to(self.target)
        self.direction = PVector(0, 0).project(angle_to_target, self.speed)
        self.angle = radians(angle)  # In radians for math purposes
        self.pos = self.circle_center.project(self.angle, self.circle_radius)

        self.images = cycle([GFX['e_bt5'], GFX['e_bt6']])
        self.image: pygame.Surface = next(self.images)
        self.rect: pygame.Rect = self.image.get_rect(center=tuple(self.pos))

    def move(self):
        self.circle_radius += 2
        self.circle_center += self.direction
        self.pos = self.circle_center.project(self.angle, self.circle_radius)
        self.rect.center = tuple(self.pos)

    def update_img(self):
        if self.frame % 4 == 0:
            self.image = next(self.images)

# coding=utf-8
from math import radians

import pygame

from src.components.PVector import PVector
from src.bullets.bullet import Bullet
from src.constants import GFX


class PlayerBullet(Bullet):
    speed = 10  # TODO scale off level
    rotation = 0

    def __init__(self, player, angle, offset: PVector, *group):
        super().__init__(*group)
        self.player = player
        self.pos = player.pos + offset + player.direction.x * PVector(3, 0) - PVector(3, 25)
        if player.id in {1, 2}:
            self.pos -= PVector(0, 10)
        else:
            if player.direction.x == 0:
                PlayerBullet.rotation = 0
            else:
                PlayerBullet.rotation -= player.direction.x * 2  # Slowly rotate to the side if locust
            angle += PlayerBullet.rotation

        # print(adjusted_angle)
        self.direction = PVector(0, 0).project(radians(angle), PlayerBullet.speed)

        # print(self.direction)

        self.damage = 0
        self.init_image(player, angle)
        self.calc_damage(player)

    def reset_angle_check(self):
        if self.player.id in {3, 4} and self.player.direction.x == 0:
            PlayerBullet.rotation = 0

    def init_image(self, player, angle):
        img_level = max(player.weapon_level // 2, 1)
        self.image = GFX[f'bt{player.id}{img_level}']
        rot_angle = angle - 90  # angle with positive y axis as 0 deg
        self.image = pygame.transform.rotate(self.image, rot_angle)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.rect.inflate_ip(-5, -5)  # Adjust the hitbox of the bullet to avoid bs hits

    def calc_damage(self, player):
        if player.id in {1, 2}:
            self.damage = 1 + player.weapon_level / 2.0
        else:
            self.damage = 0.8 + player.weapon_level / 2.0

    def update(self):
        self.reset_angle_check()
        self.pos += self.direction
        self.rect.center = tuple(self.pos)
        self.check_oob()

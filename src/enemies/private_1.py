# coding=utf-8
from math import degrees

import pygame

from src.bullets.private_bullet import PrivateBullet
from src.components.PVector import PVector
from src.constants import GFX, HEIGHT
from src.enemies.enemy import Enemy
from src.special_effects.enemy_explosion import EnemyExplosion
from src.items.coin import Coin


class Private1(Enemy):
    speed = 2

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.health = 20
        self.target = self.find_target_pos()
        self.image = GFX['e_private1_body']
        self.orig_image = GFX['e_private1_body']
        self.turret_image = GFX['e_private1_turret']
        self.gun_image = GFX['e_private1_gun']
        self.direction = PVector(0, Private1.speed)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.radius = self.image.get_width() / 2

        self.hitbox.image = pygame.Surface((40, 40))
        self.hitbox.rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        self.bullet_pos: PVector = None

    def move(self):
        #print("Moving")
        self.pos += self.direction
        self.rect.center = tuple(self.pos)
        self.hitbox.rect.center = tuple(self.pos)
        self.target = self.find_target_pos()

    def update_img(self):
        angle = self.pos.angle_to(self.target)  # radians
        self.bullet_pos = self.pos.project(angle, self.radius)
        rot_ang = degrees(angle) + 90
        self.image = self.orig_image.copy()
        o_dim = PVector.from_tuple(self.turret_image.get_size())
        rot_turret_image = pygame.transform.rotate(self.turret_image.copy(), rot_ang)
        n_dim = PVector.from_tuple(rot_turret_image.get_size())
        top_left_adjust = (n_dim - o_dim) / 2
        # explanation: when we rotate an image, new padding will be automatically added to fit the new dimensions.
        # Pygame blits images using top left.
        # This means the original "center" will be moved to somewhere that's not the center.
        # To be precise, it will be shifted (n.width-o.width)/2 pixels right,
        # since "extra" padding is added to the right and the left extra space.
        # It will also be shifted the same value down. Therefore we shift the center back.
        self.image.blit(rot_turret_image, tuple(-top_left_adjust))
        self.image.blit(self.gun_image, (0, 0))

    def check_death(self):
        if self.rect.top >= HEIGHT:
            self.kill()
            self.hitbox.kill()

        if self.health <= 0:
            EnemyExplosion(self.game, self)
            Coin(self.game, self.pos - PVector(10, 10))
            Coin(self.game, self.pos + PVector(10, 10))
            self.kill()
            self.hitbox.kill()

    def check_shoot(self):
        if self.frame % 90 >= 60 and self.frame % 6 == 1:  # fire 5 times
            # print("shoot")
            PrivateBullet(self.game, self.bullet_pos, self.target)

# coding=utf-8
from itertools import cycle

import pygame

from src.bullets.enemy_weapons import SecondLieutenantWeapon1
from src.constants import GFX
from src.enemies.second_lieutenant_0 import SecondLieutenant0


class SecondLieutenant1(SecondLieutenant0):
    firing_positions = (-88, -50, -13, 24, 60)

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.image = GFX['e_secondlieutenant1']
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.hitbox.image = pygame.Surface((50, 180))
        self.hitbox.rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        self.effect_img = cycle([GFX['e_00{}{}'.format(x // 10, x % 10)] for x in range(1, 16)])
        self.effect_image = next(self.effect_img)

    def update_img(self):
        self.image = GFX['e_secondlieutenant1'].copy()  # reset
        if self.frame % 200 > 150:
            x = self.image.get_width() / 2
            y = self.image.get_height() / 2
            for position in self.firing_positions:
                self.image.blit(self.effect_image, (x - 32, y - 32 + position))
                self.effect_image = next(self.effect_img)

    def shoot(self):
        SecondLieutenantWeapon1(self, self.pos)

# coding=utf-8
import pygame

from src.bullets.enemy_weapons import ColonelWeapon2
from src.constants import GFX
from src.enemies.colonel_0 import Colonel0


class Colonel1(Colonel0):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.image = pygame.transform.flip(GFX['e_colonel1'], False, True)
        self.weapon_of_choice = ColonelWeapon2

    def update_img(self):
        self.image = pygame.transform.flip(GFX['e_colonel1'], False, True)
        if self.frame % 200 > 100:
            self.image.blit(self.effect_image, (self.image.get_width() / 2 - 32, self.image.get_height() / 2 - 32))
            self.effect_image = next(self.effect_img)

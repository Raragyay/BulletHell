# coding=utf-8
import pygame

from src.bullets.enemy_weapons import SergeantWeapon1
from src.constants import GFX
from src.enemies.sergeant_0 import Sergeant0


class Sergeant1(Sergeant0):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.image = pygame.transform.flip(GFX['e_sergeant1'], False, True)
        self.weapon = SergeantWeapon1

# coding=utf-8
import pygame

from src.constants import GFX
from src.enemies.first_lieutenant_0 import FirstLieutenant0


class FirstLieutenant1(FirstLieutenant0):  # This one spirals inwards
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.image = pygame.transform.flip(GFX['e_firstlieutenant1'], False, True)
        self.circle_radius_delta = -0.5
        self.initial_radius = 30

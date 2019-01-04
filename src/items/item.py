# coding=utf-8

import pygame

from src.components.PVector import PVector
from src.constants import HEIGHT, WIDTH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.states.level import Level


class Item(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.items)
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None
        self.pos: PVector = pos.copy()
        self.game: Level = game

    def update(self):
        self.move()
        self.update_img()
        self.check_oob()
        self.custom_action()

    def apply_effect(self, player):
        pass

    def check_oob(self):
        a = self.rect
        if a.top > HEIGHT or a.bottom < 0 or a.left > WIDTH or a.right < 0:
            # print("dead")
            self.kill()

    def move(self):
        pass

    def update_img(self):
        pass

    def custom_action(self):
        pass

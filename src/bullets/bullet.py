# coding=utf-8
import pygame

from src.constants import HEIGHT, WIDTH


class Bullet(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.rect: pygame.Rect = None
        self.image: pygame.Surface = None

    def check_oob(self):
        a = self.rect
        if a.top > HEIGHT or a.bottom < 0 or a.left > WIDTH or a.right < 0:
            self.kill()

    def update(self):
        pass

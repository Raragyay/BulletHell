# coding=utf-8
import pygame

from src.constants import WIDTH, HEIGHT


class Transition:
    def __init__(self):
        self.mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.alpha_start = 0
        self.alpha_target = 255
        self.frame = 0

    def draw(self, surface: pygame.Surface):
        surface.blit(self.mask, (0, 0))

    def fade_in(self):
        self.frame += 1
        if self.frame <= 51:  # 51*5=255, at that point no need to continue changing the mask
            # This way, we can keep on calling transition fade-in in update loop which won't do anything if its
            # already faded in.
            self.mask.fill((0, 0, 0, self.alpha_target - self.frame * 5))

    def fade_out(self):
        self.alpha_start += 5
        self.mask.fill((0, 0, 0, self.alpha_start))
        return self.alpha_start == self.alpha_target

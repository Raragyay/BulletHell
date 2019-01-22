# coding=utf-8
from random import randint, choice

import pygame
from pygame.sprite import Sprite

from src.components.PVector import PVector
from src.constants import GFX, HEIGHT, WIDTH


class StageTransition:
    def __init__(self, level_num):
        self.image = GFX[f'stage{level_num}']
        self.particles = pygame.sprite.Group()
        for y in range(0, self.image.get_height(), 2):
            for x in range(0, self.image.get_width(), 2):
                if self.image.get_at((x, y))[3] != 0:  # If there is non-transparent pixel at that location
                    Particle(self, PVector(x + WIDTH // 2 - self.image.get_width() // 2, y + 200))

    def update(self):
        self.particles.update()
        print(len(self.particles))

    def draw(self, surface):
        self.particles.draw(surface)


class Particle(Sprite):
    frames_to_group = 120
    group_time = 60

    def __init__(self, transition, target_pos: PVector, ):
        super().__init__(transition.particles)
        self.target_pos = target_pos
        self.speed = PVector(randint(1, 10) * choice([-1, 1]), randint(1, 10) * choice([-1, 1]))
        self.pos = self.target_pos - self.speed * self.frames_to_group

        self.image = GFX['particle']
        self.rect = self.image.get_rect(center=tuple(self.pos))

        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame <= self.frames_to_group:
            self.pos += self.speed
        elif self.frame > self.frames_to_group + self.group_time:
            self.pos -= self.speed
            self.check_oob()
        self.rect.center = tuple(self.pos)

    def check_oob(self):
        a = self.rect
        if a.top > HEIGHT or a.bottom < 0 or a.left > WIDTH or a.right < 0:
            self.kill()

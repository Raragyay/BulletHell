# coding=utf-8
from random import randint

import pygame

from src.constants import GFX, HEIGHT, WIDTH


class Background:
    star_num = 20

    def __init__(self, level_num):
        self.stars = pygame.sprite.Group()
        self.image = GFX[f'bg{level_num}']
        self.image_height = self.image.get_height()
        self.camera_y = self.image_height - HEIGHT  # Start at bottom
        self.bg_image = pygame.Surface((WIDTH, HEIGHT))
        self.bg_move_timer = 5
        self.bg_image.blit(self.image.subsurface(0, self.camera_y, WIDTH, HEIGHT), (0, 0))

        for i in range(self.star_num):
            x = randint(0, WIDTH)
            y = randint(0, HEIGHT)
            speed = randint(1, 4)
            Star(x, y, speed, self.stars)

    def draw(self, surface):
        surface.blit(self.bg_image, (0, 0))
        self.stars.draw(surface)

    def update(self):
        self.bg_move_timer -= 1
        if self.bg_move_timer <= 0:
            self.bg_move_timer = 5
            self.camera_y -= 1
            if self.camera_y < 0:
                self.camera_y = self.image_height - HEIGHT  # reset
            self.bg_image.blit(self.image.subsurface(0, self.camera_y, WIDTH, HEIGHT), (0, 0))
        self.stars.update()
        for _ in range(self.star_num - len(self.stars)):
            x = randint(0, WIDTH)
            y = 0
            speed = randint(1, 4)
            Star(x, y, speed, self.stars)


class Star(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, speed, *group):
        super().__init__(*group)
        assert 1 <= speed <= 4
        self.speed = speed
        self.image = pygame.Surface((speed, speed), pygame.SRCALPHA)
        self.rect: pygame.Rect = None
        if self.speed == 1:
            self.image.fill((255, 255, 255, 175))  # square
        elif self.speed == 2:
            pygame.draw.circle(self.image, (255, 255, 255, 175), (1, 1), 1)  # cicle
        elif self.speed == 3:
            self.image.fill((255, 255, 255, 175))  # big sqiare
        elif self.speed == 4:
            pygame.draw.circle(self.image, (255, 255, 255, 200), (2, 2), 2)  # big more transparent circle
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

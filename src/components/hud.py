# coding=utf-8
from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

import pygame

from src.components.label import Label
from src.constants import WIDTH, HEIGHT, ARCADE_CLASSIC, GFX

if TYPE_CHECKING:
    from src.states.level import Level


class Hud:
    def __init__(self, game: Level):
        self.game = game
        self.layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self.labels = pygame.sprite.Group()
        texts = ['player 1', 'high score', 'player 2']
        rect_attributes = ['topleft', 'midtop', 'topright']
        rect_vals = [(0, 0), (WIDTH // 2, 0), (WIDTH, 0)]
        text_colours = [(199, 42, 224), (255, 10, 10), (7, 7, 240)]
        for text, attr, pos, col in zip(texts, rect_attributes, rect_vals, text_colours):
            Label(text, {attr: pos}, self.labels, font_path=ARCADE_CLASSIC, text_colour=col, font_size=25)

        self.player_1_label = Label('', {"topleft": (0, 25)}, self.labels, font_path=ARCADE_CLASSIC, font_size=25)
        self.player_2_label = Label('', {'topright': (WIDTH, 25)}, self.labels, font_path=ARCADE_CLASSIC, font_size=25)

        self.player_1_life: pygame.Surface = None
        self.player_2_life: pygame.Surface = None
        self.bomb_img = GFX['bomb1']

        # Shouldn't assign player 1 and player 2 because it could be created by game,
        # changing the pointer in game but not in hud

    def update(self):
        self.set_player_life_pictures()
        self.update_labels()

    def draw(self, surface):
        self.layer.fill((0, 0, 0, 0))
        self.labels.draw(self.layer)
        self.draw_player_lives()
        self.draw_bomb_num()
        surface.blit(self.layer,(0,0))

    def update_labels(self):
        p1 = self.game.player_1
        if p1.alive():
            p1_text = f'{p1.score}'
        elif self.game.player_1_choose:
            if self.game.choice['1p'] == 1:
                ship_type = 'cricket'
            else:
                ship_type = 'locust'
            p1_text = f'{ceil(self.game.player_1_choose_time/60)} ??{ship_type}??'
        else:
            if self.game.coins > 0:
                p1_text = 'press 1p start'
            else:
                p1_text = 'insert coin'
        self.player_1_label.update_text(p1_text)


        p2 = self.game.player_2
        if p2.alive():
            p2_text = f'{p2.score}'
        elif self.game.player_2_choose:
            if self.game.choice['2p'] == 2:
                ship_type = 'cricket'
            else:
                ship_type = 'locust'
            p2_text = f'{ceil(self.game.player_2_choose_time/60)} ??{ship_type}??'
        else:
            if self.game.coins > 0:
                p2_text = 'press 2p start'
            else:
                p2_text = 'insert coin'
        self.player_2_label.update_text(p2_text)

    def set_player_life_pictures(self):
        scale = lambda x: pygame.transform.scale(GFX[x], (20, 30))
        if self.game.player_1.alive():
            self.player_1_life = scale(f'player{self.game.player_1.id}')
        if self.game.player_2.alive():
            self.player_2_life = scale(f'player{self.game.player_2.id}')

    def draw_player_lives(self):
        if self.game.player_1.alive():
            for i in range(self.game.player_1.lives - 1):  # 1 life left should show no lives
                self.layer.blit(self.player_1_life, (10 + i * 30, 70))

        if self.game.player_2.alive():
            for i in range(self.game.player_2.lives - 1):
                self.layer.blit(self.player_1_life, (600 - 30 - i * 30, 70))

    def draw_bomb_num(self):
        if self.game.player_1.alive():
            for i in range(self.game.player_1.bomb_num):
                self.layer.blit(self.bomb_img, (i * 30, HEIGHT - 30))

        if self.game.player_2.alive():
            for i in range(self.game.player_2.bomb_num):
                self.layer.blit(self.bomb_img, (WIDTH - 30 - i * 30, HEIGHT - 30))

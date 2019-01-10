# coding=utf-8
from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from src.components.label import Label
from src.constants import WIDTH, HEIGHT, ARCADE_CLASSIC

if TYPE_CHECKING:
    from src.states.level import Level


class Hud:
    def __init__(self, game: Level):
        self.game = game
        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.labels = pygame.sprite.Group()
        texts = ['player 1', 'high score', 'player 2']
        rect_attributes = ['topleft', 'midtop', 'topright']
        rect_vals = [(0, 0), (WIDTH // 2, 0), (WIDTH, 0)]
        text_colours = [(199, 42, 224), (255, 10, 10), (7, 7, 240)]
        for text,attr,pos,col in zip(texts,rect_attributes,rect_vals,text_colours):
            Label(text,{attr:pos},self.labels,font_path=ARCADE_CLASSIC,text_colour=col,font_size=25)

        self.player_1_label = Label('', {"topleft": (0, 25)}, self.labels, font_path=ARCADE_CLASSIC, font_size=25)
        self.player_2_label = Label('', {'topright': (WIDTH, 25)}, self.labels, font_path=ARCADE_CLASSIC, font_size=25)

        # Shouldn't assign player 1 and player 2 because it could be created by game,
        # changing the pointer in game but not in hud

    def update(self):
        self.update_labels()

    def draw(self, surface):
        self.labels.draw(surface)

    def update_labels(self):
        p1 = self.game.player_1
        if p1.alive():
            p1_text = f'{p1.score}'
        elif self.game.player_1_choose:
            if self.game.choice['1p'] == 1:
                ship_type = 'cricket'
            else:
                ship_type = 'locust'
            p1_text = f'{self.game.player_1_choose_time} ??{ship_type}??'
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
            p2_text = f'{self.game.player_2_choose_time} ??{ship_type}??'
        else:
            if self.game.coins > 0:
                p2_text = 'press 1p start'
            else:
                p2_text = 'insert coin'
        self.player_2_label.update_text(p2_text)

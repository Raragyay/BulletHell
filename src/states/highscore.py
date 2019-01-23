# coding=utf-8
import json
from typing import List

import pygame

from src.components.background import Background
from src.components.label import Label
from src.components.transition import Transition
from src.constants import GFX, SCORE, ANCIENT_MEDIUM, ARCADE_CLASSIC
from src.states.state import State


class Highscore(State):
    def __init__(self):
        super().__init__()
        self.background = Background(5)
        self.labels = pygame.sprite.Group()
        self.scoreboard: dict = None
        self.title = GFX['scoreboard']
        self.title_rect = self.title.get_rect(center=(300, 100))
        self.transition = Transition()
        self.next = 'TITLE'
        self.fade_away = False
        self.images = [pygame.transform.scale(GFX[f'player{x}'], (40, 60)) for x in range(1, 5)]

    def startup(self, persist: dict):
        self.frame = 0
        self.done = False
        self.transition = Transition()
        self.fade_away = False
        self.persist = persist
        with open(SCORE, 'r') as f:
            self.scoreboard = json.load(f)
        self.labels = pygame.sprite.Group()
        self.init_labels()
        self.controls = self.persist['controls']

    def cleanup(self):
        return self.persist.copy()

    def init_labels(self):
        ranks = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th']
        colours = [(234, 199, 135), (233, 233, 216), (186, 110, 64), (118, 119, 120), (118, 119, 120), (118, 119, 120),
                   (118, 119, 120)]
        # Gold, silver, bronze, grey, grey, because last place doesn't get anything :)
        pos_1 = [(150, 250 + y * 80) for y in range(len(self.scoreboard))]
        pos_2 = [(220, 250 + y * 80) for y in range(len(self.scoreboard))]
        pos_3 = [(550, 250 + y * 80) for y in range(len(self.scoreboard))]
        for rank, bottom_left, colour in zip(ranks, pos_1, colours):
            Label(rank, {
                'bottomleft': bottom_left}, self.labels, font_path=ANCIENT_MEDIUM, font_size=40, text_colour=colour)

        for entry, bottom_left, colour in zip(self.scoreboard, pos_2, colours):  # Name
            Label(entry[0], {
                'bottomleft': bottom_left}, self.labels, font_path=ARCADE_CLASSIC,
                  font_size=40,
                  text_colour=colour)

        for entry, bottom_left, colour in zip(self.scoreboard, pos_3, colours):  # Score
            Label(str(entry[2]), {
                'bottomleft': bottom_left}, self.labels, font_path=ARCADE_CLASSIC,
                  font_size=40,
                  text_colour=colour)

    def blit_player_images(self, surface):
        for idx, entry in enumerate(self.scoreboard):
            surface.blit(self.images[entry[1] - 1], (50, 200 + idx * 80))

    def update(self):
        self.frame += 1
        self.transition.fade_in()
        if self.frame >= 300:
            self.fade_away = True
        if self.fade_away:
            self.done = self.transition.fade_out()
        self.background.update()

    def draw(self, surface):
        self.background.draw(surface)
        self.blit_player_images(surface)
        surface.blit(self.title, self.title_rect)
        self.labels.draw(surface)
        self.transition.draw(surface)

    def event_process(self, events: List[pygame.event.Event]):
        pass

from typing import List

import pygame

from src.components.background import Background
from src.components.label import Label
from src.components.text_input import TextInput
from src.components.transition import Transition
from src.constants import ARCADE_CLASSIC, GFX
from src.states.state import State


class Entername(State):
    def __init__(self):
        super().__init__()
        self.background = Background(1)
        self.text_input = TextInput(font_family=ARCADE_CLASSIC, font_size=50, text_color=(255, 255, 255),
                                    cursor_color=(255, 255, 255), max_length=15)
        self.next = 'HIGHSCORE'
        self.scoreboard = {}
        self.p1_done = False
        self.p2_done = False
        self.event_block = False
        self.p1_idx = 0
        self.p2_idx = 0
        self.fade_away = False
        self.transition = Transition()

        self.title = GFX['entername']
        self.title_rect = self.title.get_rect(center=(300, 100))
        self.prompt_label: Label = None

    def startup(self, persist: dict):
        self.frame = 0
        self.done = False
        self.persist = persist
        self.text_input.reset()
        self.scoreboard = persist['scoreboard']
        self.check_done()
        self.fade_away = False
        self.transition = Transition()
        self.event_block = False
        self.prompt_label = Label('', {
            'center': (300, 200)}, font_path=ARCADE_CLASSIC, font_size=40)

    def cleanup(self):
        return {
            'coins'     : self.persist['coins'],
            'controls'  : self.persist['controls'],
            'scoreboard': self.scoreboard}

    def event_process(self, events: List[pygame.event.Event]):
        if self.event_block:
            return
        if self.text_input.update(events):
            if not self.p1_done:
                self.p1_done = True
                self.scoreboard[self.p1_idx][0] = self.text_input.get_text()
                self.text_input.reset()
            if not self.p2_done:
                self.p2_done = True
                self.scoreboard[self.p2_idx][0] = self.text_input.get_text()
                self.text_input.reset()

    def update(self):
        self.background.update()
        if self.p1_done and self.p2_done:
            self.event_block = True
            self.fade_away = True
            self.sort_scoreboard()
        if self.fade_away:
            self.done = self.transition.fade_out()
        self.update_labels()

    def draw(self, surface):
        self.background.draw(surface)
        input_surface = self.text_input.get_surface()
        input_rect = input_surface.get_rect(center=(300, 400))
        surface.blit(input_surface, input_rect)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.prompt_label.image, self.prompt_label.rect)

    def check_done(self):
        self.p1_done = True
        self.p2_done = True
        for idx, entry in enumerate(self.scoreboard):
            if entry[0] == 'player_1':
                self.p1_idx = idx
                self.p1_done = False
            if entry[0] == 'player_2':
                self.p2_idx = idx
                self.p2_done = False

    def sort_scoreboard(self):
        self.scoreboard = sorted(self.scoreboard, key=lambda entry: entry[2], reverse=True)

    def update_labels(self):
        if not self.p1_done:
            self.prompt_label.update_text('Enter Player 1 Name')
        elif not self.p2_done:
            self.prompt_label.update_text('Enter Player 2 Name')
        else:
            self.prompt_label.update_text('Thank you for playing')


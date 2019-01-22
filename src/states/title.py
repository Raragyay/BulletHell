# coding=utf-8
import json
from typing import List

import pygame

from src.components.label import Label, BlinkerLabel
from src.components.transition import Transition
from src.constants import GFX, ARCADE_CLASSIC, CONTROLS, SFX
from src.states.state import State


class Title(State):
    def __init__(self):
        super().__init__()
        self.background = GFX['title_bg']  # TODO make custom background
        self.coins = 0
        self.fade_away = False
        self.event_block = False
        self.transition = Transition()

        self.coin_label: Label = None
        self.control_label: Label = None
        self.hint_label: BlinkerLabel = None
        self.labels = pygame.sprite.Group()

        self.make_labels()
        self.choice = {'1p': 0, '2p': 0}

        self.screen_saver = 0

    def startup(self, persist: dict):
        self.done = False
        self.persist = persist
        self.choice = self.persist.get('choice', {'1p': 0, '2p': 0})
        self.coins = self.persist.get('coins', 0)
        self.frame = 0
        # TODO MUsic
        with open(CONTROLS, 'r') as f:
            self.controls = self.persist.get('controls', json.load(f))
        self.transition = Transition()
        self.fade_away = False
        self.event_block = False

    def cleanup(self):
        # TODO Finish music
        persist = {'controls': self.controls, 'choice': self.choice, 'coins': self.coins}
        return persist

    def update(self):
        self.frame += 1
        self.screen_saver += 1
        self.transition.fade_in()
        # If we have waited for 5 seconds, not transitioning
        if self.screen_saver == 300 and not self.fade_away:
            self.fade_away = True
            # self.next ='SCORE' TODO
        if self.fade_away:
            self.done = self.transition.fade_out()
        elif self.transition.frame > 0:
            self.transition = Transition()  # Reset fadeaway
        self.update_labels()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.labels.draw(surface)
        self.transition.draw(surface)

    def update_labels(self):
        self.coin_label.update_text(f'credit {self.coins}')

    def make_labels(self):
        self.coin_label = Label(f'credit {self.coins}',
                                {'midbottom': (300, 750)},
                                self.labels,
                                font_path=ARCADE_CLASSIC,
                                text_colour=(255, 255, 255),
                                font_size=25)

    def event_process(self, events: List[pygame.event.Event]):
        if self.event_block: return
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.screen_saver = 0
                if event.key == pygame.K_TAB:
                    self.fade_away = True
                    self.event_block = True
                    # TODO change to controls screen

                if event.key in {self.controls['1p_coin'], self.controls['2p_coin']}:
                    SFX['coin'].play()
                    self.coins += 1

                if event.key == self.controls['1p_start']:
                    if self.coins >= 1:
                        self.coins -= 1
                        self.choice['1p'] = 1
                        self.fade_away = True
                        self.event_block = True
                        self.next = 'SELECT'

                if event.key == self.controls['2p_start']:
                    if self.coins >= 1:
                        self.coins -= 1
                        self.choice['2p'] = 2
                        self.fade_away = True
                        self.event_block = True
                        self.next = 'SELECT'

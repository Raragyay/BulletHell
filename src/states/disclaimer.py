# coding=utf-8
import json
from typing import List

import pygame

from src.states.state import State
from src.constants import CONTROLS, GFX
from src.components.transition import Transition


class Disclaimer(State):
    def __init__(self):
        super().__init__()
        self.next = 'LEVEL 1'  # TODO SWITCH TO OTHER STATE
        self.bg = GFX['warning']
        self.timer = 300
        self.frame = 0
        self.transition: Transition = Transition()

    def startup(self, persist: dict):
        self.persist = persist

    def cleanup(self):
        with open(CONTROLS, 'r') as file:
            self.persist["controls"] = json.load(file)
        self.persist['coins'] = 0
        return self.persist

    def event_process(self, events: List[pygame.event.Event]):
        pass

    def update(self):
        self.done = True  # TODO REMOPVE
        self.transition.fade_in()
        self.frame += 1
        if self.frame > 150:  # After fade in for sure
            self.done = self.transition.fade_out()

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.transition.draw(surface)
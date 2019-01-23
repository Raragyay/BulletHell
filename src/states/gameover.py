# coding=utf-8
import json
from typing import List

import pygame

from src.components.background import Background
from src.components.stage_transition import StageTransition
from src.constants import SCORE
from src.states.state import State


class Gameover(State):
    def __init__(self):
        super().__init__()
        self.transition = StageTransition(6)
        self.scoreboard = []
        self.next = 'NAME'

    def startup(self, persist: dict):
        self.transition = StageTransition(6)
        self.persist = persist
        with open(SCORE, 'r') as f:
            self.scoreboard = json.load(f)
        if self.persist['player_1'].alive():
            self.scoreboard.append(['player_1', self.persist['player_1'].id, self.persist['player_1'].score])
        if self.persist['player_2'].alive():
            self.scoreboard['player_2'].append(['player_2', self.persist['player_2'].id, self.persist[
                'player_2'].score])

        self.done = False
        self.frame = 0

    def cleanup(self):
        persist = {
            'coins'     : self.persist['coins'],
            'controls'  : self.persist['controls'],
            'scoreboard': self.scoreboard}
        return persist

    def event_process(self, events: List[pygame.event.Event]):
        pass

    def update(self):
        self.transition.update()
        self.frame += 1
        if self.frame == 150:
            self.done = True

    def draw(self, surface):
        surface.fill((0,0,0))
        self.transition.draw(surface)

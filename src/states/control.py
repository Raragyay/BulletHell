# coding=utf-8
import json
from typing import List

import pygame

from src.components.label import BlinkerLabel
from src.components.transition import Transition
from src.constants import GFX, ARCADE_CLASSIC, CONTROLS
from src.states.state import State


class Control(State):
    def __init__(self):
        super().__init__()
        self.background = GFX['controls']
        self.transition = Transition()
        self.next = 'TITLE'
        self.fade_away = False

        self.labels = pygame.sprite.Group()
        self.label_list: List[BlinkerLabel] = []

        self.changing_label = False
        self.chosen_control = 0

        self.texts = ['1p_coin', '1p_start', '1p_up', '1p_down', '1p_left', '1p_right', '1p_button_a', '1p_button_b',
                      '2p_coin', '2p_start', '2p_up', '2p_down', '2p_left', '2p_right', '2p_button_a', '2p_button_b']

    def startup(self, persist: dict):
        self.labels = pygame.sprite.Group()
        self.persist = persist
        self.changing_label = False
        self.done = False
        self.controls = self.persist['controls']
        self.chosen_control = 0
        self.transition = Transition()
        self.fade_away = False
        self.init_labels()

    def cleanup(self):
        persist = {
            'controls': self.controls,
            'coins'   : self.persist['coins']
        }
        return persist

    def init_labels(self):
        self.label_list: List[BlinkerLabel] = []
        label_centers = [(150 + x * 300, 360 + y * 50) for x in range(2) for y in range(8)]
        for name, center in zip(self.texts, label_centers):
            self.label_list.append(BlinkerLabel(pygame.key.name(self.controls[name]), {
                'center': center}, 30, self.labels, font_path=ARCADE_CLASSIC, font_size=25))

    def update(self):
        print(self.chosen_control)
        self.transition.fade_in()
        self.update_labels()
        if self.fade_away:
            self.done = self.transition.fade_out()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.labels.draw(surface)
        self.transition.draw(surface)

    def update_labels(self):
        for idx, label in enumerate(self.label_list):
            if idx == self.chosen_control:
                if self.changing_label:
                    label.fill_colour = (255, 255, 0)
                    label.text_colour = (0, 0, 0)
                    label.blink()
                else:
                    label.fill_colour = (255, 255, 255)
                    label.text_colour = (0, 0, 0)
                    label.text = label.original_text
            else:
                label.fill_colour = None
                label.text_colour = (255, 255, 255)
            label.update_img()

    def update_control(self, key):
        selected_label = self.label_list[self.chosen_control]
        name = pygame.key.name(key)
        selected_label.original_text = name
        self.controls[self.texts[self.chosen_control]] = key

    def event_process(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Save controls
                    with open(CONTROLS, 'w') as f:
                        json.dump(self.controls, f)
                    self.fade_away = True
                if not self.changing_label:
                    if event.key == pygame.K_RETURN:
                        self.changing_label = True
                    if event.key == pygame.K_UP:
                        if self.chosen_control % 8 > 0:
                            self.chosen_control -= 1
                    if event.key == pygame.K_DOWN:
                        if self.chosen_control % 8 < 7:
                            self.chosen_control += 1
                    if event.key == pygame.K_RIGHT:
                        if self.chosen_control < 8:  # Left column
                            self.chosen_control += 8
                    if event.key == pygame.K_LEFT:
                        if self.chosen_control >= 8:
                            self.chosen_control -= 8
                else:
                    if event.key == pygame.K_RETURN:
                        self.changing_label = False
                    elif event.key == pygame.K_ESCAPE:
                        pass
                    else:
                        self.update_control(event.key)

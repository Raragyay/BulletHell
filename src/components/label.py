# coding=utf-8
import copy
from typing import Dict

import pygame

from src.constants import LOADED_FONTS


class Label(pygame.sprite.Sprite):
    LABEL_DEFAULTS = {
        "font_path"  : None,
        "font_size"  : 12,
        "text_colour": (255, 255, 255),
        "alpha"      : 255

    }  # To add to as new come up

    def __init__(self, text: str, rect_attr: Dict, *groups, **settings):
        super().__init__(*groups)
        self.text_colour: tuple = None
        self.alpha: int = None
        self.font_size: int = None
        self.font_path: str = None
        self.kwarg_set(Label.LABEL_DEFAULTS, settings)

        self.text: str = text

        self.rect_attr: Dict = rect_attr
        if (self.font_path, self.font_size) not in LOADED_FONTS:
            LOADED_FONTS[(self.font_path, self.font_size)] = pygame.font.Font(self.font_path, self.font_size)

        self.font: pygame.font.Font = LOADED_FONTS[(self.font_path, self.font_size)]

        self.image: pygame.Surface = None
        self.rect: pygame.Surface = None

        self.update_text(text)

    def update_text(self, new_text):
        self.text = new_text
        self.update_img()

    def kwarg_set(self, default: Dict, custom: Dict):
        default_copy = copy.deepcopy(default)
        for setting in default_copy.keys():
            if setting in custom:
                default_copy[setting] = custom[setting]
            setattr(self, setting, default_copy[setting])

    def update_img(self):
        render_args = (self.text, True, self.text_colour)
        self.image: pygame.Surface = self.font.render(*render_args)  # Unpack tuple as arguments
        self.rect = self.image.get_rect(**self.rect_attr)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

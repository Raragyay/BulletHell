# coding=utf-8
import os

import pygame

from src.components.tools import load_graphics, load_music, load_maps, load_sfx, load_fonts

WIDTH = 600
HEIGHT = 800
SCREENRECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.display.set_mode((WIDTH, HEIGHT))

BASE_FOLDER = os.path.join(os.path.dirname(__file__), r'..')
RESOURCE_FOLDER = os.path.join(BASE_FOLDER, r'resources')
GRAPHICS_FOLDER = os.path.join(RESOURCE_FOLDER, r'graphics')
MUSIC_FOLDER = os.path.join(RESOURCE_FOLDER, r'music')
MAPS_FOLDER = os.path.join(RESOURCE_FOLDER, r'maps')
SFX_FOLDER = os.path.join(RESOURCE_FOLDER, r'sound')
FONTS_FOLDER = os.path.join(RESOURCE_FOLDER, r'fonts')
CONTROLS = os.path.join(RESOURCE_FOLDER, 'controls.json')
SCORE = os.path.join(RESOURCE_FOLDER, 'scoreboard.json')

GFX = load_graphics(GRAPHICS_FOLDER)
MUSIC = load_music(MUSIC_FOLDER)
MAPS = load_maps(MAPS_FOLDER)
SFX = load_sfx(SFX_FOLDER)
FONTS = load_fonts(FONTS_FOLDER)

ARCADE_CLASSIC = FONTS['ARCADECLASSIC']
ANCIENT_MEDIUM = FONTS['Ancient Medium']
GAMER = FONTS['Gamer']
LOADED_FONTS = {}

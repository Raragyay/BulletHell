# coding=utf-8
import json
import os
from typing import Dict, List

import pygame


def load_graphics(directory):
    os.chdir(directory)
    graphics: Dict[str, pygame.Surface] = {}
    for pic in os.listdir(directory):
        name, extension = os.path.splitext(pic)
        img: pygame.Surface = pygame.image.load(pic)
        if img.get_alpha:  # If it already has transparency
            img = img.convert_alpha()
        else:
            img = img.convert()
            img.set_alpha((0, 0, 0))  # transparent if black background
        graphics[name] = img
    return graphics


def load_music(directory):
    os.chdir(directory)
    songs: Dict[str, str] = {}
    for music in os.listdir(directory):
        name, extension = os.path.splitext(music)
        songs[name] = os.path.join(directory, music)
    return songs

def load_maps(directory):
    os.chdir(directory)
    maps = {}
    for map in os.listdir(directory):
        name, ext = os.path.splitext(map)
        file = os.path.join(directory, map)
        with open(file, 'r') as f:
            maps[name] = json.load(f)
    return maps

def load_sfx(directory):
    """Load all sfx of extensions found in accept.  Unfortunately it is
    common to need to set sfx volume on a one-by-one basis.  This must be done
    manually if necessary in the setup module."""
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        effects[name] = pygame.mixer.Sound(os.path.join(directory, fx))
    return effects

def subsurfaces(surface: pygame.Surface, start: tuple, size: tuple, columns: int, rows: int = 1):
    surfaces: List[pygame.Surface] = []
    for row in range(rows):
        for col in range(columns):
            location = (start[0] + size[0] * col, start[1] + size[1] * row)
            surfaces.append(surface.subsurface(pygame.Rect(location, size)))
    return surfaces



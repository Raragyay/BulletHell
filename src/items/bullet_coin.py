# coding=utf-8
from __future__ import annotations
from typing import TYPE_CHECKING
from src.items.coin import Coin

if TYPE_CHECKING:
    from src.States.level import Level


class BulletCoin(Coin):
    def __init__(self, game: Level, pos):
        super().__init__(game, pos)
        self.value /= 10

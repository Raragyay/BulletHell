# coding=utf-8
from src.bullets.sergeant_bullet import SergeantBullet


class SergeantWeapon0:
    def __init__(self, enemy, pos, target):
        SergeantBullet(-60, target, enemy.game, pos)
        SergeantBullet(-40, target, enemy.game, pos)
        SergeantBullet(-20, target, enemy.game, pos)
        SergeantBullet(20, target, enemy.game, pos)
        SergeantBullet(40, target, enemy.game, pos)
        SergeantBullet(60, target, enemy.game, pos)


class SergeantWeapon1:
    def __init__(self, enemy, pos, target):
        SergeantBullet(-60, target, enemy.game, pos)
        SergeantBullet(-30, target, enemy.game, pos)
        SergeantBullet(0, target, enemy.game, pos)
        SergeantBullet(30, target, enemy.game, pos)
        SergeantBullet(60, target, enemy.game, pos)

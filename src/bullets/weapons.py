# coding=utf-8
from src.components.PVector import PVector
from src.bullets.player_bullet import PlayerBullet
from src.bullets.player_laser_bullet import PlayerLaserBullet


class PlayerWeapon1:
    front_weapon = PVector(9, 0)
    back_weapon = PVector(24,0)
    back_offset=PVector(0,20)


    def __init__(self, player):
        level = player.weapon_level
        group = player.bullets
        if level == 1:  # TODO Add more levels
            PlayerBullet(player, 90, self.front_weapon, group)
            PlayerBullet(player, 90, -self.front_weapon, group)
        elif level == 2:
            PlayerBullet(player, 90, self.front_weapon, group)
            PlayerBullet(player, 90, -self.front_weapon, group)
            PlayerBullet(player, 90, self.back_weapon+self.back_offset, group)
            PlayerBullet(player, 90, -self.back_weapon+self.back_offset, group)


class PlayerWeapon2:
    def __init__(self, player):
        level = player.weapon_level
        group = player.bullets

        PlayerLaserBullet(player, group)

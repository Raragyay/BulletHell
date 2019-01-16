# coding=utf-8
from src.bullets.player_homing_bullet import PlayerHomingBullet
from src.components.PVector import PVector
from src.bullets.player_bullet import PlayerBullet
from src.bullets.player_laser_bullet import PlayerLaserBullet

front_weapon = PVector(9, 0)
back_weapon = PVector(24, 0)
back_offset = PVector(0, 20)


class PlayerWeapon1:
    def __init__(self, player):
        level = player.weapon_level
        if level == 1:  # TODO Add more levels
            PlayerBullet(player, 90, front_weapon, 1)
            PlayerBullet(player, 90, -front_weapon, 1)
        elif level == 2:
            PlayerBullet(player, 90, front_weapon, 1)
            PlayerBullet(player, 90, -front_weapon, 1)
            PlayerBullet(player, 90, back_weapon + back_offset, 1)
            PlayerBullet(player, 90, -back_weapon + back_offset, 1)
        elif level == 3:
            PlayerBullet(player, 80, front_weapon, 1)
            PlayerBullet(player, 100, front_weapon, 1)
            PlayerBullet(player, 80, -front_weapon, 1)
            PlayerBullet(player, 100, -front_weapon, 1)
            PlayerBullet(player, 90, back_weapon + back_offset, 1)
            PlayerBullet(player, 90, -back_weapon + back_offset, 1)
        elif level == 4:
            PlayerBullet(player, 80, front_weapon, 1)
            PlayerBullet(player, 100, front_weapon, 1)
            PlayerBullet(player, 80, -front_weapon, 1)
            PlayerBullet(player, 100, -front_weapon, 1)
            PlayerBullet(player, 90, back_weapon + back_offset, 2)
            PlayerBullet(player, 90, -back_weapon + back_offset, 2)
            HomingWeapon4(player)
        elif level == 5:
            PlayerBullet(player, 75, front_weapon, 1)
            PlayerBullet(player, 90, front_weapon, 2)
            PlayerBullet(player, 105, front_weapon, 1)
            PlayerBullet(player, 75, -front_weapon, 1)
            PlayerBullet(player, 90, -front_weapon, 2)
            PlayerBullet(player, 105, -front_weapon, 1)
            PlayerBullet(player, 90, back_weapon + back_offset, 2)
            PlayerBullet(player, 90, -back_weapon + back_offset, 2)
            HomingWeapon4(player)



class HomingWeapon:
    cooldown = 4

    def __init__(self, player):
        HomingWeapon.cooldown -= 1
        if HomingWeapon.cooldown <= 0:
            self.fire(player)
            HomingWeapon.cooldown = 4

    def fire(self, player):
        raise NotImplementedError("Do not create a raw homing weapon")


class HomingWeapon4(HomingWeapon):
    def __init__(self, player):
        super().__init__(player)

    def fire(self, player):
        PlayerHomingBullet(player, back_weapon + back_offset, 2)
        PlayerHomingBullet(player, -back_weapon + back_offset, 2)
class PlayerWeapon2:
    def __init__(self, player):
        PlayerLaserBullet(player)

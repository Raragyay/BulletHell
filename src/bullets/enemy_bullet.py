# coding=utf-8
from src.bullets.bullet import Bullet
from src.components.PVector import PVector


class EnemyBullet(Bullet):
    def __init__(self, pos, game):
        super().__init__(game.enemy_bullets)
        self.pos:PVector = pos
        self.frame=0

    def update(self):
        self.frame+=1
        self.check_oob()
        self.move()
        self.update_img()
        self.custom_action()

    def move(self):
        pass

    def custom_action(self):
        pass

    def update_img(self):
        pass


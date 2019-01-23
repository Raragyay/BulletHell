# coding=utf-8
from src.enemies.boss_1 import Boss1
from src.enemies.corporal_0 import Corporal0
from src.enemies.first_lieutenant_0 import FirstLieutenant0
from src.enemies.first_lieutenant_1 import FirstLieutenant1
from src.enemies.private_0 import Private0
from src.enemies.private_1 import Private1
from src.enemies.second_lieutenant_0 import SecondLieutenant0
from src.enemies.second_lieutenant_1 import SecondLieutenant1
from src.enemies.sergeant_0 import Sergeant0
from src.enemies.sergeant_1 import Sergeant1
from src.special_effects.warning_sign import WarningSign

enemy_dict = {
    "1" : Private0,
    "2" : Private1,
    "3" : Corporal0,
    "4" : Sergeant0,
    "5" : Sergeant1,
    "6" : SecondLieutenant0,
    "7" : SecondLieutenant1,
    "8" : FirstLieutenant0,
    "9" : FirstLieutenant1,
    "16": Boss1,
    "21":WarningSign
}

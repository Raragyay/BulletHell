# coding=utf-8
from src.enemies.boss_1 import Boss1
from src.enemies.captain_0 import Captain0
from src.enemies.captain_1 import Captain1
from src.enemies.colonel_0 import Colonel0
from src.enemies.colonel_1 import Colonel1
from src.enemies.corporal_0 import Corporal0
from src.enemies.first_lieutenant_0 import FirstLieutenant0
from src.enemies.first_lieutenant_1 import FirstLieutenant1
from src.enemies.private_0 import Private0
from src.enemies.private_1 import Private1
from src.enemies.second_lieutenant_0 import SecondLieutenant0
from src.enemies.second_lieutenant_1 import SecondLieutenant1
from src.enemies.sergeant_0 import Sergeant0
from src.enemies.sergeant_1 import Sergeant1
from src.special_effects.emerge_1 import Emerge1
from src.special_effects.emerge_2 import Emerge2
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
    "10": Captain0,
    "11": Captain1,
    "14": Colonel0,
    "15": Colonel1,
    "16": Boss1,
    "21": Emerge1,
    "22": Emerge2,
    "23": WarningSign
}

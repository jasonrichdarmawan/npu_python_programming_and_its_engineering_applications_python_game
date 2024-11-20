import random
from fighter_jet import FighterJet
from game_window import GAME_WINDOW_WIDTH

def create_enemy_fighter_jet() -> FighterJet:
    x = random.randint(0, GAME_WINDOW_WIDTH)
    enemy = FighterJet("enemy", 3, x, 0, None)
    return enemy
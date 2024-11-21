from typing import Callable
from bullet import Bullet
from fighter_jet import FighterJet
import random
from game_window import GAME_WINDOW

def create_fighter_jet(type: str, append_bullet_in_flight: Callable[[Bullet], None]) -> FighterJet:
    x = random.randint(0, GAME_WINDOW.get_width())
    y = random.randint(0, GAME_WINDOW.get_height())
    fighter_jet = FighterJet(type, 5, x, y, 1000, append_bullet_in_flight)
    return fighter_jet
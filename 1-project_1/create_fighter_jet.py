from fighter_jet import FighterJet
import random
from game_window import GAME_WINDOW

def create_fighter_jet(type: str) -> FighterJet:
    x = random.randint(0, GAME_WINDOW.get_width())
    match type:
        case "enemy":
            y = random.randint(0, 100)
        case "fighter_1" | "fighter_2":
            y = random.randint(GAME_WINDOW.get_height() - 100, GAME_WINDOW.get_height())
    fighter_jet = FighterJet(type, 5, x, y, 1000)
    return fighter_jet
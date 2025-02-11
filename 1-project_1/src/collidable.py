from .moveable import Moveable
from .renderable import Renderable

class Collidable(Moveable, Renderable):
    def __init__(self, speed: int, x: int, y: int, name: str):
        Moveable.__init__(self, speed, x, y)
        Renderable.__init__(self, name)
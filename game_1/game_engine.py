from fighter_jet import FighterJet
from moveable import Moveable
import pygame
from game_window import GAME_WINDOW
from bullet import Bullet
from direction import Direction
from create_enemy_fighter_jet import create_enemy_fighter_jet

class GameEngine:
    def __init__(self):
        self.player_fighter_jet: FighterJet = None
        self.enemy_fighter_jets: list[FighterJet] = []
        self.bullets_in_flight: list[Bullet] = []

    def append_bullet_in_flight(self, bullet: Bullet):
        self.bullets_in_flight.append(bullet)

    def update_state(self):
        self.__check_collisions()
        for obj in self.enemy_fighter_jets:
            obj.move(Direction.DOWN)
            if obj.y >= obj.bottom_boundary:
                self.enemy_fighter_jets.remove(obj)
                self.enemy_fighter_jets.append(create_enemy_fighter_jet())
        for obj in self.bullets_in_flight:
            obj.move()
            if obj.y < 0:
                self.bullets_in_flight.remove(obj)

    # TODO: local check_collisions method
    def __check_collisions(self):
        for enemy_fighter_jet in self.enemy_fighter_jets:
            if self.__is_colliding(self.player_fighter_jet, enemy_fighter_jet):
                self.player_fighter_jet = None
                self.enemy_fighter_jets.remove(enemy_fighter_jet)
                continue

            for bullet in self.bullets_in_flight:
                if self.__is_colliding(bullet, enemy_fighter_jet):
                    self.bullets_in_flight.remove(bullet)
                    self.enemy_fighter_jets.remove(enemy_fighter_jet)

    def __is_colliding(self, obj1: Moveable, obj2: Moveable):
        rect1 = pygame.Rect(obj1.x, obj1.y, obj1.image.get_width(), obj1.image.get_width())
        rect2 = pygame.Rect(obj2.x, obj2.y, obj2.image.get_width(), obj2.image.get_height())
        return rect1.colliderect(rect2)

    def update_screen(self):
        if self.player_fighter_jet is not None:
            GAME_WINDOW.blit(self.player_fighter_jet.image, (self.player_fighter_jet.x, self.player_fighter_jet.y))
        for enemy_fighter_jet in self.enemy_fighter_jets:
            GAME_WINDOW.blit(enemy_fighter_jet.image, (enemy_fighter_jet.x, enemy_fighter_jet.y))
        for bullet_in_flight in self.bullets_in_flight:
            GAME_WINDOW.blit(bullet_in_flight.image, (bullet_in_flight.x, bullet_in_flight.y))
        pygame.display.update()


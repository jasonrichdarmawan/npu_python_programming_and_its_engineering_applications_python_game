from fighter_jet import FighterJet
import pygame
from game_window import GAME_WINDOW
from bullet import Bullet
from direction import Direction
from create_fighter_jet import create_fighter_jet
from collidable import Collidable

class GameEngine:
    def __init__(self):
        self.player_fighter_jet: FighterJet = None
        self.enemy_fighter_jets: list[FighterJet] = []
        self.bullets_in_flight: list[Bullet] = []

    def append_bullet_in_flight(self, bullet: Bullet):
        self.bullets_in_flight.append(bullet)

    def update_state(self):
        self.__handle_collisions()
        self.__update_enemies_state()
        self.__update_bullets_state()

    # TODO: local
    def __handle_collisions(self):
        # Check if any bullet is colliding with any fighter jet
        fighter_jets: list[Collidable] = []
        fighter_jets.append(self.player_fighter_jet)
        fighter_jets.extend(self.enemy_fighter_jets)
        fighter_jets_to_remove: list[Collidable] = []
        for fighter_jet in fighter_jets:
            for bullet in self.bullets_in_flight:
                if self.__is_colliding(bullet, fighter_jet):
                    fighter_jets_to_remove.append(fighter_jet)
                    self.bullets_in_flight.remove(bullet)
                    break

        for fighter_jet in fighter_jets_to_remove:
            if fighter_jet == self.player_fighter_jet:
                self.player_fighter_jet = create_fighter_jet("fighter_2", self.append_bullet_in_flight)
            else:
                self.enemy_fighter_jets.remove(fighter_jet)

        # Check if player fighter jet is colliding with any enemy fighter jet
        if self.player_fighter_jet is None:
            return
        for enemy in self.enemy_fighter_jets:
            if self.__is_colliding(self.player_fighter_jet, enemy):
                self.player_fighter_jet = create_fighter_jet("fighter_2", self.append_bullet_in_flight)
                self.enemy_fighter_jets.remove(enemy)
                break

    def __is_colliding(self, obj1: Collidable, obj2: Collidable):
        obj1_image = obj1.get_image()
        rect1 = pygame.Rect(obj1.x, obj1.y, obj1_image.get_width(), obj1_image.get_height())

        obj2_image = obj2.get_image()
        rect2 = pygame.Rect(obj2.x, obj2.y, obj2_image.get_width(), obj2_image.get_height())
        return rect1.colliderect(rect2)
    
    def __update_enemies_state(self):
        if self.enemy_fighter_jets == []:
            self.enemy_fighter_jets.append(create_fighter_jet("enemy", self.append_bullet_in_flight))
        for enemy in self.enemy_fighter_jets:
            enemy.move(Direction.DOWN)
            if enemy.x >= enemy.get_right_boundary() or enemy.y >= enemy.get_bottom_boundary():
                self.enemy_fighter_jets.remove(enemy)
                self.enemy_fighter_jets.append(create_fighter_jet("enemy", self.append_bullet_in_flight))

    def __update_bullets_state(self):
        for bullet in self.bullets_in_flight:
            bullet.move()
            if bullet.y < 0:
                self.bullets_in_flight.remove(bullet)

    def update_screen(self):
        GAME_WINDOW.fill((0,0,0))
        if self.player_fighter_jet is not None:
            GAME_WINDOW.blit(self.player_fighter_jet.get_image(), (self.player_fighter_jet.x, self.player_fighter_jet.y))
        for enemy_fighter_jet in self.enemy_fighter_jets:
            GAME_WINDOW.blit(enemy_fighter_jet.get_image(), (enemy_fighter_jet.x, enemy_fighter_jet.y))
        for bullet_in_flight in self.bullets_in_flight:
            GAME_WINDOW.blit(bullet_in_flight.get_image(), (bullet_in_flight.x, bullet_in_flight.y))
        pygame.display.update()


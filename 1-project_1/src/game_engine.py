from .fighter_jet import FighterJet
from .game_window import GAME_WINDOW
from .bullet import Bullet
from .direction import Direction
from .create_fighter_jet import create_fighter_jet
from .collidable import Collidable
from .moveable import Moveable
import pygame

class GameEngine:
    def __init__(self, player_fighter_jet: FighterJet, 
                 enemy_fighter_jets: list[FighterJet]):
        self.running = True
        self.player_fighter_jet = player_fighter_jet
        self.player_fighter_jet.set_append_bullet_in_flight(self.append_bullet_in_flight)
        self.enemy_fighter_jets = enemy_fighter_jets
        for enemy_fighter_jet in self.enemy_fighter_jets:
            enemy_fighter_jet.set_append_bullet_in_flight(self.append_bullet_in_flight)
        self.bullets_in_flight: list[Bullet] = []

    def append_bullet_in_flight(self, bullet: Bullet):
        self.bullets_in_flight.append(bullet)

    def update_state(self):
        self.__handle_collisions()
        self.__update_enemies_state()
        if self.player_fighter_jet is None:
            self.player_fighter_jet = self.__make_player_fighter_jet()
        self.__update_bullets_state()

    def update_screen(self):
        GAME_WINDOW.fill((0,0,0))
        if self.player_fighter_jet is not None:
            position = self.player_fighter_jet.get_position()
            GAME_WINDOW.blit(self.player_fighter_jet.get_image(), position)
        for enemy_fighter_jet in self.enemy_fighter_jets:
            position = enemy_fighter_jet.get_position()
            GAME_WINDOW.blit(enemy_fighter_jet.get_image(), position)
        for bullet_in_flight in self.bullets_in_flight:
            position = bullet_in_flight.get_position()
            GAME_WINDOW.blit(bullet_in_flight.get_image(), position)
        pygame.display.update()

    def __handle_collisions(self):
        # Check if any bullet is colliding with any fighter jet
        fighter_jets: list[Collidable] = []
        if self.player_fighter_jet is not None:
            fighter_jets.append(self.player_fighter_jet)
        fighter_jets.extend(self.enemy_fighter_jets)
        for fighter_jet in fighter_jets:
            for bullet in self.bullets_in_flight:
                if self.__is_colliding(bullet, fighter_jet):
                    if fighter_jet == self.player_fighter_jet:
                        self.player_fighter_jet = None
                    else:
                        self.enemy_fighter_jets.remove(fighter_jet)
                    self.bullets_in_flight.remove(bullet)
                    break

        # Check if player fighter jet is colliding with any enemy fighter jet
        if self.player_fighter_jet is None:
            return
        for enemy in self.enemy_fighter_jets:
            if self.__is_colliding(self.player_fighter_jet, enemy):
                self.player_fighter_jet = None
                self.enemy_fighter_jets.remove(enemy)
                break

    def __is_colliding(self, obj1: Collidable, obj2: Collidable):
        obj1_x, obj1_y = obj1.get_position()
        obj1_image = obj1.get_image()
        rect1 = pygame.Rect(obj1_x, obj1_y, obj1_image.get_width(), 
                            obj1_image.get_height())

        obj2_x, obj2_y = obj2.get_position()
        obj2_image = obj2.get_image()
        rect2 = pygame.Rect(obj2_x, obj2_y, obj2_image.get_width(), 
                            obj2_image.get_height())
        return rect1.colliderect(rect2)
    
    def __make_player_fighter_jet(self) -> FighterJet:
        player_fighter_jet = create_fighter_jet("fighter_2")
        player_fighter_jet.set_append_bullet_in_flight(self.append_bullet_in_flight)
        return player_fighter_jet
    
    def __update_enemies_state(self):
        if self.enemy_fighter_jets == []:
            new_enemy = self.__make_enemy_fighter_jet()
            self.enemy_fighter_jets.append(new_enemy)
        for enemy in self.enemy_fighter_jets:
            self.__make_enemy_decision(enemy)
            x, y = enemy.get_position()
            if (x <= 0 or x >= enemy.get_right_boundary() or 
                y <= 0 or y >= enemy.get_bottom_boundary()):
                self.enemy_fighter_jets.remove(enemy)
                new_enemy = self.__make_enemy_fighter_jet()
                self.enemy_fighter_jets.append(new_enemy)
    
    def __make_enemy_fighter_jet(self) -> FighterJet:
        enemy = create_fighter_jet("enemy")
        enemy.set_append_bullet_in_flight(self.append_bullet_in_flight)
        return enemy

    def __make_enemy_decision(self, fighter_jet: FighterJet):
        decision = self.__try_shoot_with(fighter_jet)

        if decision: return
        
        direction = fighter_jet.get_direction()
        fighter_jet.move(direction)

    def __try_shoot_with(self, fighter_jet: FighterJet) -> bool:
        if self.player_fighter_jet is None:
            return False

        player_x, player_y = self.player_fighter_jet.get_position()
        enemy_x, enemy_y = fighter_jet.get_position()
        x_abs = abs(player_x - enemy_x)
        x_range = 5
        y_abs = abs(player_y - enemy_y)
        y_range = 5
        if x_abs <= x_range or y_abs <= y_range:
            player_direction_relative_to_enemy = self.__get_relative_direction_to(self.player_fighter_jet, fighter_jet, x_range, y_range)
            fighter_jet.move(player_direction_relative_to_enemy)
            fighter_jet.shoot()
            return True
        
        return False

    def __get_relative_direction_to(self, fighter_jet1: Moveable, 
                                    fighter_jet2: Moveable, 
                                    x_range: int, y_range: int) -> Direction:
        fighter_jet1_x, fighter_jet1_y = fighter_jet1.get_position()
        fighter_jet2_x, fighter_jet2_y = fighter_jet2.get_position()

        x_abs = abs(fighter_jet1_x - fighter_jet2_x)
        y_abs = abs(fighter_jet1_y - fighter_jet2_y)

        if x_abs <= x_range:
            if fighter_jet1_y > fighter_jet2_y:
                return Direction.DOWN
            else: return Direction.UP
        elif y_abs <= y_range:
            if fighter_jet1_x > fighter_jet2_x:
                return Direction.RIGHT
            else: return Direction.LEFT

    def __update_bullets_state(self):
        for bullet in self.bullets_in_flight:
            bullet.move()
            x, y = bullet.get_position()
            if (x <= 0 or 
                x >= GAME_WINDOW.get_width() or 
                y <= 0 or 
                y >= GAME_WINDOW.get_height()):
                self.bullets_in_flight.remove(bullet)


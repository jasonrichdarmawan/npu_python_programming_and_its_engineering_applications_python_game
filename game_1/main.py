# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 14:44:55 2024

@author: HP
"""

import pygame
from game_window import GAME_WINDOW
from fighter_jet import FighterJet
from direction import Direction
from create_enemy_fighter_jet import create_enemy_fighter_jet
from game_engine import GameEngine

def initialize_game_engine() -> GameEngine:
    "初始化Pygame Initializing Pygame"
    pygame.init()
    game_engine = GameEngine()
    player_fighter_jet = FighterJet("fighter_2", 5, 100, 1000, game_engine.append_bullet_in_flight)
    enemy_fighter_jets = [create_enemy_fighter_jet()]
    game_engine.player_fighter_jet = player_fighter_jet
    game_engine.enemy_fighter_jets = enemy_fighter_jets
    return game_engine

def handle_player_input(player_fighter_jet: FighterJet):
    "Handle player input"
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_fighter_jet.move(direction=Direction.LEFT)
    if keys[pygame.K_RIGHT]:
        player_fighter_jet.move(direction=Direction.RIGHT)
    if keys[pygame.K_SPACE]:
        player_fighter_jet.shoot()

def main_game_loop(game_engine: GameEngine):
    "Main Game Loop"
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60) # 设置帧率为60帧每秒 Set the frame rate to 60 frames per second

        if game_engine.player_fighter_jet is None:
            running = False
            break

        # 处理事件 Handling Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
    
        handle_player_input(game_engine.player_fighter_jet)

        # Update game state
        game_engine.update_state()

        # Update screen
        game_engine.update_screen()

    # 退出游戏
    pygame.quit()

if __name__ == "__main__":
    game_engine = initialize_game_engine()
    main_game_loop(game_engine)
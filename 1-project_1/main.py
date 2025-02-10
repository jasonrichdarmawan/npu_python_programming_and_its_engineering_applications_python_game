# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 14:44:55 2024

@author: HP
"""

import pygame
from fighter_jet import FighterJet
from direction import Direction
from game_engine import GameEngine
from create_fighter_jet import create_fighter_jet

def initialize_game_engine() -> GameEngine:
    "初始化Pygame Initializing Pygame"
    pygame.init()
    player_fighter_jet = create_fighter_jet("fighter_2")
    enemy_fighter_jets = [create_fighter_jet("enemy")]
    game_engine = GameEngine(player_fighter_jet, enemy_fighter_jets)
    return game_engine

def handle_player_input(player_fighter_jet: FighterJet):
    "Handle player input"
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player_fighter_jet.move(direction=Direction.UP)
    elif keys[pygame.K_RIGHT]:
        player_fighter_jet.move(direction=Direction.RIGHT)
    elif keys[pygame.K_DOWN]:
        player_fighter_jet.move(direction=Direction.DOWN)
    elif keys[pygame.K_LEFT]:
        player_fighter_jet.move(direction=Direction.LEFT)
    
    if keys[pygame.K_SPACE]:
        player_fighter_jet.shoot()

def main_game_loop(game_engine: GameEngine):
    "Main Game Loop"
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60) # 设置帧率为60帧每秒 Set the frame rate to 60 frames per second

        # 处理事件 Handling Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
    
        if game_engine.player_fighter_jet is not None:
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
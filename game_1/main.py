# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 14:44:55 2024

@author: HP
"""

import pygame
from game_window import GAME_WINDOW, GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT
from fighter_jet import FighterJet
from direction import Direction
from assets.assets import get_image_metadata
import random

# 初始化Pygame Initializing Pygame
pygame.init()

# 创建战斗机对象 Create a fighter object
fighter = FighterJet("fighter_2", 5, 100, 1000)
x = random.randint(0, GAME_WINDOW_WIDTH)
enemy_1 = FighterJet("enemy", 3, x, 0)

enemies = [enemy_1]

# 游戏主循环 Main Game Loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)  # 设置帧率为60帧每秒 Set the frame rate to 60 frames per second
    GAME_WINDOW.fill((0,0,0))

    # 处理事件 Handling Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        fighter.move(direction=Direction.LEFT)
    if keys[pygame.K_RIGHT]:
        fighter.move(direction=Direction.RIGHT)
    if keys[pygame.K_SPACE]:
        fighter.shoot()

    # 移动和绘制敌机 Moving and drawing enemy aircraft
    for enemy in enemies:
        enemy.move(Direction.DOWN)
        enemy.draw()
        if enemy.y >= enemy.bottom_boundary:
            enemies.remove(enemy)
            x = random.randint(0, GAME_WINDOW_WIDTH)
            new_enemy = FighterJet("enemy", 3, x, 0)
            enemies.append(new_enemy)

    # 移动和绘制子弹 Moving and drawing bullets
    for bullet in fighter.bullets:
        bullet.move(Direction.UP)
        bullet.draw()
        if bullet.y < 0:
            fighter.bullets.remove(bullet)

    # 检测碰撞 Detecting collisions
    for bullet in fighter.bullets:
        for enemy in enemies:
            bullet_metadata = get_image_metadata("bullet")
            bullet_width = bullet_metadata["width"]
            bullet_height = bullet_metadata["height"]
            if pygame.Rect(bullet.x, bullet.y, bullet_width, bullet_height).colliderect(
                pygame.Rect(enemy.x, enemy.y, enemy.image_metadata['width'], enemy.image_metadata['height'])
            ):
                fighter.bullets.remove(bullet)
                enemies.remove(enemy)

    # 绘制战斗机 Drawing fighter jets
    fighter.draw()

    # 更新屏幕 Update screen
    pygame.display.update()

# 退出游戏
pygame.quit()
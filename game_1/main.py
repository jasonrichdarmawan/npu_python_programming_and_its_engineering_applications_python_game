# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 14:44:55 2024

@author: HP
"""

import pygame
from game_window import GAME_WINDOW, GAME_WINDOW_HEIGHT
from fighter import Fighter
from bullet import BULLET_WIDTH, BULLET_HEIGHT
from enemy import Enemy, ENEMY_WIDTH, ENEMY_HEIGHT
from direction import Direction

# 初始化Pygame Initializing Pygame
pygame.init()

# 创建战斗机对象 Create a fighter object
fighter = Fighter(5, 100, 1000)
enemy_1 = Enemy()

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
        enemy.move()
        enemy.draw()
        if enemy.y > GAME_WINDOW_HEIGHT:
            enemies.remove(enemy)
            new_enemy = Enemy()
            enemies.append(new_enemy)

    # 移动和绘制子弹 Moving and drawing bullets
    for bullet in fighter.bullets:
        bullet.move()
        bullet.draw()
        if bullet.y < 0:
            fighter.bullets.remove(bullet)

    # 检测碰撞 Detecting collisions
    for bullet in fighter.bullets:
        for enemy in enemies:
            if pygame.Rect(bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT).colliderect(
                pygame.Rect(enemy.x, enemy.y, ENEMY_WIDTH, ENEMY_HEIGHT)
            ):
                fighter.bullets.remove(bullet)
                enemies.remove(enemy)

    # 绘制战斗机 Drawing fighter jets
    fighter.draw()

    # 更新屏幕 Update screen
    pygame.display.update()

# 退出游戏
pygame.quit()
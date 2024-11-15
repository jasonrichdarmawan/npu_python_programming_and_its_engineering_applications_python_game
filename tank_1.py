# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 17:18:03 2024

@author: HP
"""

import pygame
import turtle
import random
import math

# 初始化pygame
pygame.init()

# 游戏窗口大小
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tank Battle Game")

# 颜色定义（修改为turtle能接受的格式）
WHITE = 'white'
GREEN = 'green'
RED = 'red'
BLACK = 'black'

# 坦克类
class Tank:
    def __init__(self, x, y, color, is_player=True):
        self.x = x
        self.y = y
        self.color = color
        self.is_player = is_player
        self.angle = 0
        self.bullets = []
        self.health = 100
        self.turtle_draw()

    def turtle_draw(self):
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(self.x, self.y)
        t.pendown()
        t.color(self.color)
        t.begin_fill()
        for _ in range(2):
            t.forward(30)
            t.right(90)
            t.forward(20)
            t.right(90)
        t.end_fill()
        t.right(self.angle)
        t.penup()
        t.goto(self.x + 15, self.y + 10)
        t.pendown()
        t.begin_fill()
        t.circle(5)
        t.end_fill()
        turtle.update()

    def move_forward(self):
        if self.is_player:
            self.x += math.cos(math.radians(self.angle)) * 2
            self.y += math.sin(math.radians(self.angle)) * 2
        else:
            # 简单的AI移动逻辑，向玩家方向移动
            if player_tank:
                target_angle = math.degrees(math.atan2(player_tank.y - self.y, player_tank.x - self.x))
                if abs(target_angle - self.angle) > 5:
                    if target_angle > self.angle:
                        self.angle += 3
                    else:
                        self.angle -= 3
                self.x += math.cos(math.radians(self.angle)) * 2
                self.y += math.sin(math.radians(self.angle)) * 2

        self.turtle_draw()

    def rotate_left(self):
        if self.is_player:
            self.angle -= 5
            self.turtle_draw()

    def rotate_right(self):
        if self.is_player:
            self.angle += 5
            self.turtle_draw()

    def fire(self):
        bullet = Bullet(self.x + 15, self.y + 10, self.angle, self.is_player)
        self.bullets.append(bullet)

# 子弹类
class Bullet:
    def __init__(self, x, y, angle, is_player):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 5
        self.is_player = is_player

    def move(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 3)

# 创建玩家坦克和敌人坦克
player_tank = Tank(100, 100, GREEN, True)
enemy_tank = Tank(700, 500, RED, False)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_tank.move_forward()
            elif event.key == pygame.K_LEFT:
                player_tank.rotate_left()
            elif event.key == pygame.K_RIGHT:
                player_tank.rotate_right()
            elif event.key == pygame.K_SPACE:
                player_tank.fire()

    
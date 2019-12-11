#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

import numpy as np

from scipy.linalg import solve


class Bone(pygame.sprite.Sprite):
    def __init__(self, img_path):
        super(Bone, self).__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = -100, -100
        self.speed = 30
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.road_number = 0

    def move(self):
        if self.rect.left > 1280 or self.rect.left < -100 or self.rect.top > 800:
            self.active = False
        else:
            self.rect.left, self.rect.top = self.road_x[self.road_number], self.road_y[self.road_number]
            self.road_number += 1

    def update(self, position, power):
        self.rect.left, self.rect.top = position
        self.road_number = 0
        if power > 0:
            self.set_track(position, power)

    def set_track(self, original_position, power):
        a, b, c = self.get_abc(original_position, power)
        if original_position[0] < 650:
            self.road_x = np.arange(self.rect.left, 1500, 50)
        else:
            self.road_x = np.arange(self.rect.left, -200, -50)
        self.road_y = a * self.road_x ** 2 + b * self.road_x + c

    def get_abc(self, original_position, power):
        point1 = [original_position[0] - 15, original_position[1]]
        tag = 1
        if original_position[0] > 650:
            tag = -1
        point2 = [point1[0] + power * 10 * tag, 100]
        point3 = [point1[0] + power * 10 * 2 * tag, point1[1]]
        a = np.array([[point1[0] * point1[0], point1[0], 1],
                      [point2[0] * point2[0], point2[0], 1],
                      [point3[0] * point3[0], point3[0], 1]])
        b = np.array([point1[1], point2[1], point3[1]])
        return solve(a, b)

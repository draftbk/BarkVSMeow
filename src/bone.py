#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

import numpy as np


class Bone(pygame.sprite.Sprite):
    def __init__(self,img_path):
        super(Bone, self).__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = -100, -100
        self.speed = 30
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.road_number = 0

    def move(self):
        if self.rect.left > 1280 or self.rect.left < 0:
            self.active = False
        else:
            self.rect.left, self.rect.top = self.road_x[self.road_number], self.road_y[self.road_number]
            self.road_number += 1

    def update(self, position):
        self.rect.left, self.rect.top = position
        self.road_x = np.arange(self.rect.left, 1500, 50)
        self.road_y = 0.001389 * self.road_x ** 2 - 1.806 * self.road_x + 686.6
        self.road_number = 0

    def cat_update(self, position):
        self.rect.left, self.rect.top = position
        self.road_x = np.arange(self.rect.left, -200, -50)
        self.road_y = 0.001389 * self.road_x ** 2 - 1.806 * self.road_x + 686.6
        self.road_number = 0

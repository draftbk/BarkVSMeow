#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super(Cat, self).__init__()
        self.image = pygame.image.load("material/picture/cat.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = (1160, 570)
        self.active = True
        self.life = 550

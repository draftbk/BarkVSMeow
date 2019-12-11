#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame


class Dog(pygame.sprite.Sprite):
    def __init__(self):
        super(Dog, self).__init__()
        self.image = pygame.image.load("material/picture/dog.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = (20, 570)
        self.active = True
        self.life = 550

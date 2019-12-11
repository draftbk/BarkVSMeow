#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame


class Magic(pygame.sprite.Sprite):
    def __init__(self, picture_path, position):
        super(Magic, self).__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.state = 2

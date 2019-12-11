#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import threading
from pyaudio import PyAudio, paInt16
from config.settings import *
from pygame.locals import *
import numpy as np
from src.dog import Dog
from src.cat import Cat
from src.bone import Bone
from src.magic import Magic

WHITE = (255, 255, 255)

width, height = 1280, 680
bg_size = width, height
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("BarkVSMeow")

all_sprites_list = pygame.sprite.Group()

dog = Dog()
cat = Cat()

magic1 = Magic("material/picture/bigger.png", (625 - 180, 50))
magic2 = Magic("material/picture/times2.png", (625 - 130, 50))
magic3 = Magic("material/picture/times2.png", (625 + 180, 50))
magic4 = Magic("material/picture/bigger.png", (625 + 130, 50))

all_sprites_list.add(dog)
all_sprites_list.add(cat)
all_sprites_list.add(magic1)
# all_sprites_list.add(magic2)
# all_sprites_list.add(magic3)
all_sprites_list.add(magic4)

control = 0

bone = Bone("material/picture/bone.png")
bone.active = False

fish = Bone("material/picture/fish_bone.png")
fish.active = False

font = pygame.font.Font(None, 36)


def main():
    running = True
    delay = 60
    power = 0
    isDogRound = True
    winner = 0
    round_state = 0
    while running:

        screen.fill(WHITE)

        dog_rc = (255, 87, 51)
        dog_rp = (width / 2 - dog.life, 10)
        dog_rs = (dog.life, 20)
        pygame.draw.rect(screen, dog_rc, Rect(dog_rp, dog_rs))

        if isDogRound:
            dog_rc_power = (255, 87, 51)
            dog_rp_power = (dog.rect.left, dog.rect.top)
            dog_rs_power = (power, 5)
            pygame.draw.rect(screen, dog_rc_power, Rect(dog_rp_power, dog_rs_power))
        else:
            cat_rc_power = (255, 87, 51)
            cat_rp_power = (cat.rect.left, cat.rect.top - 5)
            cat_rs_power = (power, 5)
            pygame.draw.rect(screen, cat_rc_power, Rect(cat_rp_power, cat_rs_power))

        cat_rc = (255, 87, 51)
        cat_rp = (width / 2, 10)
        cat_rs = (cat.life, 20)
        pygame.draw.rect(screen, cat_rc, Rect(cat_rp, cat_rs))

        mid_rc = (20, 20, 20)
        mid_rp = (width / 2 - 2, 10)
        mid_rs = (2, 20)
        pygame.draw.rect(screen, mid_rc, Rect(mid_rp, mid_rs))

        all_sprites_list.draw(screen)

        clock = pygame.time.Clock()
        clock.tick(60)

        # collision detection
        cat_hit = pygame.sprite.collide_mask(cat, bone)
        if cat_hit:
            cat.life -= 80
            if magic1.state == 1:
                cat.life -= 160
            if cat.life < 0:
                cat.life = 0
                winner = 2
            bone.update((-200, -100), power)
            bone.active = False

        dog_hit = pygame.sprite.collide_mask(dog, fish)
        if dog_hit:
            dog.life -= 80
            if magic4.state == 1:
                dog.life -= 160
            if dog.life < 0:
                dog.life = 0
                winner = 1
            fish.update((-200, -100), power)
            fish.active = False
        if winner == 1:
            show_text("Cat wins!")
        elif winner == 2:
            show_text("Dog wins!")

        if control == 1 and power == 0:
            if isDogRound and magic1.state == 2:
                magic1.state -= 1
                magic1.rect.left = -100
                bone.image = pygame.image.load("material/picture/big_bone.png")
            elif not isDogRound and magic4.state == 2:
                magic4.state -= 1
                magic4.rect.left = -100
                fish.image = pygame.image.load("material/picture/big_fish_bone.png")

        if control == 2 and not bone.active and not fish.active:
            power += 2
        if control ==0 and power > 0:
            if isDogRound:
                bone.update(dog.rect.center, power)
                bone.active = True
                # reset fish_bone
                if magic4.state == 1 and fish.active == False:
                    fish.image = pygame.image.load("material/picture/fish_bone.png")
                    magic4.state = 0
            else:
                fish.update(cat.rect.center, power)
                fish.active = True
                # reset bone
                if magic1.state == 1 and bone.active == False:
                    bone.image = pygame.image.load("material/picture/bone.png")
                    magic1.state = 0
            power = 0

        for event in pygame.event.get():
            if event.type == 12:
                pygame.quit()
                sys.exit()

        if power > 0:
            power += 2

        if bone.active:
            round_state = 1
            bone.move()
        if fish.active:
            round_state = 1
            fish.move()
        if round_state == 1 and isDogRound and not bone.active:
            isDogRound = False
            round_state = 0
        if round_state == 1 and not isDogRound and not fish.active:
            isDogRound = True
            round_state = 0

        screen.blit(bone.image, bone.rect)
        screen.blit(fish.image, fish.rect)
        if delay == 0:
            delay = 60
        delay -= 1
        pygame.display.flip()


def show_text(message):
    text = font.render(message, True, (25, 25, 25))
    text_rect = text.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text, [text_x, text_y])


def listen_voice(threadName, delay):
    global control
    # voice input
    NUM_SAMPLES = 2000
    SAMPLING_RATE = 8000

    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    while 1:
        string_audio_data = stream.read(NUM_SAMPLES)
        audio_data = np.fromstring(string_audio_data, dtype=np.short)
        value = np.max(audio_data)
        print(value)
        if value >= 30000:
            control = 1
        elif value < 30000 and value >= 2000:
            control = 2
        else:
            control = 0


# create a thread
try:
    threading._start_new_thread(listen_voice, ("voice_listener", 2,))
except:
    print("Error: unable to start thread")

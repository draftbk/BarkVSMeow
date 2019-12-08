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

WHITE = (255, 255, 255)

width, height = 1280, 680
bg_size = width, height
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("BarkVSMeow")

all_sprites_list = pygame.sprite.Group()

dog = Dog(bg_size)
cat = Cat(bg_size)

all_sprites_list.add(dog)
all_sprites_list.add(cat)

control = 0

bone = Bone("material/picture/bone.png")
bone.active = False

fish = Bone("material/picture/fish_bone.png")
fish.active = False


def main():
    running = True
    delay = 60
    power = 0
    isDogRound = True
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
            if cat.life < 0:
                cat.life = 0
            bone.update((-200, -100), power)
            bone.active = False
        dog_hit = pygame.sprite.collide_mask(dog, fish)
        if dog_hit:
            dog.life -= 80
            if dog.life < 0:
                dog.life = 0
            fish.update((-200, -100), power)
            fish.active = False

        if control == 2:
            power += 2
        elif power > 0:
            if isDogRound:
                bone.update(dog.rect.center, power)
                bone.active = True
                isDogRound = False
            else:
                fish.update(cat.rect.center, power)
                fish.active = True
                isDogRound = True
            power = 0

        # 响应用户的操作
        for event in pygame.event.get():
            if event.type == 12:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    power = 1
            elif event.type == KEYUP:
                if power > 0:
                    if isDogRound:
                        bone.update(dog.rect.center, power)
                        bone.active = True
                        isDogRound = False
                    else:
                        fish.update(cat.rect.center, power)
                        fish.active = True
                        isDogRound = True
                    power = 0
        if delay == 0:
            delay = 60
        delay -= 1
        if power > 0:
            power += 2
        if bone.active:
            bone.move()
        if fish.active:
            fish.move()
        screen.blit(bone.image, bone.rect)
        screen.blit(fish.image, fish.rect)
        pygame.display.flip()


# 为线程定义一个函数
def listen_voice(threadName, delay):
    global control
    # voice input
    NUM_SAMPLES = 2000  # pyAudio内部缓存的块的大小
    SAMPLING_RATE = 8000  # 取样频率
    SAVE_LENGTH = 8  # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样

    # 开启声音输入
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    while 1:
        # 读入NUM_SAMPLES个取样
        string_audio_data = stream.read(NUM_SAMPLES)
        # 将读入的数据转换为数组
        audio_data = np.fromstring(string_audio_data, dtype=np.short)
        value = np.max(audio_data)
        print(value)
        if value >= 18000:
            control = 1
        elif value < 18000 and value >= 2500:
            control = 2
        else:
            control = 0


# 创建两个线程
try:
    threading._start_new_thread(listen_voice, ("voice_listener", 2,))
except:
    print("Error: unable to start thread")

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :main.py
@说明    :
@时间    :2020/10/11 17:15:31
@作者    :jeroen
@版本    :1.0
'''

from res import *
import pygame
from pygame.locals import *
import sys


if __name__ == '__main__':
    lrs = LibResSingleton()
    lrs.LoadScn('zhc_house1.Scn')
    map_info = lrs.map_info
    cx = map_info['cx']
    cy = map_info['cy']
    info = map_info['info']

    pygame.init()
    window = pygame.display.set_mode((700, 600))
    window.convert_alpha()
    window.fill((0, 0, 0, 0))
    mu_item = info[3][2]

    while True:
        # surf = pygame.display.set_mode((64, 32))
        surf = pygame.Surface([64, 32], pygame.SRCALPHA)
        surf = surf.convert_alpha()
        surf.fill((0, 0, 0, 0))
        buf = mu_item.combine_buffer
        # print(buf)
        print(buf.shape[0])
        print(buf.shape[1])
        pygame.surfarray.blit_array(surf, buf)
        window.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        pygame.display.flip()

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
    

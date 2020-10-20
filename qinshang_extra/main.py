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
from PIL import Image

if __name__ == '__main__':
    # 初始化资源数据工厂
    lrs = LibResSingleton()
    lrs.LoadScn('zhc_house1.Scn')
    map_info = lrs.map_info
    # 获取 某场景的map数据
    cx = map_info['cx']
    cy = map_info['cy']
    buf = map_info['info']

    # pygame初始化
    pygame.init()
    # 设置窗口大小
    window = pygame.display.set_mode((cx*64, cy*32))
    window.convert_alpha()
    window.fill((0, 0, 0, 0))

    surf = pygame.Surface([64*cx, 32*cy], pygame.SRCALPHA)
    surf.set_colorkey((0, 0, 0))

    # buf绘制到surf
    pygame.surfarray.blit_array(surf, buf)
    # surf 透明化
    surf = surf.convert_alpha()
    window.blit(surf, (0, 0))

    while True:
        # 绘制surf到Windows        
        pygame.display.flip()

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)

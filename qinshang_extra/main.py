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
import pygame, sys, time
from pygame.locals import *
from PIL import Image

if __name__ == '__main__':
    # 初始化资源数据工厂
    lrs = LibResSingleton()
    lrs.LoadScn('zhc_house1.Scn')
    # lrs.LoadScn('zhaocun1.Scn')
    map_info = lrs.map_info
    # 获取 某场景的map数据
    cx = map_info['cx']
    cy = map_info['cy']
    # 获取图片数据
    buf = map_info['info']
    print(buf.shape[0])
    print(buf.shape[1])

    # pygame初始化
    pygame.init()
    # 设置窗口大小
    width = cx * 64
    height = cy * 32
    window = pygame.display.set_mode((width, height))

    surf = pygame.Surface((width, height), pygame.SRCALPHA)

    # buf绘制到surf
    pygame.surfarray.blit_array(surf, buf)
    # surf 透明化
    #surf = surf.convert_alpha()
    # surf = pygame.transform.rotate(surf, 90)
    
    surface_x = 0
    surface_y = 0
    fps_count = 0
    start_fps = time.time()
    clock = pygame.time.Clock()

    while True:
        clock.tick(600)
        now = time.time()
        fps = fps_count / (now - start_fps)
        fps_count += 1

        now = time.time()

        window.blit(surf, (surface_x, surface_y))

        for x in range(6):
            c, d = pygame.mouse.get_pos()  # 鼠标位置
            screen_speed = 10  # 背景移动速度
            if c > 0 and d == 0:
                surface_y += screen_speed
            if c == 0 and d > 0:
                surface_x += screen_speed
            if c > 0 and d == 1079:  # 1920*1080
                surface_y -= screen_speed
            if c == 1919 and d > 0:  # 1920*1080
                surface_x -= screen_speed
            # 如果大于边界
            if surface_x > 0:
                surface_x = 0
            if surface_y > 0:
                surface_y = 0


        # 绘制surf到Windows        
        pygame.display.flip()

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
                
        keys = pygame.key.get_pressed()  # 获取键盘事件
        if keys[K_ESCAPE]:  # 如果按下ESC键
            sys.exit()  # 退出游戏
        pygame.display.update()

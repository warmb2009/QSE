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


if __name__ == '__main__':
    lrs = LibResSingleton()
    lrs.GetResBufferByID(3)
    map_info = lrs.map_info
    
    

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :GamePubicGlobal.py
@说明    :  此文件存储全局变量,如各个文件目录
@时间    :2020/10/11 16:39:47
@作者    :jeroen
@版本    :1.0
'''
import os.path
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

def GetResPath():
    '''
    获取Res lib文件目录
    '''
    return os.path.join(PROJECT_ROOT, '../../datas/Res/')

def GetResIniPath():
    '''
    获取资源对应ID文件
    '''
    return os.path.join(GetResPath(), 'Combination.csv')

def GetMdlPath():
    '''
    获取mdl文件目录
    '''
    return os.path.join(PROJECT_ROOT, '../../datas/mdl/')

def GetScnPath():
    '''
    获取scn文件目录
    '''
    return os.path.join(PROJECT_ROOT, '../../datas/SCENE/Scn_new/')

def GetMapPath():
    '''
    获取map文件目录
    '''
    return os.path.join(PROJECT_ROOT, '../../datas/SCENE/Map')

def GetBntPath():
    '''
    获取bnt文件目录
    '''
    return os.path.join(PROJECT_ROOT, '../../datas/SCENE/Bnt')

def GetOntPath():
    '''
    获取ont文件目录
    '''
    return os.path.join(PROJECT_ROOT, '../../datas/SCENE/Ont')


# 合并两个图块 buf_2 覆盖在buf_1 上面
def combine( buf_1, buf_2):
    width = buf_1.shape[0]
    height = buf_1.shape[1]
    ret_array = np.empty(shape=[width, height, 4], dtype=int)
    for i in range(0, buf_1.shape[0]):
        for j in range(0, buf_1.shape[1]):
            item_1 = buf_1[i][j]
            item_2 = buf_2[i][j]

            ret = item_1
            if (item_2[3] != 0).all():
                ret = item_2
            ret_array[i, j] = ret
    return ret_array

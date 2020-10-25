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


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

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

def GetResPath():
    '''
    获取Res lib文件目录
    '''
    return os.path.join(PROJECT_ROOT, '../../datas/Res/')

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
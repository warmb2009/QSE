#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :map.py
@说明    :此模块用于读取地图的地表数据（地表贴图，是否可走等数据）
@时间    :2020/10/11 16:39:27
@作者    :jeroen
@版本    :1.0
'''


import struct


class BaseClass():
    def printc(self):
        for i, j in vars(self).items():
            print('<--- ' + i + ' : ' + str(j) + ' --->')


class MapResClass(BaseClass):
    '''
    地图资源文件读取
    '''
    class FileHeader(BaseClass):
        '''
        map文件的头文件格式
        '''
        def __init__(self, _style=0, _x=0, _y=0, _tag='', _version=''):
            self.mapstyle = _style
            self.cx = _x
            self.cy = _y
            self.tag = _tag
            self.version = _version

    class LibHeader(BaseClass):
        '''
        所需要的lib文件名称等数据
        '''
        def __init__(self):
            self.libversion = ''
            self.libname = ''
            self.libnum = 0
            self.libsizenum = 0

    class MUObject(BaseClass):
        '''
        地图块数据结构（菱形地图块）
        '''
        def __init__(self):
            self.id_1 = 0
            self.id_2 = 0
            self.btype = 0
            self.team_index = 0
            self.height = 0
            self.terrain = 0
            self.scneffid = 0
            self.buffer_1 = None
            self.buffer_2 = None
            self.combine_buffer = None

    def __init__(self, _file_path):
        self.file_path = _file_path

        self.file_header = None
        self.lib_header = None

        self.index_list = []  # 地图块索引列表
        self.mu_list = []  # 地图块数据列表

        # 地图数据初始化
        self.InitData()

    def read(self, _file_path):
        print(_file_path)
        f = open(_file_path, 'rb')
        return f

    def InitData(self):
        f = self.read(self.file_path)

        # 读取地图文件头部
        self.file_header = self.FileHeader()
        self.file_header.tag = struct.unpack('16c', f.read(16))[0]
        self.file_header.version = struct.unpack('16c', f.read(16))[0]
        self.file_header.mapstyle = int(struct.unpack('h', f.read(2))[0])
        self.file_header.cx = int(struct.unpack('h', f.read(2))[0])
        self.file_header.cy = int(struct.unpack('h', f.read(2))[0])
        f.seek(128)

        self.file_header.printc()

        # 读取所需要的lib数据
        self.lib_header = self.LibHeader()
        self.lib_header.libversion = struct.unpack('16c', f.read(16))[0]

        self.lib_header.libname = str(struct.unpack('256s', f.read(256))[0].split(b'\x00')[0], encoding="gb2312")
        self.lib_header.libnum = int(struct.unpack('h', f.read(2))[0])
        self.lib_header.libsizenum = int(struct.unpack('i', f.read(4))[0])

        num = self.file_header.cx * self.file_header.cy

        # 读取索引块
        while num:
            index = int(struct.unpack('h', f.read(2))[0])
            self.index_list.append(index)
            num -= 1

        # 读取mu数据，放入列表
        while num:
            mu = self.MUObject()
            mu.id_1 = struct.unpack('h', f.read(2))[0]  # 第一层图块 下层
            mu.id_2 = struct.unpack('h', f.read(2))[0]  # 第二层图块 上层
            mu.btype = struct.unpack('c', f.read(1))[0]
            mu.team_index = struct.unpack('c', f.read(1))[0]
            mu.height = struct.unpack('c', f.read(1))[0]
            mu.terrain = struct.unpack('c', f.read(1))[0]
            mu.scneffid = struct.unpack('h', f.read(2))[0]

            self.mu_list.append(mu)
            num -= 1
        f.close()

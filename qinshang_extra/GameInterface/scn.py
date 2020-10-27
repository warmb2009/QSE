#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :scn.py
@说明    :读取scn文件
@时间    :2020/10/18 11:39:54
@作者    :jeroen
@版本    :1.0
'''

import json


class ScnResClass():
    # scn文件的管理类
    def EnterObject(self):
        # 入口点对象类
        self.scene_index = 1
        self.x = 0
        self.y = 0
        self.direction = 0

    def ScnObject(self):
        # Scn文件类
        self.map_name = ''  # map文件名
        self.bnt_name = ''  # bnt文件名 bld
        self.ont_name = ''  # ont文件名 obj

        self.enterpoint = 0
        self.raderid = -1
        self.enters = []  # 存储入口点列表

    def __init__(self, _file_path):
        self.data = None
        self.file_path = _file_path

        self.InitData(self.file_path)

    # 初始化，读取scn文件的内容
    def InitData(self, file_path):
        with open(file_path, 'r') as f:
            self.data = json.loads(f.read())

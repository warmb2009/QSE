#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :scene.py
@说明    :场景管理
@时间    :2020/10/18 12:09:27
@作者    :jeroen
@版本    :1.0
'''

from GameInterface.scn import *
from GameInterface.map import *
from GameInterface.lib import *
import os.path
import numpy as np


class SceneMng():
    def __init__(self):
        self.mpResMng = None
        pass

    def LoadMap(self, file_path):
        self.mpResMng = MapResClass(file_path)
        mu_list = self.mpResMng.mu_list

        # 获取所需要的lib文件
        libname = self.mpResMng.lib_header.libname
        width_count = self.mpResMng.file_header.cx
        height_count = self.mpResMng.file_header.cy
        lib_folder = '/home/jeroen/work/qinshang/QSE/datas/Res/'
        lib_path = os.path.join(lib_folder, libname)

        ql = QinLib(lib_path)
        count = len(mu_list)

        content_list = []
        line_list = []

        for i in range(count):
            if i > 0 and i % width_count == 0:
                content_list.append(line_list)
                line_list = []

            mu_item = mu_list[i]

            index_1 = mu_item.id_1
            index_2 = mu_item.id_2
            mu_item.buffer_1 = ql.get_xbm_image(index_1)
            mu_item.buffer_2 = ql.get_xbm_image(index_2)
            mu_item.combine_buffer = ql.combine(mu_item.buffer_1, mu_item.buffer_2)
            line_list.append(mu_item)

        map_info = {}
        map_info['cx'] = width_count
        map_info['cy'] = height_count
        map_info['info'] = content_list
        return map_info

    def LoadScene(self, file_path):
        SRC = ScnResClass(file_path)
        SrcInfo = SRC.data

        map_name = SrcInfo['map_name']
        bnt_name = SrcInfo['intbld']
        ont_name = SrcInfo['intobj']

        map_folder = '/home/jeroen/work/qinshang/QSE/datas/SCENE/Map/'
        map_path = os.path.join(map_folder, map_name)
        map_array = self.LoadMap(map_path)
        return map_array

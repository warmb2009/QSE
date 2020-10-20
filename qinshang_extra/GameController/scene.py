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
        # 加载map文件
        self.mpResMng = MapResClass(file_path)
        mu_list = self.mpResMng.mu_list

        # 获取所需要的lib文件
        libname = self.mpResMng.lib_header.libname
        width_count = self.mpResMng.file_header.cx
        height_count = self.mpResMng.file_header.cy

        lib_folder = '/home/jeroen/work/qinshang/QSE/datas/Res/'
        lib_path = os.path.join(lib_folder, libname)
        print(libname)
        # 初始化lib类
        ql = QinLib(lib_path)
        count = len(mu_list)

        content_list = []
        line_list = []

        combine_list = []
        combine_line_list = []

        for i in range(count):
            # 遍历行，遍历完一行就进行下一行遍历
            if i > 0 and i % width_count == 0:
                content_list.append(line_list)
                line_list = []

                combine_list.append(combine_line_list)
                combine_line_list = []

            # mu文件
            mu_item = mu_list[i]

            index_1 = mu_item.id_1
            index_2 = mu_item.id_2

            mu_item.buffer_1 = None if index_1 == -1 else ql.get_xbm_image(index_1)
            mu_item.buffer_2 = None if index_2 == -1 else ql.get_xbm_image(index_2)

            combine_buffer = None
            if index_1 == index_2 == -1:
                combine_buffer = None
            elif index_1 == -1:
                combine_buffer = ql.combine_one(mu_item.buffer_2)
            elif index_2 == -1:
                combine_buffer = ql.combine_one(mu_item.buffer_1)
            else:
                combine_buffer = ql.combine(mu_item.buffer_1, mu_item.buffer_2)
            mu_item.combine_buffer = combine_buffer
            combine_line_list.append(combine_buffer)
            line_list.append(mu_item)

        # 建立一个地图数据字典，存储宽高和要显示的图块
        map_info = {}
        map_info['cx'] = width_count
        map_info['cy'] = height_count
        map_info['info'] = self.CombineMap(width_count, height_count, combine_list)
        
        return map_info

    def CombineMap(self, columns, rows, combine_list):
        # 将地图瓦片整合成一个大图
        width = rows * 64
        height = columns * 32

        # 初始化大图矩阵
        print(width, height)
        image_array = np.zeros(shape=[width, height, 3],
                               dtype=int)

        for i in range(32):  # line
            for j in range(64):  # index
                
                x = int(columns * 64 / 2 + j * 32 - i * 32) # 每加一行左移32
                y = int(i * 16 + j * 16 + 16)
                print('index:')
                print(x, y)
                self.draw_tile(x, y, combine_list[i][j], image_array)
        return image_array

    def draw_tile(self, x, y, combine, image_array):
        if combine is None:
            return
        # 绘制瓦片到大图
        print(x, y)
        # 坐标从中心位置转为左上角
        o_x = x - 32 
        o_y = y
        for i in range(32):# 行
            for j in range(64): # 列
                i_x = o_x + i
                i_y = o_y + j
                print(i_x, i_y)
                ori_arr = image_array[i_x][i_y]
                new_arr = combine[j][i]
                
                if not (new_arr == np.array([0, 0, 0])).all():
                    image_array[i_x][i_y] = new_arr

    def LoadScene(self, file_path):
        # 加载scn文件
        SRC = ScnResClass(file_path)
        SrcInfo = SRC.data

        # 获取map信息
        map_name = SrcInfo['map_name']
        bnt_name = SrcInfo['intbld']
        ont_name = SrcInfo['intobj']

        # 加载map文件
        map_folder = '/home/jeroen/work/qinshang/QSE/datas/SCENE/Map/'
        map_path = os.path.join(map_folder, map_name)

        # 读取map文件的图块
        map_array = self.LoadMap(map_path)
        return map_array

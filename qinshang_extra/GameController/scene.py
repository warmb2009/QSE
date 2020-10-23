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
import PIL.Image as Image


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
        print('初始化lib类')
        ql = QinLib(lib_path)
        count = len(mu_list)

        content_list = []
        line_list = []

        combine_list = []
        combine_line_list = []

        line_jishu = 0  # 行计数器
        row_jishu = 0
        print('读取xbm %d 个' % count)

        to_image = Image.new('RGB', (width_count * 64, height_count * 32))
        for i in range(count):
            print(i)
            # 遍历行，遍历完一行就进行下一行遍历
            if i > 0 and i % width_count == 0:
                line_jishu += 1
                row_jishu = 0
                '''
                print('共 %d 行， 读取完一行 %d'% (int(width_count), line_jishu))
                content_list.append(line_list)
                line_list = []

                combine_list.append(combine_line_list)
                combine_line_list = []
                '''

            # mu文件
            mu_item = mu_list[i]

            index_1 = mu_item.id_1
            index_2 = mu_item.id_2
            # 读取xbm
            # print('读取xbm')
            
            # buffer_1 = None if index_1 == -1 else ql.filelist[index_1]['buffer']
            # buffer_2 = None if index_2 == -1 else ql.filelist[index_2]['buffer']
            buffer_1 = None if index_1 == -1 else ql.get_xbm_image(index_1)
            buffer_2 = None if index_2 == -1 else ql.get_xbm_image(index_2)

            combine_buffer = None
            if index_1 == index_2 == -1:
                combine_buffer = None
                continue
            elif index_1 == -1:
                combine_buffer = buffer_2
            elif index_2 == -1:
                combine_buffer = buffer_1
            else:
                combine_buffer = ql.combine(buffer_1, buffer_2)
            # mu_item.combine_buffer = combine_buffer
            #print(combine_buffer)
            from_image = Image.fromarray(np.uint8(combine_buffer))

            x = int(width_count * 64 / 2 + row_jishu * 32 - line_jishu * 32)  # 每加一行左移32
            y = int(line_jishu * 16 + row_jishu * 16 + 16)
            #print(x,y)
            to_image.paste(from_image, (x, y), mask=[0,0,0])

            #combine_line_list.append(combine_buffer)
            #line_list.append(mu_item)
            row_jishu += 1
            '''
        if i == count - 1:
            # pass
            combine_list.append(combine_line_list)
            '''
        print('读取完毕')
        # 建立一个地图数据字典，存储宽高和要显示的图块
        map_info = {}
        map_info['cx'] = width_count
        map_info['cy'] = height_count
        # return to_image
        # map_info['info'] = self.CombineMap(width_count, height_count, combine_list)
        map_info['info'] = np.array(to_image)
        return map_info

    def CombineMap(self, columns, rows, combine_list):
        print('合成大图')
        # 将地图瓦片整合成一个大图
        width = rows * 64
        height = columns * 32

        for i in range(rows):  # line
            for j in range(columns):  # index
                print(combine_array)
                combine_array = combine_list[i][j]
                
                from_image = Image.fromarray(combine_array.astype('uint8')).convert('RGB')

                x = int(columns * 64 / 2 + j * 32 - i * 32 - 32)  # 每加一行左移32
                y = int(i * 16 + j * 16)

                to_image.paste(from_image, (x, y))

        '''
        # 初始化大图矩阵
        #print(width, height)
        image_array = np.zeros(shape=[width, height, 3],
                               dtype=int)

        for i in range(rows):  # line
            for j in range(columns):  # index

                x = int(columns * 64 / 2 + j * 32 - i * 32) # 每加一行左移32
                y = int(i * 16 + j * 16 + 16)

                # 绘制瓦片
                self.draw_tile(x, y, combine_list[i][j], image_array, i, j)
        print('合成完毕')
        '''
        return image_array

    def draw_tile(self, x, y, combine, image_array, i, j):
        # 绘制瓦片到大图
        if combine is None:
            return
        #print(combine)
        #print(combine.shape[0])
        #print(combine.shape[1])
        # 坐标从中心位置转为左上角
        o_x = x - 32 
        o_y = y - 16
        # print('o_x:%d, o_y:%d' % (o_x, o_y))
        for i in range(32):# 行
            for j in range(64): # 列
                i_x = o_x + j
                i_y = o_y + i

                # print(i_x, i_y)
                ori_arr = image_array[i_x][i_y]
                new_arr = combine[i][j]
                # 空白处为新值
                if not (new_arr == [0, 0, 0]).all():
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

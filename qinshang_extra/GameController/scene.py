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
from GameInterface.bnt import *
from GameInterface.mdl import *
from GameInterface.lib import *
from GameInterface.rci import *

import os.path
import numpy as np
import PIL.Image as Image
from GameInterface.gameglobal import *

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

        # 加载lib资源
        lib_folder = GetResPath()
        lib_path = os.path.join(lib_folder, libname)
        print(libname)
        # 初始化lib类
        print('初始化lib类')
        ql = QinLib(lib_path)
        count = len(mu_list)

        line_jishu = 0  # 行计数器
        row_jishu = 0
        print('读取xbm %d 个' % count)

        to_image = Image.new('RGB', (width_count * 64, height_count * 32))

        for i in range(count):
            # print(i)
            # 遍历行，遍历完一行就进行下一行遍历
            if i > 0 and i % width_count == 0:
                line_jishu += 1
                row_jishu = 0

            # mu文件
            mu_item = mu_list[i]

            index_1 = mu_item.id_1
            index_2 = mu_item.id_2

            # 读取xbm
            buffer_1 = None if index_1 == -1 else ql.get_image(index_1)
            buffer_2 = None if index_2 == -1 else ql.get_image(index_2)

            combine_buffer = None
            if index_1 == index_2 == -1:  # 空瓦块
                combine_buffer = None
            elif index_1 == -1:
                combine_buffer = buffer_2
            elif index_2 == -1:
                combine_buffer = buffer_1
            else:
                combine_buffer = ql.combine(buffer_1, buffer_2)

            if combine_buffer is not None:  # 非空瓦块才画上，空瓦块跳过
                from_image = Image.fromarray(np.uint8(combine_buffer), mode='RGBA')

                x = int(width_count * 64 / 2 + row_jishu * 32 - line_jishu * 32)  # 每加一行左移32
                y = int(line_jishu * 16 + row_jishu * 16 + 16)
                r, g, b, a = from_image.split()  # 分离出透明通道
                to_image.paste(from_image, (x, y), a)  # 画瓦块
            row_jishu += 1

        print('读取完毕')
        # 建立一个地图数据字典，存储宽高和要显示的图块
        map_info = {}
        map_info['cx'] = width_count
        map_info['cy'] = height_count
        
        # 维度反了 行、列交换
        np_image_array = np.array(to_image).swapaxes(1, 0)
        im = Image.fromarray(np.array(to_image))
        im.save('ut.jpeg')
        map_info['info'] = np_image_array
        return map_info

    def CombineMap(self, columns, rows, combine_list):
        print('合成大图')
        # 将地图瓦片整合成一个大图
        width = rows * 64
        height = columns * 32

        for i in range(rows):  # line
            for j in range(columns):  # index
                #print(combine_array)
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

    def LoadBnt(self, file_path):
        #bnt文件读取
        bldResMng = BntResClass(file_path)

        # 读取mdl文件
        mdl_name = bldResMng.file_header.mdl_name
        mdl_path = os.path.join(GetMdlPath(), mdl_name)
        mdl_res = MdlResClass(mdl_path)

        mdltolib = {}
        mdltolib['BUILDING.MDL'] = 'Bei.lib'
        mdltolib['dong.Mdl'] = 'DONG.lib'
        mdltolib['snow.Mdl'] = 'snow.lib'
        mdltolib['house.Mdl'] = 'house.lib'

        lib_folder = GetResPath()
        lib_path = os.path.join(lib_folder, mdltolib[mdl_name])
        print(lib_path)
        # 初始化lib类
        print('初始化lib类')
        

        # 初始化资源ID转换类
        rm = ResMng(GetResIniPath())
        

        num = 0
        for mdl_info in bldResMng.mdl_list:
            print('第%d 个部件' % num)
            pos_x = mdl_info.gp_map_pos_x
            pos_y = mdl_info.gp_map_pos_y

            auto_id = mdl_info.iModelAutoID
            
            # 获取部件数据
            mdlres_info = mdl_res.get(auto_id)
            print(mdlres_info.szName)
            print('子部件数量：%d' % mdlres_info.PartNum)
            print(mdlres_info.booIsAnimate)
            for bld_item in mdlres_info.PartMng:
                print('子部件 start')
                # 子部件位置 图片id
                m_dPicID = bld_item.m_dPicID
                pos_x = bld_item.m_pos_x
                pos_y = bld_item.m_pos_y

                
                # 进行子部件图片加载
                #libname, libid, libfilename = rm.get(m_dPicID)
                libname, libid, libfilename = rm.get(m_dPicID)
                path = os.path.join( GetResPath(), libfilename)

                print(m_dPicID)
                print(libname, libid)
                
                ql = QinLib(path)
                rt_object = ql.get_image(libid)

                print(rt_object.type)

                if rt_object.type == 2: # spr
                    print(rt_object.data.getvalue())
                    return
                #print(pos_x, pos_y)
                #print(bld_item.m_booIsSpr)
                print('end')
            '''
            #mdl_res = MdlResClass()
            #print(pos_x, pos_y)
            #for part in mdl.PartMng:
                name = part.m_szName
                isSpr= part.m_booIsSpr
                picid = part.m_dPicID
                posx = part.m_pos_x
                posy = part.m_pos_y
                
                print(name)
                print(picid)
            '''
            num += 1

    def LoadScene(self, file_path):
        # 加载scn文件
        SRC = ScnResClass(file_path)
        SrcInfo = SRC.data

        # 获取map信息
        map_name = SrcInfo['map_name']
        bnt_name = SrcInfo['intbld']
        ont_name = SrcInfo['intobj']
        #print(bnt_name)
        #return
        
        # 加载map文件
        map_folder = GetMapPath()
        map_path = os.path.join(map_folder, map_name)

        # 读取map文件的图块
        map_array = self.LoadMap(map_path)
        
        # 加载 场景的物品 文件。注意，物件可进行操作，或是遮挡玩家，所以不能直接覆盖到底层地图上
        bnt_folder = GetBntPath()
        bnt_path = os.path.join(bnt_folder, bnt_name)

        # 读物bnt文件的图块
        #bld_array = self.LoadBnt(bnt_path)
        return map_array

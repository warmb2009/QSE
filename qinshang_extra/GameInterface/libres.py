#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :libres.py
@说明    :管理lib资源文件
@时间    :2020/10/18 12:30:27
@作者    :jeroen
@版本    :1.0
'''
from GameInterface.lib import *
from GameInterface.rci import *
from GameInterface.gameglobal import *
import os


class ResMng():
    '''
    res资源管理类，用于获取res的图片信息，用图片序号进行检索
    '''
    def __init__(self):
        self.image_list = {}
        self.maptiles_list = {}

    def get_image(self, res_id):
        '''
        根据资源id获取物体的图片数据
        '''
        if res_id not in self.image_list.keys():
            # 获取ini文件数据GetResIniPath
            im = IniMng(GetResIniPath())
            # 将资源总id 转为文件内资源id
            libname, libid, libfilename = im.get(res_id)
            lib_file_path = os.path.join( GetResPath(), libfilename)

            ql = QinLib(lib_file_path)
            image_array = ql.get_image(libid)
            self.image_list[res_id] = image_array

        return self.image_list[res_id]

    def get_map_image(self, lib_file_path, res_id):
        '''
        根据资源路径和资源id获取地形图块
        '''
        image_array = None
        sign = lib_file_path.split('/')[-1]

        if sign not in self.maptiles_list.keys():
            sign_list = {}
            self.maptiles_list[sign] = sign_list

        sign_list = self.maptiles_list[sign]

        if res_id not in sign_list.keys():
            ql = QinLib(lib_file_path)
            image_array = ql.get_image(res_id).item.image_array
            sign_list[res_id] = image_array

        return sign_list[res_id]

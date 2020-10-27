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
from GameInterface.ini import *
from GameInterface.gameglobal import *


class ResMng():
    def __init__(self):
        self.image_list = {}
        self.maptiles_list = {}


    # 根据资源id获取物体的图片数据
    def get_image(self, res_id):
        if not self.image_list.has_key(res_id):
            # 获取ini文件数据
            rm = IniMng(GetResIniPath())
            # 将资源总id 转为文件内资源id
            libname, libid, libfilename = rm.get(res_id)
            lib_file_path = os.path.join( GetResPath(), libfilename)  # 构造资源文件路径

            ql = QinLib(lib_file_path)
            image_array = ql.get_image(libid)
            self.image_list[res_id] = image_array

        return self.image_list[res_id]

    # 根据资源路径和资源id获取地形图块
    def get_map_image(self, lib_file_path, res_id):
        image_array = None
        sign = lib_file_path.split('/')[-1]

        if not sign in self.maptiles_list.keys():
            sign_list = {}
            self.maptiles_list[sign] = sign_list

        sign_list = self.maptiles_list[sign]

        if not res_id in sign_list.keys():
            ql = QinLib(lib_file_path)
            image_array = ql.get_image(res_id)
            sign_list[res_id] = image_array
        
        return sign_list[res_id]
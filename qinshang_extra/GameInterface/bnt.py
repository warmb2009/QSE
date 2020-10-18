#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
from mdl import MdlBase
from ini import ResMng


class BaseClass():
    def printc(self):
        for i, j in vars(self).items():
            print('<--- ' + i + ' : ' + str(j) + ' --->')


class BntBase():
    class FileHeader(BaseClass):
        def __init__(self):
            self.tag = ''  # SoloInit
            self.version = ''  # 版本 1.00
            self.inum = 0  # 部件数量
            self.mdl_name = ''  # 所属mdl文件（mdl文件：构建具体的物品）
            self.mdl_num = 0  # mdl数量 这里及以下并没有用到
            self.role_name = ''
            self.role_num = 0
            self.prop_name = ''
            self.prop_num = 0
            self.other_name = ''
            self.other_num = 0
            self.reserved = ''

    class InitBld(BaseClass):
        def __init__(self):
            '''
            模型类型
            TYPE_ModelBase,         0
            TYPE_ModelBeastie,      1
            TYPE_ModelCharacter,    2
            TYPE_ModelBld,          3
            TYPE_ModelMethodMain,   4
            TYPE_ModelMethodUnit,   5
            TYPE_ModelProp          6
            '''
            self.itype = 0  # 类型
            self.iModelAutoID = 0  # 物品ID
            self.gp_map_pos = 0  # 地图上的坐标
            self.reserve = 0  # 保留块
            self.init_name_num = 0  # 名称模块数量
            self.init_name = ''  # 名称（可选）
            self.sztrigeer = ''  # 触发器（可选）

    def __init__(self, _filename):
        self.file_name = _filename

        self.file_header = None
        self.mdl_list = []
        self.init_data()

    def init_data(self):
        f = self.read(self.file_name)
        self.file_header = self.FileHeader()
        self.file_header.tag = struct.unpack('16c', f.read(16))[0]
        self.file_header.version = struct.unpack('16c', f.read(16))[0]
        self.file_header.inum = int(struct.unpack('h', f.read(2))[0])

        self.file_header.mdl_name = struct.unpack('256c', f.read(256))[0]
        self.file_header.mdl_num = int(struct.unpack('h', f.read(2))[0])
        self.file_header.role_name = struct.unpack('256c', f.read(256))[0]
        self.file_header.role_num = int(struct.unpack('h', f.read(2))[0])
        self.file_header.prop_name = struct.unpack('256c', f.read(256))[0]
        self.file_header.prop_num = int(struct.unpack('h', f.read(2))[0])
        self.file_header.other_name = struct.unpack('256c', f.read(256))[0]
        self.file_header.other_num = int(struct.unpack('h', f.read(2))[0])
        self.file_header.reserved = struct.unpack('86c', f.read(86))[0]
        self.file_header.printc()

        num = self.file_header.inum
        while num:
            bld = self.InitBld()
            bld.itype = int(struct.unpack('h', f.read(2))[0])
            print('bld.type: %d' % bld.itype)
            bld.iModelAutoID = struct.unpack('h', f.read(2))[0]

            ''' 测试读取资源
            mybld = mdlMng.get(bld.iModelAutoID)
            mng = mybld.PartMng
            res_mng = ResMng('a.csv')
            res_mng.printc()

            for b in mng:
                print(b.m_dPicID)
                print(res_mng.get(b.m_dPicID))
            return
            '''

            bld.gp_map_pos = struct.unpack('2i', f.read(8))[0]
            bld.reserve = struct.unpack('2h', f.read(4))[0]
            bld.init_name_num = struct.unpack('i', f.read(4))[0]
            if bld.init_name_num > 0:
                bld.init_name = struct.unpack('i', f.read(4))[0]
            if bld.itype == 4:
                bld.sztrigeer = struct.unpack('128c', f.read(128))[0]

            bld.printc()
            print("%d : %s" % (bld.iModelAutoID, hex(bld.iModelAutoID)))
            num -= 1
        print('共有%d个组件' % self.file_header.inum)

    def read(self, _filename):
        f = open(_filename, 'rb')
        return f


'''
if __name__ == '__main__':
    file_name = '/home/jeroen/work/qinshang/game/SCENE/Int/zhc_house1.BNT'
    # file_name = '/home/jeroen/work/qinshang/game/SCENE/Int/zhaocun1.BNT'
    bnt = BntBase(file_name)
'''

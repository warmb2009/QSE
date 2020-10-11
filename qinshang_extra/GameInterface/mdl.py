#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
# import os
# import sys
# from io import BytesIO


class BaseClass():
    def printc(self):
        for i, j in vars(self).items():
            print('<--- ' + i + ' : ' + str(j) + ' --->')


class MdlBase():
    class FileHeader(BaseClass):
        def __init__(self):
            self.tag = ''  # mdl头的标识 SoloMdl
            self.version = ''  # 文件版本
            self.inum = 0  # 所包含部件数量
            self.szname = ''  # 
            self.reserved = ''


    class SModelBld():
        def __init__(self):
            self.itype = 0  # 2
            self.szName = 0  # 32 char
            self.wManualID = 0  # 2
            self.wAutoID = 0  # 2
            self.PartMng_LPSTR = 0  # 4 char * 
            self.PartNum = 0  # 2 部件数
            self.DownNum = 0  # 2 下层部件数
            self.MiddleNum = 0  # 2 中层部件数
            self.UpNum = 0  # 2 上层部件数
            self.booIsAnimate = 0  # 1 是否动画
            self.grFrame = 0  # 20 大小框架
            self.m_gpAttribLeftUp = 0  # 8 左上角
            self.m_cxDisMetrix = 0  # 2 坐标x
            self.m_cyDisMetrix = 0  # 2 坐标y
            self.m_gpCharacter = 0  # 80  8*10 
            self.m_aDisMetrix = {}

            self.m_wSound = 0  # 建筑物声音
            self.m_bLight = 0  # 灯光
            self.m_bAniDisplay = 0  # 正常光影，半透

            self.PartMng = []

    class PartialModal():
        def __init__(self):
            self.m_szName = ''
            self.m_booIsSpr = 0
            self.m_dPicID = 0
            self.m_pos_x = 0
            self.m_pos_y = 0

    def __init__(self, _filename):
        self.file_name = _filename

        self.file_header = None

        self.m_apMdl = []
        self.idTable = {}
        self.init_data()

    def init_data(self):
        f = self.read(self.file_name)

        self.file_header = self.FileHeader()
        self.file_header.tag = struct.unpack('16c', f.read(16))[0]
        self.file_header.version = struct.unpack('16c', f.read(16))[0]
        self.file_header.inum = int(struct.unpack('h', f.read(2))[0])

        self.file_header.szname = struct.unpack('256c', f.read(256))[0]
        self.file_header.reserved = struct.unpack('94c', f.read(94))[0]
        self.file_header.printc()

        num = self.file_header.inum
        # while num:
        
        for index in range(self.file_header.inum):
            bld = self.SModelBld()

            bld.itype = int(struct.unpack('h', f.read(2))[0])
            # print('\nbld.type: %d' % bld.itype)
            or_name = struct.unpack('32s', f.read(32))[0]
            bld.szName = or_name.replace(b'\xcd', b'')
            # print(or_name)
            # print('szname:%s' % bld.szName.decode(encoding='gbk', errors='replace'))
            bld.wManualID = struct.unpack('h', f.read(2))[0]
            bld.wAutoID = struct.unpack('h', f.read(2))[0]
            bld.PartMng_LPSTR = struct.unpack('2h', f.read(4))[0]

            # print('manualID:%d,\tAutoID:%d' % (bld.wManualID, bld.wAutoID))

            bld.PartNum = struct.unpack('h', f.read(2))[0]
            bld.DownNum = struct.unpack('h', f.read(2))[0]
            bld.MiddleNum = struct.unpack('h', f.read(2))[0]
            bld.UpNum = struct.unpack('h', f.read(2))[0]

            bld.booIsAnimate = struct.unpack('c', f.read(1))[0]
            bld.grFrame = struct.unpack('5i', f.read(20))[0]
            bld.m_gpAttribLeftUp = struct.unpack('2i', f.read(8))

            bld.m_cxDisMetrix = struct.unpack('h', f.read(2))[0]
            bld.m_cyDisMetrix = struct.unpack('h', f.read(2))[0]

            bld.m_gpCharacter = struct.unpack('20i', f.read(80))[0]

            for i in range(bld.m_cyDisMetrix):
                for j in range(bld.m_cxDisMetrix):
                    '''
                    BYTE	bAttrib;
                    BYTE    bTemporaryFlag;		// not used on suffer,暂时为高度标记0-3
                    '''
                    bld.m_aDisMetrix[str(i * bld.m_cxDisMetrix + j)] = struct.unpack('2c', f.read(2))[0]

            bld.m_wSound = struct.unpack('h', f.read(2))[0]
            bld.m_bLight = struct.unpack('c', f.read(1))[0]
            bld.m_bAniDisplay = struct.unpack('c', f.read(1))[0]

            for z in range(bld.PartNum):
                a_bld = self.PartialModal()

                or_m_name = struct.unpack('8s', f.read(8))[0]
                a_bld.m_szName = or_m_name.replace(b'\xcd', b'')

                # print('\tszname:%s' % a_bld.m_szName.decode(encoding='gbk', errors='replace'))
                a_bld.m_booIsSpr = struct.unpack('c', f.read(1))[0]
                a_bld.m_dPicID = struct.unpack('i', f.read(4))[0]

                # print('\tpicID:%d' % int(a_bld.m_dPicID))
                a_bld.m_pos_x = struct.unpack('i', f.read(4))[0]
                a_bld.m_pos_y = struct.unpack('i', f.read(4))[0]

                bld.PartMng.append(a_bld)
            self.m_apMdl.append(bld)
            self.idTable[bld.wAutoID] = bld

        print('共有%d个组件' % self.file_header.inum)

    def get(self, mAutoID):
        return self.idTable[mAutoID]

    def read(self, _filename):
        f = open(_filename, 'rb')
        return f


if __name__ == '__main__':
    file_name = '/home/jeroen/work/qinshang/game/mdl/house.Mdl'
    # file_name = '/home/jeroen/work/qinshang/game/SCENE/Int/zhaocun1.BNT'
    bnt = MdlBase(file_name)

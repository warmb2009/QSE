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


class MapBase(BaseClass):
    class FileHeader(BaseClass):
        def __init__(self, _style=0, _x=0, _y=0, _tag='', _version=''):
            self.mapstyle = _style
            self.cx = _x
            self.cy = _y
            self.tag = _tag
            self.version = _version

    class LibHeader(BaseClass):
        def __init__(self, _libversion='', _libname='', _libnum=0, _libsizenum=0):
            self.libversion = _libversion
            self.libname = _libname
            self.libnum = _libnum
            self.libsizenum = _libsizenum

    class MU(BaseClass):
        def __init__(self, _id_1=0, _id_2=0, _btype=0, _team_index=0, _height=0, _terrain=0, _scneffid=0):
            self.id_1 = _id_1
            self.id_2 = _id_2
            self.btype = _btype
            self.team_index = _team_index
            self.height = _height
            self.terrain = _terrain
            self.scneffid = _scneffid

        def printb(self, ex=''):
            print('%s\t:%.4X(%d)\t%.4X(%d)\t' % (ex, self.id_1, self.id_1,
                                                 self.id_2, self.id_2))

    def __init__(self, _filename):
        self.file_name = _filename

        self.file_header = None
        self.lib_header = None

        self.index_list = []
        self.mu_list = []

        self.init_data()

    def read(self, _filename):
        f = open(_filename, 'rb')
        return f

    def read_index(self, num, f):
        while num:
            index = int(struct.unpack('h', f.read(2))[0])
            self.index_list.append(index)
            num -= 1
        return self.index_list

    def read_data(self, num, f):
        while num:
            mu = self.MU()
            mu.id_1 = struct.unpack('h', f.read(2))[0]
            mu.id_2 = struct.unpack('h', f.read(2))[0]
            mu.btype = struct.unpack('c', f.read(1))[0]
            mu.team_index = struct.unpack('c', f.read(1))[0]
            mu.height = struct.unpack('c', f.read(1))[0]
            mu.terrain = struct.unpack('c', f.read(1))[0]
            mu.scneffid = struct.unpack('h', f.read(2))[0]
            self.mu_list.append(mu)
            num -= 1

        return self.mu_list

    def init_data(self):
        f = self.read(self.file_name)
        self.file_header = self.FileHeader()
        self.file_header.tag = struct.unpack('16c', f.read(16))[0]
        self.file_header.version = struct.unpack('16c', f.read(16))[0]
        self.file_header.mapstyle = int(struct.unpack('h', f.read(2))[0])
        self.file_header.cx = int(struct.unpack('h', f.read(2))[0])
        self.file_header.cy = int(struct.unpack('h', f.read(2))[0])
        f.seek(128)

        self.file_header.printc()

        self.lib_header = self.LibHeader()
        self.lib_header.libversion = struct.unpack('16c', f.read(16))[0]
        self.lib_header.libname = struct.unpack('256c', f.read(256))[0]
        self.lib_header.libnum = int(struct.unpack('h', f.read(2))[0])
        self.lib_header.libsizenum = int(struct.unpack('i', f.read(4))[0])
        self.lib_index_list = self.read_index(self.lib_header.libnum, f)

        mu_list = self.read_data(self.file_header.cx * self.file_header.cy, f)
        # print(self.lib_index_list)
        # print(mu_list)
        blk_list = []
        blk_list2 = []

        tiled_list1 = []
        tiled_list2 = []
        
        for i in range(len(mu_list)):
            mu = mu_list[i]
            blk_list.append(mu.id_1)
            blk_list2.append(mu.id_2)

        for i in range(len(blk_list)):
            mu = blk_list[i]
            mu2 = blk_list2[i]
            #print('%d\t:%d'% (i+1, mu))
            tiled_str = '<tile id="%d"><image width="64" height="32" source="D:/qin_export/Bei/%s.png"/></tile>' % (i+1, str(mu+1) + '-1')
            tiled_str2 = '<tile id="%d"><image width="64" height="32" source="D:/qin_export/Bei/%s.png"/></tile>' % (i+1, str(mu2+1) + '-1')
            tiled_list1.append(tiled_str)
            tiled_list2.append(tiled_str2)

        self.write('tiled_list1', tiled_list1)
        self.write('tiled_list2', tiled_list2)
        num_list = []
        x = 192        
        for i in range(1, x*x+1):
            num_list.append(str(i))
        t = ','.join(num_list)
        self.write_str('num_list1', t)

        num_list2 = []
        for test in range(36865, 36865+x*x):
            num_list2.append(str(test))
        tt = ','.join(num_list2)
        self.write_str('num_list2', tt)

    def write_str(self, file_name, num_str):
        f = open(file_name, 'w')
        f.write(num_str)
        f.close()
   
    def write(self, file_name, data):
        f = open(file_name, 'w')
        f.writelines([line+'\n' for line in data])
        # f.writelines(data)
        f.close()


if __name__ == '__main__':
    file_name = '/home/jeroen/work/qinshang/game/SCENE/Map/zhaocun1.MAP'
    mp = MapBase(file_name)

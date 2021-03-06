#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :ResCombinationIni.py
@说明    :
@时间    :2020/10/18 11:20:15
@作者    :jeroen
@版本    :1.0
'''


import csv


class BaseClass():
    def printc(self):
        for i, j in vars(self).items():
            if type(j) == type(1):
                print('<--- ' + i + ' : ' + hex(j) + '--' + str(j) +' --->')
            else:
                print('<--- ' + i + ' : ' + str(j) + ' --->')


class Ini(BaseClass):
    def __init__(self):
        self.szTemp = ''
        self.iMin = 0
        self.iMax = 0
        self.nNum = 0
        self.lib_name = ''


class IniMng(BaseClass):
    def __init__(self, _filename):
        self.ini_list = {}
        self.InitData(_filename)

    def InitData(self, _filename):
        with open(_filename) as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                ini = Ini()
                ini.szTemp = row[0]
                iMin = int(row[1])
                iMin = iMin & 0xff0000
                nNum = iMin >> 18

                ini.nNum = nNum
                ini.iMin = int(row[1])
                ini.iMax = int(row[2])
                ini.lib_name = row[3]
                self.ini_list[nNum] = ini

    def get(self, dResID):
        fact_resid = dResID & 0x3ffff
        libid = dResID & 0xff0000
        fact_libid = libid >> 18

        fact_lib_name = self.ini_list[fact_libid].szTemp
        lib_file_name = self.ini_list[fact_libid].lib_name
        print('Fact Res libID: %d' % fact_resid)
        print('fact lib id: %d' % fact_libid)
        print('fact lib name: %s' % self.ini_list[fact_libid].szTemp)
        return fact_lib_name, fact_resid, lib_file_name

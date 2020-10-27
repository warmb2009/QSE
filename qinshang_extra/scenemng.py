#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :res.py
@说明    :管理场景文件
@时间    :2020/10/18 12:30:27
@作者    :jeroen
@版本    :1.0
'''
import threading
from GameController.scene import *
import os.path        
from GameInterface.gameglobal import *

class LibSceneMngSingleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.map_info = []
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(LibSceneMngSingleton, "_instance"):
            with LibSceneMngSingleton._instance_lock:
                if not hasattr(LibSceneMngSingleton, "_instance"):
                    LibSceneMngSingleton._instance = object.__new__(cls)

        return LibSceneMngSingleton._instance


    def LoadScn(self, scn_name):
        # scn_folder = '/home/jeroen/work/qinshang/QSE/datas/SCENE/Scn_new/'
        scn_folder = GetScnPath()
        scn_path = os.path.join(scn_folder, scn_name)
        sc = Scene()
        self.map_info = sc.LoadScene(scn_path)

    def GetResBufferByID(self, res_id):
        scn_filename = '/home/jeroen/work/qinshang/QSE/datas/SCENE/Scn_new/zhc_house1.Scn'

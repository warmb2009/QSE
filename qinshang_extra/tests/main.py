#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :main.py
@说明    :测试文件
@时间    :2020/10/11 17:06:59
@作者    :jeroen
@版本    :1.0
'''


from GameInterface.lib import QinLib, QinXBM, QinXbmDev


def test(filename):
    index = 1168
    test = QinLib(filename)
    data = test.get_xbm_buf(index)
    xbm = QinXbmDev(data)
    if xbm.type == 0:
        print(len(xbm.data.qx_list))
    else:
        print('xbm ')

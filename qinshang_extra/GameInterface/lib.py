#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :lib.py
@说明    :
@时间    :2020/10/11 16:39:21
@作者    :jeroen
@版本    :1.0
'''

import struct
from io import BytesIO
import numpy as np
#from PIL import Image

'''
读取秦殇目录的资源文件lib
经过三天的努力，成功的破解了目标公司的游戏图片格式xbm,还有他的库文件*.lib,
也就是可以轻松的从其中提取图片,哎,竟然没有压缩.太简单了. 时间有限,我就说一下他的xbm格式.
**图片文件的头结构
**
1: 16字节 图片标记:xbm
2: 几个整数 都是: 0
3: 一个整数 宽度:
4: 一个整数 高度:
5: 一个整数 未知: 总是 0x10100100
6: 一个整数 掩码: 0xF81F
7: 7个整数 都是: 0
**图片文件的每一行描述
** 行的描述是:
    1:偏移地址(相对于文件头结构结束的地方)
    2:行的数据长度 那么这里有多少个描述呢? 当然是 "高度" 个了.

**图片文件的图象数据(rle)
** 如果行头的第一个(short)短整形数,是零!!!
那么表示接下来的一个(short)短整形数 就是 ,是 连续的不透明色的个数.
反之,就是透明色的个数. 注意一点: 他们都是短整形数,因为,哎,因为图象的点就是16位的.
'''


class LibResClass():
    '''
    资源处理类， 传入缓存数据，解析为可识别的资源数据 包含图片，图片组，帧序列
    '''
    def __init__(self, _buf):
        self.type = 0
        self.buf = _buf
        self.item = None

        self.initdata()

    def initdata(self):
        b = BytesIO(self.buf)
        h_str = str(struct.unpack('8s', b.read(8))[0].split(b'\x00')[0], encoding = "gb2312")
        # 分辨是否是xbmgroup 序列帧
        if h_str == 'xbmgroup':
            self.type = 0
            self.item = XBMGroupObject(self.buf)
        elif h_str == 'xbm':
            self.type = 1
            self.item = XBMObject(self.buf)
        else:  # spr
            self.type = 2
            self.item = SprObject(self.buf)


# 读取帧动画数据
class SprGroupObject():
    '''
    帧动画对象，从缓存数据中读入
    '''
    def __init__(self, _buf):
        _buf = BytesIO(_buf)
        self.spr_num = 0  # 动画数量
        self.frame_num = 0  # 帧数
        self.average_speed = 0  # 动画速度
        self.frame_script_size = 0

        self.spr_list = []  # 帧列表
        
        self.init_data(_buf)

    def init_data(_buf):
        self.spri_num = struct.unpack('i', _buf.read(4))[0]
        self.frame_num = struct.unpack('i', _buf.read(4))[0]
        self.average_speed = struct.unpack('i', _buf.read(4))[0]
        self.frame_script_size = struct.unpack('i', _buf.read(4))[0]

        num = self.frame_num
        while num:
            spr = SprObject(_buf.read(28))
            self.spr_list.append(spr)
            num -= 1

class SprObject():
    '''
    帧动画单独一帧的对象
    '''
    def __init__(self, _buf):
        _buf = BytesIO(_buf)
        self.frame_type = 0  # 帧类型
        self.frame_speed = 0  # 帧速度
        self.res_id = 0  # 帧图片的资源id
        self.x_offset = 0
        self.y_offset = 0
        self.x_center = 0
        self.y_center = 0

        self.init_data(_buf)

    def init_data(_buf):
        self.frame_type = struct.unpack('i', _buf.read(4))[0]
        self.frame_speed = struct.unpack('i', _buf.read(4))[0]
        self.res_id = struct.unpack('i', _buf.read(4))[0]
        self.x_offset = struct.unpack('i', _buf.read(4))[0]
        self.y_offset = struct.unpack('i', _buf.read(4))[0]
        self.x_center = struct.unpack('i', _buf.read(4))[0]
        self.y_center = struct.unpack('i', _buf.read(4))[0]
        

# 读取xbm序列帧
class XBMGroupObject():
    '''
    xbm组对象，从缓存数据中读入
    '''
    def __init__(self, _buf):
        _buf = BytesIO(_buf)
        self.type = 0
        # self.buf = BytesIO(_buf)
        self.szName = ''
        self.iNum = 0
        self.size = 0
        self.qx_list = []

        self.InitData(_buf)

    def InitData(self, _buf):
        # 标识
        self.szName = struct.unpack('16s', _buf.read(16))[0]
        # 子图片数量
        self.iNum = struct.unpack('i', _buf.read(4))[0]
        self.size = struct.unpack('i', _buf.read(4))[0]

        pos_list = []
        # 读取偏移地址（相对于文件头）
        num = self.iNum
        while num:
            pos = struct.unpack('i', _buf.read(4))[0]
            pos_list.append(pos)
            num -= 1

        # 读取xbm 加入列表
        for pos in pos_list:
            _buf.seek(pos)
            data = _buf.read(self.size)
            qx = XBMObject(data)
            self.qx_list.append(qx)


class XBMObject():
    '''
    xbm对象，从缓存数据中读入
    '''
    def __init__(self, _buf):
        _buf = BytesIO(_buf)  # 内存
        self.szName = ''  # 名称
        self.iVer = 0
        self.width = 0  # 图片宽度
        self.height = 0  # 图片高度
        self.position_list = []  # 索引表
        self.index = 0

        #self.image_array = None  # 像素点阵
        self.InitData(_buf)
        self.image_array = self.read_data(_buf)

    def get_image_array():
        '''
        获取图像数组
        '''
        return self.image_array

    def InitData(self, _buf):
        '''
        xbm 类型图片初始化
        '''
        self.szName = struct.unpack('16s', _buf.read(16))
        self.iVer = struct.unpack('4s', _buf.read(4))
        _buf.seek(20)

        # 读取图片宽度 高度
        self.width = struct.unpack('i', _buf.read(4))[0]
        self.height = struct.unpack('i', _buf.read(4))[0]

        # 初始化图片数据的矩阵
        self.image_array = np.empty(shape=[self.width, self.height, 4],
                                    dtype=int)
        # 定位到数据段
        _buf.seek(64)

        # 读取每行的偏移地址
        for i in range(self.height):
            pos = struct.unpack('i', _buf.read(4))[0] + 64
            # 处理单行数据
            self.position_list.append(pos)

    # rgb565图像转为rgb888
    def rgb565torgb888(self, color):
        '''
        565格式像素转为888格式
        '''
        r_mask = 0b1111100000000000
        g_mask = 0b0000011111100000
        b_mask = 0b0000000000011111

        r_888 = (r_mask & color) >> 8  # 右移11 左移动3
        g_888 = (g_mask & color) >> 3  # 右移动5 左移动2
        b_888 = (b_mask & color) << 3  # 左移动3

        return (r_888, g_888, b_888, 255)

    def read_image_line_data(self, _buf, current_count, width):
        '''
        处理图像的单行像素数据
        '''
        pixel_array = []
        # buf: xbm图片缓存
        # current_count 初始为0 记录所读取的游标，用于迭代
        # width:图片宽度 用于限制迭代次数
        # pixel_array 要存入数据的数组

        # 读取透明色的个数
        zero_count = int(struct.unpack('h', _buf.read(2))[0]/2)

        for i in range(zero_count):
            pixel_array.append((0, 0, 0, 0))
            # 颜色计数器+1
            current_count += 1
        if (current_count < width):
            # 继续读取非透明颜色
            no_zero_count = int(struct.unpack('h', _buf.read(2))[0]/2)
            for i in range(no_zero_count):
                res = _buf.read(2)
                data = struct.unpack('h', res)[0]
                # 565颜色转为888
                color = self.rgb565torgb888(data)
                # 将新颜色加入图片像素矩阵
                pixel_array.append(color)
                # 计数器+1
                current_count += 1

        if (current_count < width):
            # 继续读取后面的颜色
            r_array = self.read_image_line_data(_buf,
                                                current_count,
                                                width)
            pixel_array.extend(r_array)  # 合并迭代数组

        return pixel_array

    def read_data(self, _buf):
        '''
        开始处理图像数据
        '''
        all_array = []
        for i in range(self.height):
            # 获取每行的偏移地址
            pos = self.position_list[i]
            # 定位到偏移地址
            _buf.seek(pos)

            pixel_array = self.read_image_line_data(_buf, 0, self.width)
            all_array.append(pixel_array)
        # 转为np数组
        rt = np.array(all_array)
        return rt


class QinLib():
    '''
    处理lib资源文件    
    '''
    def __init__(self, _filename):
        self.filename = _filename
        self.filecount = 0
        self.filelist = []
        self.initdata(self.filename)

    def read(self, _filename):
        f = open(_filename, 'rb')
        return f

    def initdata(self, _filename=''):

        f = self.read(_filename)
        
        f.seek(16)  # 读取头
        libcount = struct.unpack('i', f.read(4))[0]  # 读取数量
        self.filecount = libcount
        #print(_filename)
        #print('count:%d' % libcount)
        f.seek(256)

        # 读取lib文件内每个分块的数据 pos length buf
        for i in range(libcount):
            seek_pos = i * 8 + 256
            f.seek(seek_pos)
            sig_pos = struct.unpack('i', f.read(4))[0]
            sig_length = struct.unpack('i', f.read(4))[0]

            fileinfo = {}
            fileinfo['pos'] = sig_pos
            fileinfo['length'] = sig_length
            self.filelist.append(fileinfo)
        f.close()

    def get_zero_buf(self, width, height):
        empty_buf = np.zeros(shape=[width, height, 4],
                                    dtype=int)
        return empty_buf

    def get_buf(self, index):
        '''
        获取指定序号的缓存数据
        '''
        info = self.filelist[index]
        f = self.read(self.filename)
        f.seek(info['pos'])
        data = f.read(info['length'])

        f.close()
        return data

    # 获取图片的数据后 转为数组
    def get_image(self, index):
        '''
        获取对应序号的格式化图片数据
        '''
        data = self.get_buf(index)
        return LibResClass(data)

    # 去掉第四位的透明数据
    def combine_one(self, buf):
        width = buf.shape[0]
        height = buf.shape[1]
        ret_array = np.empty(shape=[width, height, 4], dtype=int)
        for i in range(0, buf.shape[0]):
            for j in range(0, buf.shape[1]):
                item = buf[i][j]
                ret_array[i, j] = item[:3]
        return ret_array

    def combine_map(self, width, height):
        pass

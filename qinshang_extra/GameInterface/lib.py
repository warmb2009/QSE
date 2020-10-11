#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import struct
from io import BytesIO
import numpy as np
from PIL import Image


class QinXBM():
    def __init__(self, _buf):
        self.buf = BytesIO(_buf)
        self.width = 0
        self.height = 0
        self.position_list = []
        self.index = 0

        self.image_array = None
        self.initdata()
        self.read_data()

        return

    # xbm 类型图片初始化
    def initdata(self):
        # xbmtype = struct.unpack('4s', self.buf.read(4))
        self.buf.seek(20)

        # 读取图片宽度 高度
        self.width = struct.unpack('i', self.buf.read(4))[0]
        self.height = struct.unpack('i', self.buf.read(4))[0]

        self.image_array = np.empty(shape=[self.height, self.width, 4],
                                    dtype=int)
        # 定位到数据段
        self.buf.seek(64)

        # 读取每行的偏移地址
        for i in range(self.height):
            pos = struct.unpack('i', self.buf.read(4))[0] + 64
            self.position_list.append(pos)

    def rgb565torgb888(self, color):
        r_mask = 0b1111100000000000
        g_mask = 0b0000011111100000
        b_mask = 0b0000000000011111

        r_888 = (r_mask & color) >> 8  # 右移11 左移动3
        g_888 = (g_mask & color) >> 3  # 右移动5 左移动2
        b_888 = (b_mask & color) << 3  # 左移动3

        return [r_888, g_888, b_888, 255]

    def read_image_line_data(self, current_count, zero=True):
        if(zero):
            zero_count = int(struct.unpack('h', self.buf.read(2))[0]/2)

            for i in range(zero_count):
                self.image_array[self.index, current_count] = [255,
                                                               255,
                                                               255,
                                                               0]
                current_count += 1

        if (current_count < self.width):
            no_zero_count = int(struct.unpack('h', self.buf.read(2))[0]/2)

            for i in range(no_zero_count):
                res = self.buf.read(2)
                print(''.join([r'\x{:x}'.format(c) for c in res]))
                data = struct.unpack('h', res)[0]
                color = self.rgb565torgb888(data)
                print(self.index)
                print(current_count)
                print(self.image_array.shape)
                self.image_array[self.index, current_count] = color

                current_count += 1

        if (current_count < self.width):
            self.read_image_line_data(current_count, True)
        else:
            return

    # 读取图片某行的数据 index行
    def read_line_data(self, _index):
        print(_index)
        self.index = _index
        pos = self.position_list[self.index]
        self.buf.seek(pos)

        # length = self.width
        # rest = self.buf.read(4)
        # print(''.join([r'\x{:x}'.format(c) for c in rest]))

        self.read_image_line_data(0, True)
        print(self.image_array[self.index])

    def read_data(self):
        for i in range(self.height):
            self.read_line_data(i)

        return self.image_array

    def save_file(self, filename='out.jpeg'):
        img = Image.fromarray(self.image_array.astype('uint8')).convert('RGBA')
        img.save(filename)


# 处理lib资源文件
class QinLib():
    def __init__(self, _filename):
        self.filename = _filename
        self.filecount = 0
        self.filelist = []
        self.initdata(self.filename)
        return

    def read(self, _filename):
        f = open(_filename, 'rb')
        return f

    def initdata(self, _filename=''):
        f = self.read(_filename)
        # libtype = struct.unpack('8s', f.read(8))
        f.seek(16)
        libcount = struct.unpack('i', f.read(4))[0]
        self.filecount = libcount
        f.seek(256)

        for i in range(libcount):
            seek_pos = i * 8 + 256
            f.seek(seek_pos)
            sig_pos = struct.unpack('i', f.read(4))
            sig_length = struct.unpack('i', f.read(4))

            fileinfo = {}
            fileinfo['pos'] = sig_pos[0]
            fileinfo['length'] = sig_length[0]

            self.filelist.append(fileinfo)
        f.close()

    def get_xbm_buf(self, index):
        xbminfo = self.filelist[index]
        f = self.read(self.filename)
        f.seek(xbminfo['pos'])
        data = f.read(xbminfo['length'])
        return data


if __name__ == '__main__':
    test = QinLib('../Res/snow.lib')

    data = test.get_xbm_buf(0)
    xbm = QinXBM(data)
    xbm.save_file('test.bmp')

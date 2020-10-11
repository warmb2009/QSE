#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import getopt
import os


class h2():
    @classmethod
    def data_convert(self, from_data):
        b = bytearray(from_data)
        decode = True

        if len(b) > 0:
            if b[0] == 128:  # 进行解密
                del b[0]
                decode = False
            else:  # 进行编码转换
                b = bytearray(b.decode('utf8').encode('gbk'))
        else:
            print("NULL File")
            exit(2)
        # 进行数据偏移操作
        for i in range(len(b)):
            b[i] ^= 0x78

        if decode:  # 加密后添加识别
            b.insert(0, 128)
            return b
        else:  # 将解密编码进行转换
            return b.decode('gbk').encode('utf8')

    @classmethod
    def file_convert(self, from_file, to_file):
        ff = open(from_file, 'rb')
        read = ff.read()
        data = self.data_convert(read)
        ff.close()

        tf = open(to_file, 'wb')
        tf.write(data)
        tf.close()


def main(argv):
    try:
        opts = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("test.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    inputfile = ''
    outputfile = ''
    all_path = ''
    print(opts)
    print(len(opts))
    for opt, arg in opts[0]:
        if opt == '-h':
            print("help: python h2.py -i <inputfile> -o <outputfile>")
            print("          此命令处理单个文件")
            print("      python h2.py -a <input dir>")
            print("          此命令会处理目录下的所有文件,并会在目录下创建out目录,放入所有的解密文件")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-a", "--all"):
            all_path = arg

    if all_path != '':  # 处理整个目录
        if os.path.isdir(all_path):
            filelist = os.listdir(all_path)

            # out 目录处理, 不存在则创建
            if len(filelist) != 0:
                output_dir = os.path.join(all_path, 'out')
                if os.path.exists(output_dir) is False:
                    os.makedirs(output_dir)
            else:
                print('DIR is NULL')
                exit(2)

            for filename in filelist:
                filename_path = os.path.join(all_path, filename)
                if os.path.isfile(filename_path):
                    absfilename = os.path.basename(filename).split('.')[0]
                    output_filename = '%s_new.txt' % absfilename
                    output_path = os.path.join(all_path,
                                               'out', output_filename)

                    h2.file_convert(filename_path, output_path)
        else:
            print('-a must be a directory.')
        return
    if outputfile == '':
        filename = os.path.basename(inputfile).split('.')[0]
        outputfile = './%s_new.txt' % filename
    try:
        f = open(inputfile)
        f.close()
        h2.file_convert(inputfile, outputfile)
    except IOError:
        print("File is not accessible")

    print('创建文件成功')
    print(os.path.abspath(outputfile))


if __name__ == '__main__':
    main(sys.argv[1:])

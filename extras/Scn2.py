#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :Scn2.py
@说明    :将Scn文件转为utf8的json文件
@时间    :2020/10/18 00:04:50
@作者    :jeroen
@版本    :1.0
'''

import os
import json


class Scn2():
    def __init__(self, _from_foler, _to_folder):
        self.from_folder = _from_foler
        self.to_folder = _to_folder

        self.convert_folder(self.from_folder, self.to_folder)
        
    # 去掉文件多余空行
    def del_space(self, file_buffer):
        file_content = []
        for line in file_buffer:
            if not line.isspace():
                file_content.append(line)
        return file_content

    # 将json内容写入文件
    def write_file(self, to_folder, to_file_name, content):
        path = os.path.join(to_folder, to_file_name)
        file_out = json.dumps(content, indent=1)
        with open(path, 'w') as f:
            f.write(file_out)
            f.close()

    # 处理文件夹下所有文件
    def convert_folder(self, from_folder, to_folder):
        for folder_path, lisdirs, lisfiles in os.walk(from_folder):
            paths = [os.path.join(from_folder, file_name)for file_name in lisfiles]
            to_paths = [os.path.join(to_folder, file_name)for file_name in lisfiles]

            for i in range(len(paths)):
                from_file = paths[i]
                to_file = to_paths[i]
                self.convert_file(from_file, to_file)
                
    # 处理单个文件
    def convert_file(self, from_file, to_file):
        content = {}
        with open(os.path.join(self.from_folder, from_file), encoding='gb18030') as f:

            lines = f.readlines()
            lines = self.del_space(lines)
            print(lines)  # 打印文件内容 已做对照
            content['map_name'] = lines[0].split('=')[1].strip()
            content['intbld'] = lines[1].split('=')[1].strip()
            content['intobj'] = lines[2].split('=')[1].strip()
            content['enterpoint'] = lines[3].split('=')[1].strip()
            content['raderid'] = lines[-1].split('=')[1].strip()
            
            item_line = []
            for line_num in range(4, len(lines) - 1, 4):
                item = {}
                item['scene_index'] = lines[line_num].split('=')[1].strip()
                item['x'] = lines[line_num+1].split('=')[1].strip()
                item['y'] = lines[line_num+2].split('=')[1].strip()
                item['direction'] = lines[line_num+3].split('=')[1].strip()
                item_line.append(item)
            content['enters'] = item_line
        self.write_file(from_file, to_file, content)


if __name__ == '__main__':
    folder = '/home/jeroen/work/qinshang/QSE/datas/SCENE/Scn'
    to_folder = '/home/jeroen/work/qinshang/QSE/datas/SCENE/Scn_new'

    s = Scn2(folder, to_folder)


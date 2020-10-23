import numpy

# rgb565图像转为rgb888
def rgb565torgb888(color):
    r_mask = 0b1111100000000000
    g_mask = 0b0000011111100000
    b_mask = 0b0000000000011111

    r_888 = (r_mask & color) >> 8  # 右移11 左移动3
    g_888 = (g_mask & color) >> 3  # 右移动5 左移动2
    b_888 = (b_mask & color) << 3  # 左移动3

    return (r_888, g_888, b_888, 255)

# 读取行数据
def read_image_line_data(int current_count, int zero, buf, int width, int index):
    if(zero):
        zero_count = int(struct.unpack('h', buf.read(2))[0]/2)

        for i in range(zero_count):
            image_array[current_count, self.index] = (0,
                                                      0,
                                                      0,
                                                      0)
            current_count += 1

    if (current_count < width):
        int no_zero_count = int(struct.unpack('h', buf.read(2))[0]/2)

        for i in range(no_zero_count):
            res = buf.read(2)
            
            data = struct.unpack('h', res)[0]
            color = rgb565torgb888(data)
            image_array[current_count, index] = color

            current_count += 1

    if (current_count < width):
        read_image_line_data(current_count, True)
    else:
        return

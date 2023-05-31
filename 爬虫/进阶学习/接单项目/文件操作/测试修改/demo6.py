import os
from PIL import Image
import os
import sys


def getPhoto():
    base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))
    path_photo = f'{base_dir}/文件'  # 所有photo所在的文件夹目录
    files_list = os.listdir(path_photo)  # 得到文件夹下的所有文件名称，存在字符串列表中
    # print(type(files_list))
    print(files_list)  # 打印path_photo文件夹下的所有文件
    yangben = f'{base_dir}/样本3'
    if not os.path.exists(yangben):
        os.mkdir(yangben)

    for i in files_list:
        img1 = Image.open(f'{path_photo}/{i}')
        img2 = Image.open(f"{base_dir}/图层/图层 1.png").convert("RGBA")
        img1.paste(img2, (650, 1000), mask=img2)

        img1.save(f"{yangben}/{i}.png")


if __name__ == '__main__':
    getPhoto()

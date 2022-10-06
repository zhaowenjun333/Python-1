from aip import AipOcr

APP_ID = '26844959'
APP_KEY = 'Rc6CIKDayLjW9fzY6upd4ear'
SECRET_KEY = 'cytVQ2FOuzdnaHRqqbvGSG2Vak02nGvv'

# 初始化对象
client = AipOcr(APP_ID, APP_KEY, SECRET_KEY)


# 读取图片
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


image = get_file_content('img.png')

# 调用通用文字识别接口，识别图像
# 通用文字识别
result1 = client.basicGeneral(image)
print(result1)
# 高精度版
result2 = client.basicAccurate(image)
print(result2)

from PIL import Image

# 加载图像

img = Image.open('back_num.png')

# print(img)

# 新建图像
img2 = Image.new('RGB', (200, 100), 'red')
img2.show()
img2.save('red.png')

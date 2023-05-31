import random
import time
import pygame

# 初始化Pygame
pygame.init()

# 设置窗口的大小和标题
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Bubble Sort Visualization"
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# 设置颜色常量
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 设置方块大小和间隔
BLOCK_SIZE = 10
BLOCK_SPACING = 5

MAX_NUM = 100
i = 0
j = 0
swapping = False

if __name__ == '__main__':
    # 创建随机数组
    arr = [random.randint(1, WINDOW_HEIGHT - BLOCK_SIZE) for _ in range(WINDOW_WIDTH // (BLOCK_SIZE + BLOCK_SPACING))]

    while True:
        # 处理退出事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 绘制背景
        WINDOW.fill(WHITE)

        # 绘制方块
        for index, value in enumerate(arr):
            rect = pygame.Rect(index * (BLOCK_SIZE + BLOCK_SPACING), WINDOW_HEIGHT - value, BLOCK_SIZE, value)
            pygame.draw.rect(WINDOW, BLUE, rect)

        # 排序逻辑
        if not swapping:
            if j == len(arr) - i - 1:
                i += 1
                j = 0
                if i == len(arr) - 1:
                    pygame.quit()
                    quit()
            else:
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapping = True
                j += 1
        else:
            swapping = False

        # 延时更新 Pygame 窗口
        time.sleep(0.05)
        pygame.display.update()

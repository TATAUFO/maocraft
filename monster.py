import pygame
import random


# 创建一个自定义的物体类，继承自pygame.sprite.Sprite
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, v, dl):
        super().__init__()
        self.frames = []  # 存储每一帧图像的列表
        self.row_index = 0  # 当前帧的索引
        self.col_index_f = 0
        self.load_frames()  # 加载帧图像
        self.image = self.frames[0][0]  # 设置当前图像为第一帧
        self.rect = self.image.get_rect()
        self.rect.x = x  # 物体的初始X坐标
        self.rect.y = y  # 物体的初始Y坐标
        self.velocity = v  # 物体的移动速度
        self.direct_limit = dl
        self.direct_change_cnt = 0 # 为防止总在变方向
        self.health_font = pygame.font.Font(None, 20)
        self.health = random.randint(30,100)

    def load_frames(self):
        # 加载原图
        image = pygame.image.load("./resource/images/monster/xiaokulou.png")

        # 切分原图为单独的帧
        frame_width = 48  # 每帧的宽度
        frame_height = 64  # 每帧的高度
        for i in range(4):
            frames_row = []
            for j in range(4):
                frame = image.subsurface((j * frame_width, i * frame_height, frame_width, frame_height))
                frames_row.append(frame)
            self.frames.append(frames_row)

    def update(self, *args, **kwargs):

        self.target = kwargs["target"]

        self.col_index_f += 0.05
        if self.col_index_f >= 4:
            self.col_index_f = 0

        # 根据按下的键盘按键更新物体的位置
        xdiff = abs(self.target[0] - self.rect.x)
        ydiff = abs(self.target[1] - self.rect.y)

        # 根据方向变化
        if max(xdiff, ydiff) > 10:
            if self.direct_change_cnt < self.direct_limit:
                self.direct_change_cnt += 1
                if self.row_index == 0:
                    self.rect.y += self.velocity
                if self.row_index == 1:
                    self.rect.x -= self.velocity
                if self.row_index == 2:
                    self.rect.x += self.velocity
                if self.row_index == 3:
                    self.rect.y -= self.velocity

            else:
                self.direct_change_cnt = 0
                if xdiff > ydiff:
                    if self.target[0] < self.rect.x :
                        self.rect.x -= self.velocity
                        self.row_index = 1
                    else:
                        self.rect.x += self.velocity
                        self.row_index = 2
                else:
                    if self.target[1] < self.rect.y:
                        self.rect.y -= self.velocity
                        self.row_index = 3
                    else:
                        self.rect.y += self.velocity
                        self.row_index = 0

        image = self.frames[self.row_index][int(self.col_index_f)]

        # self.health -= (len(collisions) - 1)/10 if len(collisions) > 1 else 0
        # self.health = 0 if self.health < 0 else self.health
        text = self.health_font.render(str(int(self.health)), True, (255, 255, 255))

        current_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        current_surface.blit(image, (0, 0))
        current_surface.blit(text, (0,0))
        self.image = current_surface


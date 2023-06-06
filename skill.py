import pygame

# 创建一个自定义的物体类，继承自pygame.sprite.Sprite
class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []  # 存储每一帧图像的列表
        self.row_index = 0  # 当前帧的索引
        self.col_index_f = 0
        self.load_frames()  # 加载帧图像
        self.image = self.frames[0]  # 设置当前图像为第一帧
        self.rect = self.image.get_rect()
        self.rect.x = x  # 物体的初始X坐标
        self.rect.y = y  # 物体的初始Y坐标


    def load_frames(self):
        # 加载原图
        image = pygame.image.load("./resource/images/skill/fire.png")

        # 切分原图为单独的帧
        frame_width = 60  # 每帧的宽度
        frame_height = 60  # 每帧的高度
        for i in range(4):
            for j in range(4):
                frame = image.subsurface((j * frame_width, i * frame_height, frame_width, frame_height))
                self.frames.append(frame)

    def update(self, *args, **kwargs):
        target = kwargs["target"]

        self.col_index_f += 0.5
        if self.col_index_f >= 16:
            self.col_index_f = 0

        self.image = self.frames[int(self.col_index_f)]
        self.rect.x = target[0]
        self.rect.y = target[1]



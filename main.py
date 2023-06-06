import random
import pygame
from settings import *
from player import Player
from monster import Monster
from skill import Fire

class Mao:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(SCREEN_CAPTION)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def create_background(self) -> pygame.Rect:
        bg = pygame.image.load("./resource/images/background/bg.png")
        # 背景图片的尺寸 50 * 64
        surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        for x in range(0,SCREEN_WIDTH, 50):
            for y in range(0,SCREEN_HEIGHT, 40):
                if ((x == 200 or x == 800) and  200 <= y <= 520) \
                or ((y == 200 or y == 520) and  200 <= x <= 800):
                    surf.blit(bg, (x, y), (4, 4, 55 , 70) ) # 石子路
                else:
                    surf.blit(bg, (x, y), (82, 90, 55, 70)) # 草地

        return surf

    def create_monster(self) -> Monster:
        init_x, init_y = random.randint(50,SCREEN_WIDTH-50), random.randint(50, SCREEN_HEIGHT -50)
        velocity = random.randint(1,3)
        direct_limit = random.randint(20,50)
        return Monster(init_x, init_y, velocity, direct_limit)
        
    def run(self):
        # 创建背景
        background = self.create_background()
        collision_sound = pygame.mixer.Sound("./resource/audios/sound/baozha.mp3")

        player = Player(50,50)
        # 创建一个精灵组，并将物体添加到精灵组中
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        for _ in range(10):
            monster = self.create_monster()
            all_sprites.add(monster)

        # 火焰效果计数相关
        skill_display_count = 0
        fire = None

        # 循环
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # 在精灵组中调用update方法更新物体的位置和图像
            all_sprites.update(target=player.rect.topleft)
            # 画出背景
            self.screen.blit(background, (0,0))
            # 在精灵组中调用draw方法绘制物体到屏幕上
            all_sprites.draw(self.screen)
            pygame.display.flip()
            
            collisions = pygame.sprite.spritecollide(player, all_sprites, False)
            if len(collisions) > 1 and skill_display_count == 0:
                # collision_sound.play()
                player_pos = player.rect.topleft
                fire = Fire(player_pos[0], player_pos[1])
                skill_display_count = 30
                all_sprites.add(fire)

            if skill_display_count > 0:
                skill_display_count -= 1
            if skill_display_count == 0 and fire != None:
                all_sprites.remove(fire)
                fire.kill()


            # 百分之一的可能添加怪兽
            if random.randint(0,100) == 10:
                all_sprites.add(self.create_monster()) 
            # ESC 退出
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False


            self.clock.tick(60)

if __name__ == "__main__":
    game = Mao()
    game.run()
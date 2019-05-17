import pygame

class MyPlane(pygame.sprite.Sprite):#碰撞检测的类
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/hero1.png").convert_alpha()
        self.image2 = pygame.image.load("images/hero2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("images/hero_blowup_n1.png").convert_alpha(),\
            pygame.image.load("images/hero_blowup_n2.png").convert_alpha(),\
            pygame.image.load("images/hero_blowup_n3.png").convert_alpha(),\
            pygame.image.load("images/hero_blowup_n4.png").convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1] #将传进来的背景图片本地化
        self.rect.left, self.rect.top =\
                        (self.width - self.rect.width) // 2,\
                        self.height - self.rect.height - 60
        self.active = True
        self.invicible = False
        #mask用于指定检测范围  fromsurface把非透明部分表为mask
        self.mask = pygame.mask.from_surface(self.image1)

    def reset(self):
        self.rect.left, self.rect.top =\
                        (self.width - self.rect.width) // 2,\
                        self.height - self.rect.height - 60
        self.active = True
        self.invicible = True

#检测偶然触发 通过检测时间消息(KEYDOWN...)
    #频繁触发 key模块里面getPress方法(返回一个事件返回所有按键的bool类型值

    
        

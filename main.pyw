import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply
import base64
import json
from random import *
import os
import socket
from pygame.locals import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 50)  # 窗口显示位置

pygame.init()
pygame.mixer.init()

bg_size = width, height = 400, 650
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("灰机大战 -- by CCY")

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
supply_time = 30

# 载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_fly.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
hero_down_sound = pygame.mixer.Sound("sound/hero_down.wav")
hero_down_sound.set_volume(0.2)
# 供给
bullet_supply = supply.Bullet_Supply(bg_size)
bomb_supply = supply.Bomb_Supply(bg_size)


def add_small_enemies(group1, group2, num):  # 自己的和enemy的group
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def inc_speed(target, inc):  # 加速
    for each in target:
        each.speed += inc


def main(begin, flag):  # 重新开始是否进入开始界面标记 重新开始重设线程运行标记
    p = supply_time
    pygame.mixer.music.play(-1)

    # 生成飞机
    hero = myplane.MyPlane(bg_size)

    enemies = pygame.sprite.Group()

    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4  # 宏定义
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(hero.rect.midtop))  # 顶部中央,别的再了解

    # 超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8  # 一对两个
    for i in range(BULLET2_NUM // 2):  # 循环每次两个
        bullet2.append(bullet.Bullet2((hero.rect.centerx - 36, hero.rect.centery - 17)))  # 元祖
        bullet2.append(bullet.Bullet2((hero.rect.centerx + 28, hero.rect.centery - 17)))

    clock = pygame.time.Clock()

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    hero_destroy_index = 0

    score = 0
    score_font = pygame.font.Font("font/haibao.ttf", 36)

    paused = False
    pause_image = pygame.image.load("images/game_pause_pressed.png").convert_alpha()
    resume_image = pygame.image.load("images/game_resume_pressed.png").convert_alpha()
    paused_rect = pause_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10

    music_paused = False
    music_pause_image = pygame.image.load("images/music_pause_pressed.png").convert_alpha()
    music_resume_image = pygame.image.load("images/music_resume_pressed.png").convert_alpha()
    music_paused_rect = music_pause_image.get_rect()
    music_paused_rect.left, music_paused_rect.top = width - 2 * music_paused_rect.width - 20, 10

    # 游戏结束画面内容
    over_image = pygame.image.load("images/sql/background_overol.png").convert_alpha()
    gameover_font = pygame.font.Font("font/haibao.ttf", 48)
    again_pressed_image = pygame.image.load("images/sql/restart_sel.png").convert_alpha()
    again_nor_image = pygame.image.load("images/sql/restart_nor.png").convert_alpha()
    again_rect = again_pressed_image.get_rect()
    gameover_pressed_image = pygame.image.load("images/sql/quit_sel.png").convert_alpha()
    gameover_nor_image = pygame.image.load("images/sql/quit_nor.png").convert_alpha()
    gameover_rect = gameover_pressed_image.get_rect()
    online_pressed_image = pygame.image.load("images/sql/online_sel.png").convert_alpha()
    online_nor_image = pygame.image.load("images/sql/online_nor.png").convert_alpha()
    local_pressed_image = pygame.image.load("images/sql/local_sel.png").convert_alpha()
    local_nor_image = pygame.image.load("images/sql/local_nor.png").convert_alpha()
    linkerror_image = pygame.image.load("images/sql/linkerror.png").convert_alpha()
    online_rect = online_pressed_image.get_rect()
    local_rect = local_pressed_image.get_rect()
    again_image = again_nor_image
    gameover_image = gameover_nor_image
    online_image = online_nor_image
    local_image = local_nor_image
    # 开始画面内容
    start_image = pygame.image.load("images/sql/background_start.png").convert_alpha()
    gamestart_pressed_image = pygame.image.load("images/sql/gamestart_sel.png").convert_alpha()
    gamestart_nor_image = pygame.image.load("images/sql/gamestart_nor.png").convert_alpha()
    gamestart_rect = gamestart_pressed_image.get_rect()
    gamestart_rect.left, gamestart_rect.top = (width - gamestart_rect.width) // 2, 403
    rule_pressed_image = pygame.image.load("images/sql/rule_sel.png").convert_alpha()
    rule_nor_image = pygame.image.load("images/sql/rule_nor.png").convert_alpha()
    rule_rect = rule_pressed_image.get_rect()
    rule_rect.left, rule_rect.top = (width - rule_rect.width) // 2, 485
    back_pressed_image = pygame.image.load("images/sql/back_sel.png").convert_alpha()
    back_nor_image = pygame.image.load("images/sql/back_nor.png").convert_alpha()
    back_rect = back_pressed_image.get_rect()
    gamestart_image = gamestart_nor_image
    rule_image = rule_nor_image
    back_image = back_nor_image
    rule_cont_image = pygame.image.load("images/sql/background_rule.png").convert_alpha()
    name_font = pygame.font.Font("font/haibao.ttf", 40)

    # 用于切换我方生死图片
    switch_image = True
    flash = True  # 无敌闪动
    color_flash = 0  # 破纪录RGB闪动
    flashcolor = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    timer_flag = True  # 定时器执行一次
    delay = 100  # 延迟
    level = 1  # 难度
    rule_pressed = False
    enter = False
    con_flag = False
    capslock = False
    with open("namerecord.dat", "r") as f:
        name = f.read()[:12]  # 用户名
        name_size = len(name)
        f.close()
    ss = open('record.json').read()
    record = eval(base64.b64decode(ss[2:-1]))  # 所有人成绩的字典 eval()将字符串str当成有效的表达式来求值并返回计算结果
    record['Robot1'] = 0  # 防止异常设定的三个假人
    record['Robot2'] = 0
    record['Robot3'] = 0

    INV_TIME = USEREVENT + 1  # 解除我方无敌de定时器

    SUPPLY_TIME = USEREVENT + 2  # 用于检测炸弹已经过的时间
    SUPPLY1_TIME = USEREVENT + 3  # 补给定时器
    SUPPLY2_TIME = USEREVENT + 4  # p定时器

    pygame.time.set_timer(SUPPLY_TIME, 1 * 1000)
    DOUBLE_BULLET_TIME = USEREVENT  # 超级子弹定时器
    is_double_bullet = False  # 是否超级子弹

    recorded = False
    onlined = False

    life_image = pygame.image.load("images/life.png").convert_alpha()  # 生命
    life_rect = life_image.get_rect()
    life_num = 3

    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/haibao.ttf", 48)
    bomb_num = 1
    bullets = bullet1  # 初始化

    running = True

    while running:
        if paused:
            paused_image = resume_image
        else:
            paused_image = pause_image
        if music_paused:
            music_paused_image = music_resume_image
        else:
            music_paused_image = music_pause_image

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if gamestart_rect.collidepoint(event.pos):
                        begin = True
                    if rule_rect.collidepoint(event.pos):
                        rule_pressed = True
                    if back_rect.collidepoint(event.pos):
                        if not begin:  # 开始界面的
                            rule_pressed = False
                        else:
                            con_flag = False
                    if online_rect.collidepoint(event.pos):
                        if not onlined:
                            try:
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.connect(('47.114.165.253', 8026))  # 与服务器连接，需要基于局域网

                                for data in [bytes(name, 'utf-8'), bytes(str(score), 'utf-8')]:
                                    if s.recv(1024):
                                        s.send(data)
                                record1 = s.recv(1024).decode('utf-8')
                                record1 = eval(record1)
                                record.update(record1)

                                s.close()
                            except ConnectionRefusedError:
                                con_flag = True  # 结束画面绘制网络连接错误页面
                                onlined = not onlined  # 使得此次点击无效

                        if onlined:
                            ss = open('record.json').read()
                            record = eval(base64.b64decode(ss[2:-1]))  # 所有人成绩的字典
                        onlined = not onlined

            elif event.type == MOUSEMOTION:  # 当你鼠标有任何移动就会有消息, 效验按钮用
                if again_rect.collidepoint(event.pos):
                    again_image = again_pressed_image
                else:
                    again_image = again_nor_image
                if gameover_rect.collidepoint(event.pos):
                    gameover_image = gameover_pressed_image
                else:
                    gameover_image = gameover_nor_image

                if gamestart_rect.collidepoint(event.pos):
                    gamestart_image = gamestart_pressed_image
                else:
                    gamestart_image = gamestart_nor_image
                if rule_rect.collidepoint(event.pos):
                    rule_image = rule_pressed_image
                else:
                    rule_image = rule_nor_image
                if back_rect.collidepoint(event.pos):
                    back_image = back_pressed_image
                else:
                    back_image = back_nor_image
                if online_rect.collidepoint(event.pos):
                    online_image = online_pressed_image
                    local_image = local_pressed_image
                else:
                    online_image = online_nor_image
                    local_image = local_nor_image

            elif event.type == KEYDOWN:  # event.mod == KMOD_SHIFT & K_m 同时按下shift+m 不能改为and
                if not begin and enter and name_size < 13 and (
                        event.key in range(45, 57) or event.key in range(97, 122)):  # 数字-./和小写字母
                    if not capslock:
                        name = name + chr(event.key)  # 转化为字符
                    else:
                        name = name + chr(event.key - 32)
                    name_size += 1
                if event.key == K_BACKSPACE:
                    if not begin and enter and name_size > 0:
                        name = name[:-1]
                        name_size -= 1
                if event.key == K_p:
                    paused = not paused
                    if paused:
                        pygame.event.set_grab(False)
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.time.set_timer(SUPPLY1_TIME, 0)
                        pygame.mixer.pause()
                    else:
                        pygame.event.set_grab(True)
                        pygame.time.set_timer(SUPPLY_TIME, 1 * 1000)
                        pygame.time.set_timer(SUPPLY1_TIME, p * 1000)
                        pygame.time.set_timer(SUPPLY2_TIME, p * 1000)
                        pygame.mouse.set_pos(x, y)
                        pygame.mixer.unpause()
                if event.key == K_m and (not enter or begin):
                    music_paused = not music_paused
                    if music_paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if event.key == K_SPACE:
                    if enter:
                        capslock = not capslock
                    if begin:
                        if bomb_num:
                            bomb_num -= 1
                            bomb_sound.play()
                            for each in enemies:
                                if each.rect.bottom > 0:
                                    each.active = False
                if event.key == K_ESCAPE:
                    if begin:
                        life_num = 0
                if event.key == K_RETURN:
                    if not begin:
                        enter = not enter

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)  # 关闭定时器

            elif event.type == INV_TIME:
                hero.invicible = False
                pygame.time.set_timer(INV_TIME, 0)

            elif event.type == SUPPLY_TIME:  # 补给剩余时间
                p -= 1
                if p == 0:
                    p = supply_time

            elif event.type == SUPPLY1_TIME:  # 补给剩余时间
                supply_sound.play()
                if choice([True, False]):  # 随机选一个
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == SUPPLY2_TIME:
                pygame.time.set_timer(SUPPLY2_TIME, 0 * 1000)
                pygame.time.set_timer(SUPPLY1_TIME, supply_time * 1000)

        # 根据得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        screen.blit(background, (0, 0))  # 如果想暂停时可以看见当前战局可以放在下面if里面(绘制飞机上方), 不能放外面, 会重影
        # 开始界面
        if not begin:
            pygame.mouse.set_visible(True)
            screen.blit(start_image, (0, 0))
            screen.blit(gamestart_image, gamestart_rect)
            screen.blit(rule_image, rule_rect)
            screen.blit(music_paused_image,
                        (music_paused_rect.left + 10 + music_paused_rect.width, music_paused_rect.top))
            name_text = name_font.render(name, True, WHITE)  # 将一个字符串渲染成字符串, true:不要渲染
            name_rect = name_text.get_rect()
            screen.blit(name_text, ((width - name_rect.width) // 2, 320))
            if rule_pressed:
                screen.blit(rule_cont_image, (0, 0))
                screen.blit(back_image, back_rect)
            for each in small_enemies:  # 为了开始界面不单调
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)

        elif life_num and not paused:
            # 检测偶然触发 通过检测事件消息(KEYDOWN...)
            # 频繁触发 key模块里面getPress方法(返回一个事件返回所有按键的bool类型值
            # 检测用户的键盘操作
            if flag:  # 执行一次, 重新开始不执行
                flag = False
                bomb_sound.play()
                for each in enemies:  # 为了开场更帅(无敌)
                    if each.rect.bottom > 0:
                        each.active = False

                hero.invicible = True
                pygame.time.set_timer(INV_TIME, 3 * 1000)
            if timer_flag:
                timer_flag = False
                pygame.time.set_timer(SUPPLY1_TIME, supply_time * 1000)

            key_pressed = pygame.key.get_pressed()

            # 绘制补给
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, hero):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, hero):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # 子弹
            if not (delay % 10):  # 每10帧调用一次 能被整除执行
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((hero.rect.centerx - 36, hero.rect.centery - 17))
                    bullets[bullet2_index + 1].reset((hero.rect.centerx + 28, hero.rect.centery - 17))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(
                        (hero.rect.centerx - 3, hero.rect.top))  # 每次reset吧玩家当前位置传进去  hero.rect.midtop元祖改
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检查命中否
            for b in bullets:
                if b.active:  # false就是不存在的状态 活动的才能击中敌机
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制敌方飞机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)  # 宽度
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)

                    if each.rect.bottom == -50:  # 只需要一次
                        enemy3_fly_sound.play(-1)  # 循环播放
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()  # 放里面防止重复播放占用通道pygame.mixer.set_num_channels()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)  # 宽度
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 检测我方飞机被撞
            enemies_down = pygame.sprite.spritecollide(hero, enemies, False, pygame.sprite.collide_mask)  # 指定调用具体函数
            # 和里面任何一个精灵 返回一个列表 (没用mask 用这个会是矩形区域)
            if enemies_down and not hero.invicible:
                hero.active = False
                for e in enemies_down:
                    e.active = False

            # 绘制我方飞机
            pygame.mouse.set_visible(False)
            x, y = pygame.mouse.get_pos()  # 获得鼠标当前位置
            hero.rect.left, hero.rect.top = x - hero.rect.width // 2, y - hero.rect.height // 2
            pygame.event.set_grab(True)  # 设置鼠标在屏幕内
            if x < 0:
                pygame.mouse.set_pos(0, y)
            if x > width:
                pygame.mouse.set_pos(width, y)
            if y < 60:
                pygame.mouse.set_pos(x, 60)
            if y > height - 60:
                pygame.mouse.set_pos(x, height - 60)
            if hero.active:
                if not hero.invicible:
                    if switch_image:
                        screen.blit(hero.image1, hero.rect)
                    else:
                        screen.blit(hero.image2, hero.rect)
                else:  # 无敌闪动
                    if not (delay % 10):
                        flash = not flash
                    if flash:
                        if switch_image:
                            screen.blit(hero.image1, hero.rect)
                        else:
                            screen.blit(hero.image2, hero.rect)
            else:
                if not (delay % 3):
                    if hero_destroy_index == 0:
                        hero_down_sound.play()  # 需要只播放一次
                    screen.blit(hero.destroy_images[hero_destroy_index], hero.rect)
                    hero_destroy_index = (hero_destroy_index + 1) % 4
                    if hero_destroy_index == 0:
                        life_num -= 1
                        hero.reset()
                        pygame.time.set_timer(INV_TIME, 3 * 1000)

        if life_num and begin:  # 游戏开始包括暂停
            # 暂停绘制
            screen.blit(paused_image, paused_rect)
            screen.blit(music_paused_image, music_paused_rect)
            # 绘制炸弹数量
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)  # 将一个字符串渲染成, true:不要渲染
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))
            # 绘制生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))
            # 得分
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)  # 将一个字符串渲染成, true:不要渲染
            screen.blit(score_text, (10, 5))
        # 绘制游戏结束画面
        elif life_num == 0:
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)
            pygame.time.set_timer(SUPPLY_TIME, 0)
            pygame.time.set_timer(SUPPLY1_TIME, 0)
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            if not recorded:
                recorded = True
                record_score = record[max(record, key=record.get)]
                with open("record.json", "w") as f:
                    if (name in record and record[name] < score) or name not in record:  # 判断有这个键并且记录小于当前成绩再记录
                        record[name] = score
                    jsObj = json.dumps(record)  # json.dumps()用于将dict类型的数据转成str
                    f.write(str(base64.b64encode(str(jsObj).encode('utf-8'))))
                    f.close()
                if score > record_score:
                    record_score = score
                with open("namerecord.dat", "w") as f:
                    f.write(str(name))
                    f.close()
            record = dict(sorted(record.items(), key=lambda record: record[1], reverse=True))  # 排序 降序,不强制转化会变成list

            screen.blit(over_image, (0, 0))
            count = 0
            for key in record.keys():  # 获取字典第一个元素 第一名
                count += 1
                if count == 1:
                    count = 0
                    break
            recordn1_score_text = score_font.render("%s:" % key, True, (250, 236, 117))
            screen.blit(recordn1_score_text, (100, 60))
            records1_score_text = score_font.render("%d" % record[key], True, (250, 236, 117))
            records1_score_rect = records1_score_text.get_rect()
            screen.blit(records1_score_text, (353 - records1_score_rect.width, 100))
            for key in record.keys():  # 获取字典第二个元素
                count += 1
                if count == 2:
                    count = 0
                    break
            recordn2_score_text = score_font.render("%s:" % key, True, (235, 235, 235))
            screen.blit(recordn2_score_text, (100, 140))
            records2_score_text = score_font.render("%d" % record[key], True, (235, 235, 235))
            records2_score_rect = records2_score_text.get_rect()
            screen.blit(records2_score_text, (353 - records2_score_rect.width, 180))
            for key in record.keys():  # 获取字典第三个元素
                count += 1
                if count == 3:
                    count = 0
                    break
            recordn3_score_text = score_font.render("%s:" % key, True, (243, 168, 87))
            screen.blit(recordn3_score_text, (100, 220))
            records3_score_text = score_font.render("%d" % record[key], True, (243, 168, 87))
            records3_score_rect = records3_score_text.get_rect()
            screen.blit(records3_score_text, (353 - records3_score_rect.width, 260))

            gameover_text1 = gameover_font.render(str(score), True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, 388

            gameover_text2 = gameover_font.render("%s的得分:" % name, True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2, 325
            # 破纪录特效
            if record[name] == score:
                if not (delay % 30):
                    color_flash += 1
                    if color_flash == len(flashcolor):
                        color_flash = 0
                gameover_text1 = gameover_font.render(str(score), True, flashcolor[color_flash])
                screen.blit(gameover_text1, gameover_text1_rect)
                gameover_text2 = gameover_font.render("%s的成绩:" % name, True, flashcolor[color_flash])
                screen.blit(gameover_text2, gameover_text2_rect)
            else:
                screen.blit(gameover_text1, gameover_text1_rect)
                screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = (width - again_rect.width) // 2, 452
            screen.blit(again_image, again_rect)

            online_rect.left, online_rect.top = (width - online_rect.width) // 2, 510
            if not onlined:
                screen.blit(online_image, online_rect)
            else:
                screen.blit(local_image, online_rect)

            if con_flag:
                screen.blit(linkerror_image, (0, 0))
                screen.blit(back_image, back_rect)

            gameover_rect.left, gameover_rect.top = (width - gameover_rect.width) // 2, 565
            screen.blit(gameover_image, gameover_rect)

            if pygame.mouse.get_pressed()[0]:  # 按下鼠标左键
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                    main(True, False)  # 重新开始不用无敌和爆炸
                elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[
                    1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()

        if not (delay % 5):
            switch_image = not switch_image  # 为了让尾气更好看

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    try:
        main(False, True)
    except SystemExit:  # 和IDLE分开
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

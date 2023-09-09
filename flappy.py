import random  # For generating random numbers
import pygame
import sys
from pygame.locals import *
import os
import math
import time
# I see no reason to disable screensaver for this tool.
os.environ["SDL_VIDEO_ALLOW_SCREENSAVER"] = "1"

# Maybe people want to keep watching the joystick feedback even when this
# window doesn't have focus. Possibly by capturing this window into OBS.
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# A tiny performance/latency hit isn't a problem here. Instead, it's more
# important to keep the desktop compositing effects running fine. Disabling
# compositing is known to cause issues on KDE/KWin/Plasma/X11 on Linux.
os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"

# Global Variables for the game
FPS = 30
screen_width = 289
scr_height = 511
display_screen_window = pygame.display.set_mode((screen_width, scr_height))
play_ground = scr_height * 0.8
game_image = {}
game_audio_sound = {}
base = 'images/Base.png'
TailUp = 'images/mario_TailUp.png'
TailDown = 'images/mario_TailDown.png'
TailMiddle = 'images/mario_TailMiddle.png'
TailFroze = 'images/mario_freeze.png'
RunMiddle = 'images/mario_run.png'
RunStart = 'images/mario_startRun.png'
RunEnd = 'images/mario_runEnd.png'
Still = 'images/mario_still.png'
die = 'images/mario_die.png'
start = 'images/start.png'
gameOverScreen = 'images/gameOver.png'
restart = 'images/restart.png'
pipe_image = 'images/pipe.png'
coin1 = 'images/coin1.png'
coin2 = 'images/coin2.png'
PWing1 = 'images/PWing1.png'
PWing2 = 'images/PWing2.png'
coin3 = 'images/coin3.png'
coin4 = 'images/coin3.png'
Bird1 = 'images/Bird1.png'
Bird2 = 'images/Bird2.png'
Bird3 = 'images/Bird3.png'
Bird4 = 'images/Bird4.png'
Bird5 = 'images/Bird5.png'
Bird6 = 'images/Bird6.png'
Bird7 = 'images/Bird7.png'
Bird8 = 'images/Bird8.png'
Bird9 = 'images/Bird9.png'
Bird10 = 'images/Bird10.png'
Bird11 = 'images/Bird11.png'
Bird12 = 'images/Bird12.png'
Bird13 = 'images/Bird13.png'
Bird14 = 'images/Bird14.png'
Bird15 = 'images/Bird15.png'
Bird16 = 'images/Bird16.png'
Bird17 = 'images/Bird17.png'
gameLevel = 1
p_x = 0
p_y = 0
b_x = 0
score = 0
coins = 0
lives = 3
last_p_y = p_y
this_p_x = 0
last_p_x = 0
spriteInt = 0
p_wing = 0
scroll = 0
crash_test = False  # hit box detection
Bird3_dead = False
start_screen = True
freezeMario = False
die_animation = False


def load_forward_sprites():
    game_image['TailFroze'] = pygame.image.load(TailFroze).convert_alpha()
    game_image['TailUp'] = pygame.image.load(TailUp).convert_alpha()
    game_image['TailDown'] = pygame.image.load(TailDown).convert_alpha()
    game_image['TailMiddle'] = pygame.image.load(TailMiddle).convert_alpha()
    game_image['RunMiddle'] = pygame.image.load(RunMiddle).convert_alpha()
    game_image['RunStart'] = pygame.image.load(RunStart).convert_alpha()
    game_image['RunEnd'] = pygame.image.load(RunEnd).convert_alpha()
    game_image['Still'] = pygame.image.load(Still).convert_alpha()


def flip_sprites_left():
    game_image['TailFroze'] = pygame.transform.flip(game_image['TailFroze'], True, False)
    game_image['TailUp'] = pygame.transform.flip(game_image['TailUp'], True, False)
    game_image['TailDown'] = pygame.transform.flip(game_image['TailDown'], True, False)
    game_image['TailMiddle'] = pygame.transform.flip(game_image['TailMiddle'], True, False)
    game_image['RunMiddle'] = pygame.transform.flip(game_image['RunMiddle'], True, False)
    game_image['RunStart'] = pygame.transform.flip(game_image['RunStart'], True, False)
    game_image['RunEnd'] = pygame.transform.flip(game_image['RunEnd'], True, False)
    game_image['Still'] = pygame.transform.flip(game_image['Still'], True, False)


def start_Bird1():
    global ran_Bird
    n_Bird = get_Random_Bird()
    ran_Bird = [
        {'x': screen_width, 'y': n_Bird[0]['y']},
    ]


def start_Bird2():
    global ran_Bird2
    n_Bird2 = get_Random_Bird2()
    ran_Bird2 = [
        {'x': screen_width, 'y': n_Bird2[0]['y']},
    ]


def start_Bird3():
    global ran_Bird3
    n_Bird3 = get_Random_Bird3()
    ran_Bird3 = [
        {'x': screen_width, 'y': n_Bird3[0]['y']},
    ]


def start_Bird4():
    global ran_Bird4
    n_Bird4 = get_Random_Bird4()
    ran_Bird4 = [
        {'x': screen_width, 'y': n_Bird4[0]['y']},
    ]


def start_Coin2():
    global ran_coin2
    n_coin3 = get_Random_Coins2()
    n_coin4 = get_Random_Coins2()
    ran_coin2 = [
        {'x': screen_width + 200, 'y': n_coin3[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': n_coin4[0]['y']},
    ]


def start_Coin3():
    global ran_coin3
    n_coin5 = get_Random_Coins3()
    n_coin6 = get_Random_Coins3()
    ran_coin3 = [
        {'x': screen_width + 200, 'y': n_coin5[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': n_coin6[0]['y']},
    ]


def scroll_background():
    global scroll, tiles, die_animation
    i = 0
    while i < tiles:
        x = game_image['background'].get_width() * i + scroll
        display_screen_window.blit(game_image['background'], (x, 0))
        i += 1
    if not die_animation:
        scroll -= 2
        if abs(scroll) > game_image['background'].get_width():
            scroll = 0


def game_over(upper_pipes, lower_pipes, random_coin, random_coin2, random_coin3, random_Bird, random_Bird2,
              random_Bird3, random_Bird4):
    global p_x, p_y, b_x, play_ground, crash_test, gameLevel, start_screen, die_animation
    if pygame.mixer.get_busy():
        scroll_background()
        random_Stuff(upper_pipes, lower_pipes, random_coin, random_coin2, random_coin3, random_Bird, random_Bird2,
                     random_Bird3, ran_Bird4)
        display_screen_window.blit(game_image['base'], (b_x, play_ground))
        score_count()
        coin_count()
        level_lives_count()
        display_screen_window.blit(game_image['die'], (p_x, p_y))

    if lives == 0 and not pygame.mixer.get_busy():
        start_screen = True
        display_screen_window.blit(game_image['gameOverScreen'], (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)
        die_animation = False

    if lives > 0 and not pygame.mixer.get_busy():
        display_screen_window.blit(game_image['restart'], (0, 0))
        display_screen_window.blit(game_image['numbers'][lives], (160, 240))
        pygame.display.update()
        pygame.time.delay(2000)
        p_x = 150
        p_y = 150
        die_animation = False
        if gameLevel == 1:
            game_audio_sound['Overworld'].play()
        if gameLevel == 2:
            game_audio_sound['Underground'].play()
        if gameLevel == 3:
            game_audio_sound['Athletic'].play()
        if gameLevel == 4:
            game_audio_sound['desert'].play()
        if gameLevel == 5:
            game_audio_sound['Music Box'].play()
        if gameLevel == 6:
            game_audio_sound['PipeMaze'].play()
        if gameLevel == 7:
            game_audio_sound['Airship'].play()
        if gameLevel == 8:
            game_audio_sound['Castle'].play()


def flap_da_wings():
    global p_y, p_vx, p_mvx, p_accuracy, die_animation, p_flap, last_p_y
    # if die_animation and not p_flap:
    #     last_p_y = p_y
    #     p_vx = p_flap_accuracy
    if p_vx < p_mvx and not p_flap:
        p_vx += p_accuracy
    p_height = game_image['TailUp'].get_height()
    if not die_animation:
        p_y = p_y + min(p_vx, play_ground - p_y - p_height)
    else:
        p_y = p_y + min(p_vx, p_y - p_height)


def main_gameplay():
    global crash_test, start_screen, p_flap, lives, die_animation, Bird3_dead, coin_Vx, coin2_Vx, coin3_Vx, \
        ran_coin2, ran_coin3
    if not die_animation:
        flap_da_wings()

        for pip_upper, pip_lower in zip(up_pipes, low_pipes):  # set different lower and upper pipe speeds
            pip_upper['x'] += pip_Vx
            pip_lower['x'] += pip_Vx
        for coin_random in ran_coin:  # set different lower and upper pipe speeds
            coin_random['x'] += coin_Vx

        if ran_coin2:

            if 0 <= ran_coin2[0]['x'] < 5 and gameLevel == 5:
                new_coin2 = get_Random_Coins2()
                ran_coin2.append(new_coin2[0])
            for coin2_random in ran_coin2:
                coin2_random['x'] += coin2_Vx
            if ran_coin2[0]['x'] < -game_image['pipe'][0].get_width():
                ran_coin2.pop(0)

        if ran_coin3:
            if 0 <= ran_coin3[0]['x'] < 5 and gameLevel == 5:
                new_coin3 = get_Random_Coins3()
                ran_coin3.append(new_coin3[0])
            for coin3_random in ran_coin3:
                coin3_random['x'] += coin3_Vx
            if ran_coin3[0]['x'] < -game_image['pipe'][0].get_width():
                ran_coin3.pop(0)

        if ran_Bird2:
            if 0 <= ran_Bird2[0]['x'] < 3 and (gameLevel == 2 or gameLevel == 6 or gameLevel == 7):
                new_Bird2 = get_Random_Bird2()
                ran_Bird2.append(new_Bird2[0])
            for Bird2_random in ran_Bird2:
                Bird2_random['x'] += Bird2_Vx
            if ran_Bird2[0]['x'] < -game_image['Bird2_img'][0].get_width():
                ran_Bird2.pop(0)

        if ran_Bird4:
            if 0 <= ran_Bird4[0]['x'] < 4 and (gameLevel == 8):
                new_Bird4 = get_Random_Bird4()
                ran_Bird4.append(new_Bird4[0])
            for Bird4_random in ran_Bird4:
                Bird4_random['x'] += Bird3_Vx
            if ran_Bird4[0]['x'] < -game_image['Bird4_img'].get_width():
                ran_Bird4.pop(0)

        if ran_Bird3:
            if 0 < ran_Bird3[0]['x'] < 4 and (gameLevel == 3 or gameLevel == 6 or gameLevel == 7):
                game_image['Bird3_img'] = (
                    pygame.image.load(Bird9).convert_alpha(),
                    pygame.image.load(Bird10).convert_alpha(),
                    pygame.image.load(Bird11).convert_alpha(),
                    pygame.image.load(Bird12).convert_alpha(),
                )
                new_Bird3 = get_Random_Bird3()
                ran_Bird3.append(new_Bird3[0])
            for Bird3_random in ran_Bird3:
                Bird3_random['x'] += Bird3_Vx
                if Bird3_dead and Bird3_random['y'] <= 381:
                    ran_Bird3[0]['y'] -= Bird3_Vx
            if ran_Bird3[0]['x'] < -game_image['Bird3_img'][0].get_width():
                ran_Bird3.pop(0)
                game_image['Bird3_img'] = (
                    pygame.image.load(Bird9).convert_alpha(),
                    pygame.image.load(Bird10).convert_alpha(),
                    pygame.image.load(Bird11).convert_alpha(),
                    pygame.image.load(Bird12).convert_alpha(),
                )
                Bird3_dead = False

        if ran_Bird:
            if 0 <= ran_Bird[0]['x'] < 3 and (gameLevel == 4 or gameLevel == 7):
                new_Bird = get_Random_Bird()
                ran_Bird.append(new_Bird[0])
            for Bird_random in ran_Bird:
                Bird_random['x'] += Bird1_Vx
            if ran_Bird[0]['x'] < -game_image['Bird_img'][0].get_width():
                ran_Bird.pop(0)

        if 0 < up_pipes[0]['x'] < 5:
            new_pip = get_Random_Pipes()
            up_pipes.append(new_pip[0])
            low_pipes.append(new_pip[1])
            new_coin = get_Random_Coins()
            ran_coin.append(new_coin[0])

        if up_pipes[0]['x'] < -game_image['pipe'][0].get_width():
            up_pipes.pop(0)
            low_pipes.pop(0)
            ran_coin.pop(0)

        scroll_background()
        random_Stuff(up_pipes, low_pipes, ran_coin, ran_coin2, ran_coin3, ran_Bird, ran_Bird2, ran_Bird3, ran_Bird4)
        display_screen_window.blit(game_image['base'], (b_x, play_ground))

        if crash_test:
            lives -= 1
            game_audio_sound['Overworld'].stop()
            game_audio_sound['Underground'].stop()
            game_audio_sound['Athletic'].stop()
            game_audio_sound['desert'].stop()
            game_audio_sound['Music Box'].stop()
            game_audio_sound['PipeMaze'].stop()
            game_audio_sound['Airship'].stop()
            game_audio_sound['Castle'].stop()
            die_animation = True
            crash_test = False
            game_audio_sound['die'].play()
        else:
            sprite_animations()
            crash_test = is_Colliding(up_pipes, low_pipes, ran_coin, ran_coin2, ran_coin3, ran_Bird, ran_Bird2,
                                      ran_Bird3, ran_Bird4)
            check_Points()

    else:
        game_over(up_pipes, low_pipes, ran_coin, ran_coin2, ran_coin3, ran_Bird, ran_Bird2, ran_Bird3, ran_Bird4)
        flap_da_wings()

    if p_flap:  # do not move, moving will break mario sprite changing from pipe walking to flying
        p_flap = False
    score_count()
    coin_count()
    level_lives_count()

    pygame.display.update()
    time_clock.tick(FPS)


def level_lives_count():
    display_screen_window.blit(game_image['numbers'][gameLevel], (76, 454))  # world number
    display_screen_window.blit(game_image['numbers'][lives], (62, 468))  # lives


def score_count():
    d = [int(x) for x in list(str(score))]
    w = 0
    for digit in d:
        w += game_image['numbers'][digit].get_width()
    Xoffset = (screen_width - w) / 1.07  # x axis numbers
    for digit in d:
        display_screen_window.blit(game_image['numbers'][digit], (Xoffset, scr_height * 0.917))  # y axis numbers
        Xoffset += game_image['numbers'][digit].get_width()


def coin_count():
    e = [int(x) for x in list(str(coins))]
    w = 0
    for digit in e:
        w += game_image['numbers'][digit].get_width()
    Xoffset = (screen_width - w) / 1.07  # x axis numbers
    for digit in e:
        display_screen_window.blit(game_image['numbers'][digit], (Xoffset, scr_height * 0.889))  # y axis numbers
        Xoffset += game_image['numbers'][digit].get_width()


def random_Stuff(upper_pipes, lower_pipes, random_coin, random_coin2, random_coin3, random_Bird, random_Bird2,
                 random_Bird3, random_Bird4):
    for pip_upper, pip_lower in zip(upper_pipes, lower_pipes):  # Display pipe new locations
        display_screen_window.blit(game_image['pipe'][0], (pip_upper['x'], pip_upper['y']))
        display_screen_window.blit(game_image['pipe'][1], (pip_lower['x'], pip_lower['y']))

    for coin_random in random_coin:  # Display coin new locations
        display_screen_window.blit(game_image['coin_img'][spriteInt], (coin_random['x'], coin_random['y']))

    for coin2_random in random_coin2:  # Display coin new locations
        display_screen_window.blit(game_image['coin_img'][spriteInt], (coin2_random['x'], coin2_random['y']))

    for coin3_random in random_coin3:  # Display coin new locations
        display_screen_window.blit(game_image['coin_img'][spriteInt], (coin3_random['x'], coin3_random['y']))

    for Bird_random in random_Bird:  # Display Bird new locations
        display_screen_window.blit(game_image['Bird_img'][spriteInt], (Bird_random['x'], Bird_random['y']))

    for Bird2_random in random_Bird2:  # Display Bird2 new locations
        display_screen_window.blit(game_image['Bird2_img'][spriteInt], (Bird2_random['x'], Bird2_random['y']))

    for Bird3_random in random_Bird3:  # Display Bird new locations
        display_screen_window.blit(game_image['Bird3_img'][spriteInt], (Bird3_random['x'], Bird3_random['y']))

    for Bird4_random in random_Bird4:  # Display Bird new locations
        display_screen_window.blit(game_image['Bird4_img'], (Bird4_random['x'], Bird4_random['y']))


def sprite_animations():
    global p_x, p_y, this_p_x, last_p_x, forward, reverse, pipe_walking, freezeMario, p_wing
    if 0 <= p_x <= 262:
        if forward:
            p_x += 3
        if reverse:
            p_x -= 4
    if p_x < 0:
        p_x = 0
    if p_x > 262:
        p_x = 262

    if not freezeMario:
        if p_y <= 381 and not pipe_walking:
            display_screen_window.blit(game_image['PWing'][p_wing], (101, 454))
            if p_y > last_p_y:
                display_screen_window.blit(game_image['TailUp'], (p_x, p_y))  # falling sprite
            elif 25 < (last_p_y - p_y) <= 40:
                display_screen_window.blit(game_image['TailDown'], (p_x, p_y))  # middle lift sprite
            elif (last_p_y - p_y) <= 25:
                display_screen_window.blit(game_image['TailMiddle'], (p_x, p_y))  # middle animation sprite
            this_p_x = 0
            last_p_x = this_p_x

        if p_y >= 381 or pipe_walking:
            if forward or reverse:
                display_screen_window.blit(game_image['PWing'][p_wing], (101, 454))
                if 0 <= this_p_x - last_p_x <= 1:
                    this_p_x += 1
                    display_screen_window.blit(game_image['RunStart'], (p_x, p_y))  # run
                elif 2 <= this_p_x - last_p_x <= 3:
                    this_p_x += 1
                    display_screen_window.blit(game_image['RunMiddle'], (p_x, p_y))  # run
                elif 4 <= this_p_x - last_p_x <= 5:
                    this_p_x += 1
                    display_screen_window.blit(game_image['RunEnd'], (p_x, p_y))  # run
                elif 6 <= this_p_x - last_p_x <= 7:
                    this_p_x += 1
                    display_screen_window.blit(game_image['RunMiddle'], (p_x, p_y))  # run
                else:
                    display_screen_window.blit(game_image['RunMiddle'], (p_x, p_y))  # run
                    this_p_x = 0
                    last_p_x = this_p_x
            if not forward and not reverse:
                display_screen_window.blit(game_image['Still'], (p_x, p_y))
    if freezeMario:
        display_screen_window.blit(game_image['TailFroze'], (p_x, p_y))


def check_Points():
    global background, score, gameLevel, event, start_time, end_time, elapsed_time
    if score == 1 and gameLevel < 2:
        gameLevel += 1
        game_audio_sound['Overworld'].stop()
        game_audio_sound['Underground'].play()
        background = 'images/underground.png'
        game_image['background'] = pygame.image.load(background).convert()
        start_Bird2()
    if score == 2 and gameLevel < 3:
        gameLevel += 1
        game_audio_sound['Underground'].stop()
        game_audio_sound['Athletic'].play()
        background = 'images/athletic.png'
        game_image['background'] = pygame.image.load(background).convert()
        start_Bird3()
    if score == 3 and gameLevel < 4:
        gameLevel += 1
        game_audio_sound['Athletic'].stop()
        game_audio_sound['desert'].play()
        background = 'images/desert.png'
        game_image['background'] = pygame.image.load(background).convert()
        pipe_img = 'images/pipe2.png'
        game_image['pipeFlip'] = pygame.transform.flip(pygame.image.load(pipe_img).convert_alpha(), True, False)
        game_image['pipe'] = (pygame.transform.rotate(game_image['pipeFlip'], 180),
                              pygame.image.load(pipe_img).convert_alpha()
                              )
        start_Bird1()

    if score == 4 and gameLevel < 5:

        gameLevel += 1
        game_audio_sound['desert'].stop()
        game_audio_sound['Music Box'].play()
        background = 'images/clouds.png'
        game_image['background'] = pygame.image.load(background).convert()
        pipe_img = 'images/pipe.png'
        game_image['pipeFlip'] = pygame.transform.flip(pygame.image.load(pipe_img).convert_alpha(), True, False)
        game_image['pipe'] = (pygame.transform.rotate(game_image['pipeFlip'], 180),
                              pygame.image.load(pipe_img).convert_alpha()
                              )
        start_Coin2()
        start_Coin3()
        start_time = time.time()

    if gameLevel == 5 or gameLevel == 6 or gameLevel == 7 or gameLevel == 8:
        end_time = time.time()
        elapsed_time = end_time - start_time

    if gameLevel < 6 and elapsed_time >= 1:  # 68
        gameLevel += 1
        game_audio_sound['Music Box'].stop()
        game_audio_sound['PipeMaze'].play()
        background = 'images/PipeMaze.png'
        game_image['background'] = pygame.image.load(background).convert()
        start_time = time.time()
        elapsed_time = 0.00
        start_Bird2()
        start_Bird3()

    if gameLevel < 7 and elapsed_time >= 1:  # 175
        gameLevel += 1
        game_audio_sound['PipeMaze'].stop()
        game_audio_sound['Airship'].play()
        background = 'images/Airship.png'
        game_image['background'] = pygame.image.load(background).convert()
        pipe_img = 'images/pipe3.png'
        game_image['pipeFlip'] = pygame.transform.flip(pygame.image.load(pipe_img).convert_alpha(), True, False)
        game_image['pipe'] = (pygame.transform.rotate(game_image['pipeFlip'], 180),
                              pygame.image.load(pipe_img).convert_alpha()
                              )
        start_time = time.time()
        elapsed_time = 0.00
        start_Bird2()
        start_Bird3()
        start_Bird1()

    if gameLevel < 8 and elapsed_time >= 1:   # 175
        gameLevel += 1
        game_audio_sound['Airship'].stop()
        game_audio_sound['Castle'].play()
        background = 'images/Castle.png'
        game_image['background'] = pygame.image.load(background).convert()
        pipe_img = 'images/pipe4.png'
        game_image['pipeFlip'] = pygame.transform.flip(pygame.image.load(pipe_img).convert_alpha(), True, False)
        game_image['pipe'] = (pygame.transform.rotate(game_image['pipeFlip'], 180),
                              pygame.image.load(pipe_img).convert_alpha()
                              )
        start_time = time.time()
        elapsed_time = 0.00
        start_Bird4()


def is_Colliding(upper_pipes, lower_pipes, random_coin, random_coin2, random_coin3, random_Bird, random_Bird2,
                 random_Bird3, random_Bird4):
    global p_x, p_y, p_flap, forward, pipe_walking, score, coin_h, Bird_h, Bird2_h, Bird3_h, freezeMario, \
        unfreezeMario, last_p_y, p_vx, p_flap_accuracy, coins, lives, Bird3_dead

    if p_y > play_ground - 25 or p_y < 0:  # out of bounds
        p_flap = True
        last_p_y = p_y
        p_vx = p_flap_accuracy
        return True
    elif p_x == 0:
        p_flap = True
        last_p_y = p_y
        p_vx = p_flap_accuracy
        return True

    for Bird in random_Bird:  # bird hit box
        Bird_h = game_image['Bird_img'][0].get_height() - 1
        Bird_w = game_image['Bird_img'][0].get_width() * 0.45 - 1
        if abs(p_y - Bird['y']) < Bird_w and abs(p_x - Bird['x']) < Bird_w:
            p_flap = True
            last_p_y = p_y
            p_vx = p_flap_accuracy
            return True

    for Bird_4 in random_Bird4:  # bird hit box
        Bird_h = game_image['Bird4_img'].get_height() / 2
        Bird_w = game_image['Bird4_img'].get_width() / 2
        if abs(p_y - 10 - Bird_4['y']) < Bird_h and abs(p_x - Bird_4['x']) < Bird_w:
            p_flap = True
            last_p_y = p_y
            p_vx = p_flap_accuracy
            return True

    for Bird_2 in random_Bird2:
        Bird2_h = game_image['Bird2_img'][0].get_height() - 1
        Bird2_w = game_image['Bird2_img'][0].get_width() * 0.45 - 1
        if abs(p_y - Bird_2['y']) < Bird2_w and abs(p_x - Bird_2['x']) < Bird2_w:
            pygame.time.set_timer(unfreezeMario, 600)
            freezeMario = True

    for Bird_3 in random_Bird3:
        mario_h = game_image['TailUp'].get_height() / 2
        mario_w = game_image['TailUp'].get_width() / 2
        Bird3_h = game_image['Bird3_img'][0].get_height() / 2
        Bird3_w = game_image['Bird3_img'][0].get_width() / 2
        if abs(p_y + mario_h - Bird_3['y'] + Bird3_h - 10) < Bird3_h - 10 \
                and abs(p_x + mario_w - Bird_3['x'] - Bird3_w) < Bird3_w:
            score += 1
            game_audio_sound['kill'].play()
            last_p_y = p_y
            p_vx = p_flap_accuracy
            p_flap = True
            Bird3_dead = True
            game_image['Bird3_img'] = (
                pygame.image.load(Bird13).convert_alpha(),
                pygame.image.load(Bird14).convert_alpha(),
                pygame.image.load(Bird15).convert_alpha(),
                pygame.image.load(Bird16).convert_alpha(),
            )



        if abs(p_y - mario_h - Bird_3['y'] - Bird3_h + 10) < Bird3_h \
                and abs(p_x + mario_w - Bird_3['x'] - Bird3_w + 5) < Bird3_w:
            p_flap = True
            last_p_y = p_y
            p_vx = p_flap_accuracy
            return True

    # coin hit box
    for coin in random_coin:
        coin_h = game_image['coin_img'][0].get_height()
        coin_w = game_image['coin_img'][0].get_width() * 1.5
        if abs(p_y - coin['y']) < coin_w and abs(p_x - coin['x']) < coin_w:
            score += 1
            coins += 1
            a = random_coin.index(coin)
            random_coin[a] = {'x': 0, 'y': 0}  # move coin off-screen if collected
            if coins > 99:
                game_audio_sound['1UP'].play()
                lives += 1
                coins = 0
            else:
                game_audio_sound['coin'].play()
            if lives > 8:
                lives = 9

    for coin_2 in random_coin2:
        coin_h = game_image['coin_img'][0].get_height()
        coin_w = game_image['coin_img'][0].get_width() * 1.5
        if abs(p_y - coin_2['y']) < coin_w and abs(p_x - coin_2['x']) < coin_w:
            score += 1
            coins += 1
            a = random_coin2.index(coin_2)
            random_coin2[a] = {'x': 0, 'y': 0}  # move coin off-screen if collected
            if coins > 99:
                game_audio_sound['1UP'].play()
                lives += 1
                coins = 0
            else:
                game_audio_sound['coin'].play()
            if lives > 8:
                lives = 9

    for coin_3 in random_coin3:
        coin_h = game_image['coin_img'][0].get_height()
        coin_w = game_image['coin_img'][0].get_width() * 1.5
        if abs(p_y - coin_3['y']) < coin_w and abs(p_x - coin_3['x']) < coin_w:
            score += 1
            coins += 1
            a = random_coin3.index(coin_3)
            random_coin3[a] = {'x': 0, 'y': 0}  # move coin off-screen if collected
            if coins > 99:
                game_audio_sound['1UP'].play()
                lives += 1
                coins = 0
            else:
                game_audio_sound['coin'].play()
            if lives > 8:
                lives = 9

    # upper pipe hit box
    for pipe in upper_pipes:
        pip_h = game_image['pipe'][0].get_height()
        pip_w = game_image['pipe'][0].get_width() / 2
        # calculate hit box on side of pipes
        if p_y < pip_h + pipe['y'] and abs(p_x - pipe['x']) < pip_w:
            if p_flap or forward:
                p_x = p_x - 7
            else:
                p_x = p_x - 4

        # calculate hit box on bottom of pipes
        if abs(p_y - pipe['y'] + 4) < pip_h and abs(p_x - pipe['x'] - 10) < pip_w:
            p_y = pip_h + pipe['y'] + 2
            if p_flap:
                p_x = p_x + 2
            if forward:
                p_x = p_x + 3
            if reverse:
                p_x = p_x + 6

    # lower pipe hit box
    for pipe in lower_pipes:
        mario_h = game_image['Still'].get_height()
        pip_w = game_image['pipe'][0].get_width() / 2
        # calculate hit box on side of pipes
        if (p_y + mario_h > pipe['y']) and abs(p_x - pipe['x']) < pip_w:
            if p_flap or forward:
                p_x = p_x - 7
            else:
                p_x = p_x - 4

        if abs(p_y + mario_h + 4) > pipe['y'] and abs(p_x - pipe['x'] - 10) < pip_w:
            pipe_walking = True
            p_x = p_x - 4
            if forward or reverse:
                p_x = p_x + 4
            p_y = pipe['y'] - 10 - mario_h

        if p_flap or p_y > 381:
            pipe_walking = False

    return False


def get_Random_Pipes():
    # Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    pip_h = game_image['pipe'][0].get_height()  # checks pipe img height (320)
    off_s = scr_height / 3
    #  set minimum pipe height
    yes2 = off_s + random.randrange(0, int(scr_height - game_image['base'].get_height() - 1.2 * off_s))
    pipeX = screen_width  # spacing (screen_width + 10)
    y1 = pip_h - yes2 + off_s
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': yes2},  # lower Pipe
    ]
    return pipe


def get_Random_Coins():
    global spriteInt
    yesCoin = random.randrange(20, 370)
    coinX = screen_width
    coin = [
        {'x': coinX, 'y': yesCoin},  # coin
    ]
    return coin


def get_Random_Coins2():
    global spriteInt
    yesCoin = random.randrange(50, 300)
    coinX = screen_width
    coin = [
        {'x': coinX, 'y': yesCoin},  # coin
    ]
    return coin


def get_Random_Coins3():
    global spriteInt
    yesCoin = random.randrange(50, 300)
    coinX = screen_width
    coin = [
        {'x': coinX, 'y': yesCoin},  # coin
    ]
    return coin


def get_Random_Bird():
    global spriteInt
    yesBird = random.randrange(20, 370)
    BirdX = screen_width
    Bird = [
        {'x': BirdX, 'y': yesBird}
    ]
    return Bird


def get_Random_Bird2():
    global spriteInt
    yesBird2 = random.randrange(20, 370)
    Bird2X = screen_width
    Bird_2 = [
        {'x': Bird2X, 'y': yesBird2}
    ]
    return Bird_2


def get_Random_Bird3():
    global spriteInt
    yesBird3 = random.randrange(20, 370)
    Bird3X = screen_width
    Bird_3 = [
        {'x': Bird3X, 'y': yesBird3}
    ]
    return Bird_3


def get_Random_Bird4():
    yesBird4 = random.randrange(20, 370)
    Bird4X = screen_width
    Bird_4 = [
        {'x': Bird4X, 'y': yesBird4}
    ]
    return Bird_4


class joystick_handler(object):
    def __init__(self, id):
        self.id = id
        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes = self.joy.get_numaxes()
        self.numbuttons = self.joy.get_numbuttons()
        self.numhats = self.joy.get_numhats()
        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))
        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))
        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))

    def init(self):
        # self.clock = pygame.time.Clock()
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("404 Error, No Joys Found")
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(joystick_handler(i))


def axis_event(event):
    global forward, reverse, reverse_index
    if event.axis == 0 and event.value >= 1:
        forward = True
        reverse = False
        reverse_index = True
        load_forward_sprites()
    if event.axis == 0 and event.value < 1:
        forward = False
        reverse = False
    if event.axis == 0 and event.value <= -1:
        reverse = True
        forward = False
        if reverse_index:
            flip_sprites_left()
            reverse_index = False


def hat_event(event):
    global forward, reverse, reverse_index
    if event.hat == 0 and event.value == (1, 0):
        forward = True
        reverse = False
        reverse_index = True
        load_forward_sprites()
    if event.hat == 0 and event.value == (0, 0):
        forward = False
        reverse = False
    if event.hat == 0 and event.value == (-1, 0):
        reverse = True
        forward = False
        if reverse_index:
            flip_sprites_left()
            reverse_index = False


class input_test(object):
    def init(self):
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("No joysticks found.")
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(joystick_handler(i))

    def run(self):
        global start_screen, last_p_y, p_vx, p_flap, freezeMario, freezeMario, die_animation, lives
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if not freezeMario and not die_animation:
                if event.type == JOYHATMOTION:
                    self.joy[event.joy].hat[event.hat] = event.value
                    hat_event(event)
                elif event.type == JOYAXISMOTION:
                    self.joy[event.joy].axis[event.axis] = event.value
                    axis_event(event)
                elif event.type == JOYBUTTONUP:
                    self.joy[event.joy].button[event.button] = 0
                elif event.type == JOYBUTTONDOWN:
                    self.joy[event.joy].button[event.button] = 1
                    if event.button == 1 and not start_screen:
                        if p_y > 0:
                            last_p_y = p_y
                            p_vx = p_flap_accuracy
                            p_flap = True
                            game_audio_sound['wing'].play()
                    if event.button == 7 and start_screen:
                        game_audio_sound['start'].play()
                        lives = 3
                        display_screen_window.blit(game_image['restart'], (0, 0))
                        display_screen_window.blit(game_image['numbers'][lives], (160, 240))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        game_audio_sound['Overworld'].play()
                        setupGamePlay()
                        start_screen = False
                    if event.button == 6:
                        pygame.quit()
                        sys.exit()

            if start_screen:
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) \
                        or event.type == MOUSEBUTTONDOWN:
                    game_audio_sound['start'].play()
                    lives = 3
                    display_screen_window.blit(game_image['restart'], (0, 0))
                    display_screen_window.blit(game_image['numbers'][lives], (160, 240))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    game_audio_sound['Overworld'].play()
                    setupGamePlay()
                    start_screen = False
            else:
                gamePlayEvents(event)
        if start_screen:
            display_screen_window.blit(game_image['start'], (0, 0))
            display_screen_window.blit(game_image['message'], (msgx, msgy))
            pygame.display.update()
            time_clock.tick(FPS)
        else:
            main_gameplay()


def gamePlayEvents(events):
    global freezeMario, last_p_y, p_vx, p_flap, forward, reverse, animateSprite, spriteInt, animatePWing, p_wing, \
        reverse_index, die_animation
    if events.type == unfreezeMario:  # user event to flip coins
        freezeMario = False
    if not freezeMario and not die_animation:
        if events.type == KEYDOWN and (events.key == K_SPACE or events.key == K_UP) \
                or events.type == MOUSEBUTTONDOWN:
            if p_y > 0:
                last_p_y = p_y
                p_vx = p_flap_accuracy
                p_flap = True
                game_audio_sound['wing'].play()
        if events.type == KEYDOWN and (events.key == K_d):
            forward = True
            reverse = False
            reverse_index = True
            load_forward_sprites()
        if events.type == KEYUP and (events.key == K_d):
            forward = False

        if events.type == KEYDOWN and (events.key == K_a):
            reverse = True
            forward = False
            if reverse_index:
                flip_sprites_left()
                reverse_index = False

    if events.type == KEYUP and (events.key == K_a):
        reverse = False

    if events.type == animateSprite:  # user event to flip coins
        spriteInt += 1
        if spriteInt > 3:
            spriteInt = 0
    if events.type == animatePWing:  # user event to animate p-wing bar
        p_wing += 1
        if p_wing > 1:
            p_wing = 0


def setupGamePlay():
    global p_x, p_y, b_x, gameLevel, score, coins, lives, last_p_y, this_p_x, last_p_x, spriteInt, crash_test, p_flap, \
        forward, reverse, pipe_walking, freezeMario, Bird3_dead, background, ran_Bird, ran_Bird2, ran_Bird3, up_pipes, \
        low_pipes, ran_coin, ran_coin2, ran_coin3, Bird1_Vx, Bird2_Vx, Bird3_Vx, pip_Vx, coin_Vx, coin2_Vx, coin3_Vx, \
        p_vx, p_mvx, p_accuracy, p_flap_accuracy, animateSprite, unfreezeMario, animatePWing, reverse_index, tiles, \
        die_animation, elapsed_time, ran_Bird4

    p_x = 50  # 0 to 262, mario xAxis starting point
    p_y = int(screen_width / 2)  # mario starting point
    b_x = 0  # base xAxis position
    gameLevel = 1
    score = 0
    coins = 0
    lives = 3
    last_p_y = p_y
    this_p_x = 0
    last_p_x = 0
    spriteInt = 0
    crash_test = False  # hit box detection
    p_flap = False
    forward = False
    reverse = False
    reverse_index = True
    pipe_walking = False
    freezeMario = False
    Bird3_dead = False
    die_animation = False
    background = 'images/Overworld.png'
    game_image['background'] = pygame.image.load(background).convert()
    tiles = math.ceil(screen_width / game_image['background'].get_width()) + 1
    load_forward_sprites()  # right facing sprites loaded first
    ran_Bird = []
    ran_Bird2 = []
    ran_Bird3 = []
    ran_Bird4 = []
    ran_coin2 = []
    ran_coin3 = []
    n_pip1 = get_Random_Pipes()
    n_pip2 = get_Random_Pipes()
    up_pipes = [
        {'x': screen_width + 200, 'y': n_pip1[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': n_pip2[0]['y']},
    ]

    low_pipes = [
        {'x': screen_width + 200, 'y': n_pip1[1]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': n_pip2[1]['y']},
    ]

    n_coin = get_Random_Coins()
    n_coin2 = get_Random_Coins()
    ran_coin = [
        {'x': screen_width + 200, 'y': n_coin[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': n_coin2[0]['y']},
    ]

    elapsed_time = 0.00
    Bird1_Vx = - 3
    Bird2_Vx = - 2
    Bird3_Vx = - 5.5
    pip_Vx = - 4  # pipe speed
    coin_Vx = - 6
    coin2_Vx = - 5
    coin3_Vx = - 4.5
    p_vx = -9
    p_mvx = 10  # mario fall speed
    p_accuracy = 1  # mario lift
    p_flap_accuracy = -8  # mario lift
    animateSprite = pygame.USEREVENT + 0  # 8 total user events
    unfreezeMario = pygame.USEREVENT + 1
    animatePWing = pygame.USEREVENT + 2  # 8 total user events
    pygame.time.set_timer(animateSprite, 100)
    pygame.time.set_timer(animatePWing, 100)


if __name__ == "__main__":
    pygame.init()
    program = input_test()
    program.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bros.')
    game_image['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )

    game_image['PWing'] = (
        pygame.image.load(PWing1).convert_alpha(),
        pygame.image.load(PWing2).convert_alpha(),
    )
    game_image['coin_img'] = (
        pygame.image.load(coin1).convert_alpha(),
        pygame.image.load(coin2).convert_alpha(),
        pygame.image.load(coin3).convert_alpha(),
        pygame.image.load(coin4).convert_alpha(),
    )
    game_image['Bird_img'] = (
        pygame.image.load(Bird1).convert_alpha(),
        pygame.image.load(Bird2).convert_alpha(),
        pygame.image.load(Bird3).convert_alpha(),
        pygame.image.load(Bird4).convert_alpha(),
    )
    game_image['Bird2_img'] = (
        pygame.image.load(Bird5).convert_alpha(),
        pygame.image.load(Bird6).convert_alpha(),
        pygame.image.load(Bird7).convert_alpha(),
        pygame.image.load(Bird8).convert_alpha(),
    )
    game_image['Bird3_img'] = (
        pygame.image.load(Bird9).convert_alpha(),
        pygame.image.load(Bird10).convert_alpha(),
        pygame.image.load(Bird11).convert_alpha(),
        pygame.image.load(Bird12).convert_alpha(),
    )

    game_image['Bird4_img'] = pygame.image.load(Bird17).convert_alpha()

    game_image['die'] = pygame.image.load(die).convert_alpha()
    game_image['start'] = pygame.image.load(start).convert_alpha()
    game_image['restart'] = pygame.image.load(restart).convert_alpha()
    game_image['gameOverScreen'] = pygame.image.load(gameOverScreen).convert_alpha()
    game_image['message'] = pygame.image.load('images/message.png').convert_alpha()
    pipe_image = 'images/pipe.png'
    game_image['pipeFlip'] = pygame.transform.flip(pygame.image.load(pipe_image).convert_alpha(), True, False)
    game_image['pipe'] = (pygame.transform.rotate(game_image['pipeFlip'], 180),
                          pygame.image.load(pipe_image).convert_alpha()
                          )
    # Game sounds
    game_audio_sound['die'] = pygame.mixer.Sound('sounds/die.wav')
    game_audio_sound['coin'] = pygame.mixer.Sound('sounds/coin.mp3')
    game_audio_sound['coin'].set_volume(0.4)
    game_audio_sound['1UP'] = pygame.mixer.Sound('sounds/1UP.mp3')
    game_audio_sound['kill'] = pygame.mixer.Sound('sounds/kill.mp3')
    game_audio_sound['wing'] = pygame.mixer.Sound('sounds/wing.mp3')
    game_audio_sound['wing'].set_volume(0.3)
    game_audio_sound['start'] = pygame.mixer.Sound('sounds/start.mp3')
    game_audio_sound['Overworld'] = pygame.mixer.Sound('sounds/music/Overworld.mp3')
    game_audio_sound['Underground'] = pygame.mixer.Sound('sounds/music/Underground.mp3')
    game_audio_sound['Athletic'] = pygame.mixer.Sound('sounds/music/Athletic.mp3')
    game_audio_sound['desert'] = pygame.mixer.Sound('sounds/music/desert.mp3')
    game_audio_sound['PipeMaze'] = pygame.mixer.Sound('sounds/music/PipeMaze.mp3')
    game_audio_sound['Music Box'] = pygame.mixer.Sound('sounds/music/Music Box.mp3')
    game_audio_sound['Airship'] = pygame.mixer.Sound('sounds/music/Airship.mp3')
    game_audio_sound['Castle'] = pygame.mixer.Sound('sounds/music/Castle.mp3')

    game_image['base'] = pygame.image.load(base).convert_alpha()
    load_forward_sprites()
    msgx = int((screen_width - game_image['message'].get_width()) / 2)
    msgy = int(scr_height * 0.13)
    while True:
        program.run()

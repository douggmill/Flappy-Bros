import random  # For generating random numbers
import pygame
import sys
from pygame.locals import *

# Global Variables for the game
FPS = 32
screen_width = 289
scr_height = 511
display_screen_window = pygame.display.set_mode((screen_width, scr_height))
play_ground = scr_height * 0.8
game_image = {}
game_audio_sound = {}
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
gameLevel = 1
p_x = 0
p_y = 0
b_x = 0
score = 0
coins = 0
lives = 1
last_p_y = p_y
this_p_x = 0
last_p_x = 0
spriteInt = 0
p_wing = 0
gameOver = False
crash_test = False  # hit box detection
Bird3_dead = False
start_screen = True


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


def main_gameplay():
    global gameOver, crash_test, start_screen, p_flap, p_y, Bird3_dead, p_vx, p_mvx, p_accuracy

    if p_vx < p_mvx and not p_flap:
        p_vx += p_accuracy

    p_height = game_image['TailUp'].get_height()
    p_y = p_y + min(p_vx, play_ground - p_y - p_height)

    for pip_upper, pip_lower in zip(up_pipes, low_pipes):  # set different lower and upper pipe speeds
        pip_upper['x'] += pip_Vx
        pip_lower['x'] += pip_Vx
    for coin_random in ran_coin:  # set different lower and upper pipe speeds
        coin_random['x'] += coin_Vx

    if ran_Bird2:
        if 0 <= ran_Bird2[0]['x'] < 3 and gameLevel == 2:
            new_Bird2 = get_Random_Bird2()
            ran_Bird2.append(new_Bird2[0])
        for Bird2_random in ran_Bird2:
            Bird2_random['x'] += Bird2_Vx
        if ran_Bird2[0]['x'] < -game_image['Bird2_img'][0].get_width():
            ran_Bird2.pop(0)

    if ran_Bird3:
        if 0 < ran_Bird3[0]['x'] < 4 and gameLevel == 3:
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
        if 0 <= ran_Bird[0]['x'] < 3 and gameLevel == 4:
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

    display_screen_window.blit(game_image['background'], (0, 0))
    random_Stuff(up_pipes, low_pipes, ran_coin, ran_Bird, ran_Bird2, ran_Bird3)
    display_screen_window.blit(game_image['base'], (b_x, play_ground))

    if crash_test:
        game_audio_sound['Overworld'].stop()
        game_audio_sound['Underground'].stop()
        game_audio_sound['PipeMaze'].stop()
        game_audio_sound['desert'].stop()
        game_audio_sound['Hammerbros'].stop()
        game_audio_sound['Athletic'].stop()
        game_audio_sound['Castle'].stop()
        game_audio_sound['Airship'].stop()
        gameOver = True
        game_over(up_pipes, low_pipes, ran_coin, ran_Bird, ran_Bird2, ran_Bird3)

    else:
        sprite_animations()
        crash_test = is_Colliding(up_pipes, low_pipes, ran_coin, ran_Bird, ran_Bird2, ran_Bird3)
        check_Points()

    if gameOver and crash_test:  # breaks loop and goes to main menu
        start_screen = True

    d = [int(x) for x in list(str(score))]
    w = 0
    for digit in d:
        w += game_image['numbers'][digit].get_width()
    Xoffset = (screen_width - w) / 1.08  # x axis numbers
    for digit in d:
        display_screen_window.blit(game_image['numbers'][digit], (Xoffset, scr_height * 0.918))  # y axis numbers
        Xoffset += game_image['numbers'][digit].get_width()

    e = [int(x) for x in list(str(coins))]
    f = 0
    for digit in e:
        f += game_image['numbers'][digit].get_width()
    Xoffset = (screen_width - f) / 1.08  # x axis numbers
    for digit in e:
        display_screen_window.blit(game_image['numbers'][digit], (Xoffset, scr_height * 0.89))  # y axis numbers
        Xoffset += game_image['numbers'][digit].get_width()

    display_screen_window.blit(game_image['numbers'][gameLevel], (75, 456))  # world number
    display_screen_window.blit(game_image['numbers'][lives], (65, 469))  # lives

    if p_flap:
        p_flap = False
    pygame.display.update()
    time_clock.tick(FPS)


def random_Stuff(upper_pipes, lower_pipes, random_coin, random_Bird, random_Bird2, random_Bird3):
    for pip_upper, pip_lower in zip(upper_pipes, lower_pipes):  # Display pipe new locations
        display_screen_window.blit(game_image['pipe'][0], (pip_upper['x'], pip_upper['y']))
        display_screen_window.blit(game_image['pipe'][1], (pip_lower['x'], pip_lower['y']))

    for coin_random in random_coin:  # Display coin new locations
        display_screen_window.blit(game_image['coin_img'][spriteInt], (coin_random['x'], coin_random['y']))

    for Bird_random in random_Bird:  # Display Bird new locations
        display_screen_window.blit(game_image['Bird_img'][spriteInt], (Bird_random['x'], Bird_random['y']))

    for Bird2_random in random_Bird2:  # Display Bird2 new locations
        display_screen_window.blit(game_image['Bird2_img'][spriteInt], (Bird2_random['x'], Bird2_random['y']))

    for Bird3_random in random_Bird3:  # Display Bird new locations
        display_screen_window.blit(game_image['Bird3_img'][spriteInt], (Bird3_random['x'], Bird3_random['y']))


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
            display_screen_window.blit(game_image['PWing'][p_wing], (100, 455))
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
                display_screen_window.blit(game_image['PWing'][p_wing], (100, 455))
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


def game_over(upper_pipes, lower_pipes, random_coin, random_Bird, random_Bird2, random_Bird3):
    global p_x, p_y, b_x, play_ground
    game_audio_sound['die'].play()
    for i in range(0, 10):
        p_y += -4
        display_screen_window.blit(game_image['background'], (0, 0))
        random_Stuff(upper_pipes, lower_pipes, random_coin, random_Bird, random_Bird2, random_Bird3)
        display_screen_window.blit(game_image['base'], (b_x, play_ground))
        display_screen_window.blit(game_image['die'], (p_x, p_y))
        pygame.display.update()
        time_clock.tick(FPS)
    while pygame.mixer.get_busy():
        # p_vx = p_flap_accuracy
        # if p_vx < p_mvx:
        #     p_vx += p_accuracy
        p_y += 8
        display_screen_window.blit(game_image['background'], (0, 0))
        random_Stuff(upper_pipes, lower_pipes, random_coin, random_Bird, random_Bird2, random_Bird3)
        display_screen_window.blit(game_image['base'], (b_x, play_ground))
        display_screen_window.blit(game_image['die'], (p_x, p_y))
        pygame.display.update()
        time_clock.tick(FPS)


def check_Points():
    global background, score, gameLevel
    if score == 50 and gameLevel < 2:
        gameLevel += 1
        game_audio_sound['Overworld'].stop()
        game_audio_sound['Underground'].play()
        background = 'images/underground.png'
        game_image['background'] = pygame.image.load(background).convert()
        Level_Stats = 'images/undergroundBase.png'
        game_image['base'] = pygame.image.load(Level_Stats).convert()
        start_Bird2()
    if score == 100 and gameLevel < 3:
        gameLevel += 1
        game_audio_sound['Underground'].stop()
        game_audio_sound['PipeMaze'].play()
        background = 'images/pipeMaze.png'
        game_image['background'] = pygame.image.load(background).convert()
        Level_Stats = 'images/pipeBase.png'
        game_image['base'] = pygame.image.load(Level_Stats).convert()
        start_Bird3()
    if score == 150 and gameLevel < 4:
        gameLevel += 1
        game_audio_sound['PipeMaze'].stop()
        game_audio_sound['desert'].play()
        background = 'images/desert.png'
        game_image['background'] = pygame.image.load(background).convert()
        Level_Stats = 'images/desertBase.png'
        game_image['base'] = pygame.image.load(Level_Stats).convert()
        start_Bird1()
    if score == 200 and gameLevel < 5:
        gameLevel += 1
        game_audio_sound['desert'].stop()
        game_audio_sound['Hammerbros'].play()
        background = 'images/hammerBros.png'
        game_image['background'] = pygame.image.load(background).convert()
        Level_Stats = 'images/startBase.png'
        game_image['base'] = pygame.image.load(Level_Stats).convert()
    if score == 250 and gameLevel < 6:
        gameLevel += 1
        game_audio_sound['Hammerbros'].stop()
        game_audio_sound['Athletic'].play()
    if score == 350 and gameLevel < 7:
        gameLevel += 1
        game_audio_sound['Athletic'].stop()
        game_audio_sound['Airship'].play()
    if score == 400 and gameLevel < 8:
        gameLevel += 1
        game_audio_sound['Airship'].stop()
        game_audio_sound['Castle'].play()


def is_Colliding(upper_pipes, lower_pipes, random_coin, random_Bird, random_Bird2, random_Bird3):
    global p_x, p_y, p_flap, forward, pipe_walking, score, coin_h, Bird_h, Bird2_h, Bird3_h, freezeMario, \
        unfreezeMario, last_p_y, p_vx, p_flap_accuracy, coins, lives, Bird3_dead

    if p_y > play_ground - 25 or p_y < 0:  # out of bounds
        return True
    elif p_x == 0:
        return True

    for Bird in random_Bird:  # bird hit box
        Bird_h = game_image['Bird_img'][0].get_height() - 1
        Bird_w = game_image['Bird_img'][0].get_width() * 0.45 - 1
        if abs(p_y - Bird['y']) < Bird_w and abs(p_x - Bird['x']) < Bird_w:
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
            if lives > 3:
                lives = 4

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
    # Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    #  set minimum coin height
    yesCoin = random.randrange(20, 370)
    coinX = screen_width
    coin = [
        {'x': coinX, 'y': yesCoin},  # coin
    ]
    return coin


def get_Random_Bird():
    global spriteInt
    # Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    #  set minimum Bird height
    yesBird = random.randrange(20, 370)
    BirdX = screen_width
    Bird = [
        {'x': BirdX, 'y': yesBird}
    ]
    return Bird


def get_Random_Bird2():
    global spriteInt
    # Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    #  set minimum Bird2 height
    yesBird2 = random.randrange(20, 370)
    Bird2X = screen_width
    Bird_2 = [
        {'x': Bird2X, 'y': yesBird2}
    ]
    return Bird_2


def get_Random_Bird3():
    global spriteInt
    # Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    #  set minimum Bird3 height
    yesBird3 = random.randrange(20, 370)
    Bird3X = screen_width
    Bird_3 = [
        {'x': Bird3X, 'y': yesBird3}
    ]
    return Bird_3


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


class input_test(object):
    def init(self):
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("No joysticks found.")
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(joystick_handler(i))

    def run(self):
        global start_screen, last_p_y, p_vx, p_flap, freezeMario, forward, reverse, reverse_index
        for event in pygame.event.get():
            if event.type == JOYHATMOTION:
                self.joy[event.joy].hat[event.hat] = event.value
                print(event.hat, event.value)
            elif event.type == JOYAXISMOTION:
                self.joy[event.joy].axis[event.axis] = event.value
                if not start_screen:
                    if not freezeMario:
                        if event.axis == 0 and (event.value >= 1):
                            forward = True
                            reverse = False
                            reverse_index = True
                            load_forward_sprites()
                        if event.axis == 0 and (event.value < 1):
                            forward = False
                            reverse = False
                        if event.axis == 0 and (event.value <= -1):
                            reverse = True
                            forward = False
                            if reverse_index:
                                flip_sprites_left()
                                reverse_index = False

            elif event.type == JOYBUTTONUP:
                self.joy[event.joy].button[event.button] = 0
            elif event.type == JOYBUTTONDOWN:
                self.joy[event.joy].button[event.button] = 1
                if event.button == 1:
                    if p_y > 0:
                        last_p_y = p_y
                        p_vx = p_flap_accuracy
                        p_flap = True
                        game_audio_sound['wing'].play()
                if event.button == 9:
                    if start_screen:
                        game_audio_sound['start'].play()
                        pygame.time.delay(2000)
                        game_audio_sound['Overworld'].play()
                        setupGamePlay()
                        start_screen = False
                if event.button == 8:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if start_screen:
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) \
                        or event.type == MOUSEBUTTONDOWN:
                    game_audio_sound['start'].play()
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


def gamePlayEvents(event):
    global freezeMario, last_p_y, p_vx, p_flap, forward, reverse, animateSprite, spriteInt, animatePWing, p_wing, \
        reverse_index
    if event.type == unfreezeMario:  # user event to flip coins
        freezeMario = False
    if not freezeMario:
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) \
                or event.type == MOUSEBUTTONDOWN:
            if p_y > 0:
                last_p_y = p_y
                p_vx = p_flap_accuracy
                p_flap = True
                game_audio_sound['wing'].play()
        if event.type == KEYDOWN and (event.key == K_d):
            forward = True
            reverse = False
            reverse_index = True
            load_forward_sprites()
        if event.type == KEYUP and (event.key == K_d):
            forward = False

        if event.type == KEYDOWN and (event.key == K_a):
            reverse = True
            forward = False
            if reverse_index:
                flip_sprites_left()
                reverse_index = False

    if event.type == KEYUP and (event.key == K_a):
        reverse = False

    if event.type == animateSprite:  # user event to flip coins
        spriteInt += 1
        if spriteInt > 3:
            spriteInt = 0
    if event.type == animatePWing:  # user event to flip coins
        p_wing += 1
        if p_wing > 1:
            p_wing = 0


def setupGamePlay():
    global p_x, p_y, b_x, gameLevel, score, coins, lives, last_p_y, this_p_x, last_p_x, spriteInt, gameOver, \
        crash_test, p_flap, forward, reverse, pipe_walking, freezeMario, Bird3_dead, background, ran_Bird, ran_Bird2, \
        ran_Bird3, up_pipes, low_pipes, ran_coin, Bird1_Vx, Bird2_Vx, Bird3_Vx, pip_Vx, coin_Vx, p_vx, p_mvx, \
        p_accuracy, p_flap_accuracy, animateSprite, unfreezeMario, animatePWing, reverse_index

    p_x = 50  # 0 to 262, mario xAxis starting point
    p_y = int(screen_width / 2)  # mario starting point
    b_x = 0  # base xAxis position
    gameLevel = 1
    score = 0
    coins = 0
    lives = 1
    last_p_y = p_y
    this_p_x = 0
    last_p_x = 0
    spriteInt = 0
    gameOver = False
    crash_test = False  # hit box detection
    p_flap = False
    forward = False
    reverse = False
    reverse_index = False
    pipe_walking = False
    freezeMario = False
    Bird3_dead = False
    background = 'images/overworld.png'
    game_image['background'] = pygame.image.load(background).convert()
    load_forward_sprites()  # right facing sprites loaded first
    ran_Bird = []
    ran_Bird2 = []
    ran_Bird3 = []
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

    Bird1_Vx = - 3
    Bird2_Vx = - 2
    Bird3_Vx = - 5.5
    pip_Vx = - 4  # pipe speed
    coin_Vx = - 6
    p_vx = -9
    p_mvx = 10  # mario fall speed
    p_accuracy = 1  # mario lift
    p_flap_accuracy = -8  # mario lift
    animateSprite = pygame.USEREVENT + 0  # 8 total user events
    unfreezeMario = pygame.USEREVENT + 1
    animatePWing = pygame.USEREVENT + 2  # 8 total user events
    pygame.time.set_timer(animateSprite, 100)
    pygame.time.set_timer(animatePWing, 100)
    game_image['base'] = pygame.image.load(base).convert()


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
    game_image['die'] = pygame.image.load(die).convert_alpha()
    game_image['start'] = pygame.image.load(start).convert_alpha()
    game_image['message'] = pygame.image.load('images/message.png').convert_alpha()
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
    game_audio_sound['PipeMaze'] = pygame.mixer.Sound('sounds/music/PipeMaze.mp3')
    game_audio_sound['desert'] = pygame.mixer.Sound('sounds/music/desert.mp3')
    game_audio_sound['Hammerbros'] = pygame.mixer.Sound('sounds/music/Hammer Bros..mp3')
    game_audio_sound['Athletic'] = pygame.mixer.Sound('sounds/music/Athletic.mp3')
    game_audio_sound['Castle'] = pygame.mixer.Sound('sounds/music/Castle.mp3')
    game_audio_sound['Airship'] = pygame.mixer.Sound('sounds/music/Airship.mp3')
    base = 'images/startBase.png'
    game_image['base'] = pygame.image.load(base).convert()
    load_forward_sprites()
    msgx = int((screen_width - game_image['message'].get_width()) / 2)
    msgy = int(scr_height * 0.13)
    while True:
        program.run()

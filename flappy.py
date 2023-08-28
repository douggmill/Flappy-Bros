import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports

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
RunMiddle = 'images/mario_run.png'
RunStart = 'images/mario_startRun.png'
RunEnd = 'images/mario_runEnd.png'
Still = 'images/mario_still.png'
die = 'images/mario_die.png'
start = 'images/start.png'
pipe_image = 'images/pipe.png'
coin1 = 'images/coin1.png'
coin2 = 'images/coin2.png'
coin3 = 'images/coin3.png'


def welcome_main_screen():
    global p_x, p_y, b_x
    # Shows welcome images on the screen
    p_x = int(screen_width / 5)
    p_y = int((scr_height - game_image['TailUp'].get_height()) / 2)
    msgx = int((screen_width - game_image['message'].get_width()) / 2)
    msgy = int(scr_height * 0.13)
    b_x = 0
    while True:
        for button_event in pygame.event.get():
            # if user clicks on cross button, close the game
            if button_event.type == QUIT or (button_event.type == KEYDOWN and button_event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif button_event.type == KEYDOWN and (button_event.key == K_SPACE or button_event.key == K_UP) or button_event.type == MOUSEBUTTONDOWN:
                game_audio_sound['start'].play()
                pygame.time.delay(2000)
                game_audio_sound['Overworld'].play()
                return
            else:
                display_screen_window.blit(game_image['start'], (0, 0))
                display_screen_window.blit(game_image['message'], (msgx, msgy))
                pygame.display.update()
                time_clock.tick(FPS)


def load_forward_sprites():
    game_image['TailUp'] = pygame.image.load(TailUp).convert_alpha()
    game_image['TailDown'] = pygame.image.load(TailDown).convert_alpha()
    game_image['TailMiddle'] = pygame.image.load(TailMiddle).convert_alpha()
    game_image['RunMiddle'] = pygame.image.load(RunMiddle).convert_alpha()
    game_image['RunStart'] = pygame.image.load(RunStart).convert_alpha()
    game_image['RunEnd'] = pygame.image.load(RunEnd).convert_alpha()
    game_image['Still'] = pygame.image.load(Still).convert_alpha()


def flip_sprites_left():
    game_image['TailUp'] = pygame.transform.flip(game_image['TailUp'], True, False)
    game_image['TailDown'] = pygame.transform.flip(game_image['TailDown'], True, False)
    game_image['TailMiddle'] = pygame.transform.flip(game_image['TailMiddle'], True, False)
    game_image['RunMiddle'] = pygame.transform.flip(game_image['RunMiddle'], True, False)
    game_image['RunStart'] = pygame.transform.flip(game_image['RunStart'], True, False)
    game_image['RunEnd'] = pygame.transform.flip(game_image['RunEnd'], True, False)
    game_image['Still'] = pygame.transform.flip(game_image['Still'], True, False)

def main_gameplay():
    global last_p_y, gameOver, crash_test, p_x, p_y, this_p_x, last_p_x, forward, reverse, reverse_index, \
        coinInt, event, p_flap, pipe_walking, score, b_x, background

    load_forward_sprites()  # right facing sprites loaded first
    gameOver = False
    crash_test = False  # hit box detection
    score = 0
    p_x = 50  # 0 to 262, mario xAxis starting point
    p_y = int(screen_width / 2)  # mario starting point
    last_p_y = p_y
    this_p_x = 0
    last_p_x = 0
    b_x = 0  # base xAxis position
    coinInt = 0
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

    pip_Vx = - 4  # pipe speed
    coin_Vx = - 6

    p_vx = -9
    p_mvx = 10  # mario fall speed
    # p_mvy = -8
    p_accuracy = 1  # mario lift

    p_flap_accuracy = -8  # mario lift
    p_flap = False
    forward = False
    reverse = False
    reverse_index = True
    pipe_walking = False
    flipCoin = pygame.USEREVENT + 0
    pygame.time.set_timer(flipCoin, 100)
    background = 'images/overworld.png'
    game_image['background'] = pygame.image.load(background).convert()
    # base = 'images/startBase.png'
    game_image['base'] = pygame.image.load(base).convert()

    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
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

            if event.type == flipCoin:  # user event to flip coins
                coinInt += 1
                if coinInt > 3:
                    coinInt = 0

        if gameOver and crash_test:  # breaks loop and goes to main menu
            return

        if p_vx < p_mvx and not p_flap:
            p_vx += p_accuracy

        p_height = game_image['TailUp'].get_height()
        p_y = p_y + min(p_vx, play_ground - p_y - p_height)

        for pip_upper, pip_lower in zip(up_pipes, low_pipes):  # set different lower and upper pipe speeds
            pip_upper['x'] += pip_Vx
            pip_lower['x'] += pip_Vx

        for coin_random in ran_coin:  # set different lower and upper pipe speeds
            coin_random['x'] += coin_Vx

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
        for pip_upper, pip_lower in zip(up_pipes, low_pipes):  # Display pipe new locations
            display_screen_window.blit(game_image['pipe'][0], (pip_upper['x'], pip_upper['y']))
            display_screen_window.blit(game_image['pipe'][1], (pip_lower['x'], pip_lower['y']))
        for coin_random in ran_coin:  # Display coin new locations
            display_screen_window.blit(game_image['coin_img'][coinInt], (coin_random['x'], coin_random['y']))
        display_screen_window.blit(game_image['base'], (b_x, play_ground))

        if not crash_test:
            sprite_animations()
            crash_test = is_Colliding(up_pipes, low_pipes, ran_coin)
        else:
            game_audio_sound['Overworld'].stop()
            game_audio_sound['Underground'].stop()
            game_audio_sound['PipeMaze'].stop()
            game_audio_sound['desert'].stop()
            game_audio_sound['Hammerbros'].stop()
            game_audio_sound['Athletic'].stop()
            game_audio_sound['Castle'].stop()
            game_audio_sound['Airship'].stop()
            gameOver = True
            game_over()

        d = [int(x) for x in list(str(score))]
        w = 0
        for digit in d:
            w += game_image['numbers'][digit].get_width()
        Xoffset = (screen_width - w) / 1.08  # x axis numbers

        for digit in d:
            display_screen_window.blit(game_image['numbers'][digit], (Xoffset, scr_height * 0.918))  # y axis numbers
            Xoffset += game_image['numbers'][digit].get_width()
        if p_flap:
            p_flap = False
        pygame.display.update()
        time_clock.tick(FPS)


def sprite_animations():
    global p_x, p_y, this_p_x, last_p_x, forward, reverse, pipe_walking
    if 0 <= p_x <= 262:
        if forward:
            p_x += 3
        if reverse:
            p_x -= 4
    if p_x < 0:
        p_x = 0
    if p_x > 262:
        p_x = 262

    if p_y <= 381 and not pipe_walking:
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


def game_over():
    global p_x, p_y, b_x, play_ground
    game_audio_sound['hit'].play()
    for i in range(0, 10):
        p_y += -4
        display_screen_window.blit(game_image['background'], (0, 0))
        display_screen_window.blit(game_image['die'], (p_x, p_y))
        display_screen_window.blit(game_image['base'], (b_x, play_ground))
        pygame.display.update()
        time_clock.tick(FPS)
    while pygame.mixer.get_busy():
        # p_vx = p_flap_accuracy
        # if p_vx < p_mvx:
        #     p_vx += p_accuracy
        p_y += 8
        display_screen_window.blit(game_image['background'], (0, 0))
        display_screen_window.blit(game_image['die'], (p_x, p_y))
        display_screen_window.blit(game_image['base'], (b_x, play_ground))
        pygame.display.update()
        time_clock.tick(FPS)


def is_Colliding(up_pipes, low_pipes, ran_coin):
    global p_x, p_y, p_flap, forward, pipe_walking, score, coin_h, background
    # out of bounds
    if p_y > play_ground - 25 or p_y < 0:
        return True
    elif p_x == 0:
        return True

    # coin hit box
    for coin in ran_coin:
        coin_h = game_image['coin_img'][0].get_height()
        coin_w = game_image['coin_img'][0].get_width() * 1.5

        if abs(p_y - coin['y']) < coin_w and abs(p_x - coin['x']) < coin_w:
            score += 1
            game_audio_sound['coin'].play()
            a = ran_coin.index(coin)
            ran_coin[a] = {'x': 0, 'y': 0}  # move coin off-screen if collected
            if score == 10:
                game_audio_sound['Overworld'].stop()
                game_audio_sound['Underground'].play()
                background = 'images/underground.png'
                game_image['background'] = pygame.image.load(background).convert()
                Level_Stats = 'images/undergroundBase.png'
                game_image['base'] = pygame.image.load(Level_Stats).convert()
            if score == 20:
                game_audio_sound['Underground'].stop()
                game_audio_sound['PipeMaze'].play()
                background = 'images/pipeMaze.png'
                game_image['background'] = pygame.image.load(background).convert()
                Level_Stats = 'images/pipeBase.png'
                game_image['base'] = pygame.image.load(Level_Stats).convert()
            if score == 30:
                game_audio_sound['PipeMaze'].stop()
                game_audio_sound['desert'].play()
                background = 'images/desert.png'
                game_image['background'] = pygame.image.load(background).convert()
                Level_Stats = 'images/desertBase.png'
                game_image['base'] = pygame.image.load(Level_Stats).convert()
            if score == 40:
                game_audio_sound['desert'].stop()
                game_audio_sound['Hammerbros'].play()
            if score == 50:
                game_audio_sound['Hammerbros'].stop()
                game_audio_sound['Athletic'].play()
            if score == 60:
                game_audio_sound['Athletic'].stop()
                game_audio_sound['Airship'].play()
            if score == 70:
                game_audio_sound['Airship'].stop()
                game_audio_sound['Castle'].play()

    # upper pipe hit box
    for pipe in up_pipes:
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
    for pipe in low_pipes:
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
    global coinInt
    # Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    #  set minimum coin height
    yesCoin = random.randrange(20, 370)
    coinX = screen_width
    coin = [
        {'x': coinX, 'y': yesCoin},  # coin
    ]
    return coin


if __name__ == "__main__":

    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
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

    game_image['coin_img'] = (
        pygame.image.load('images/coin1.png').convert_alpha(),
        pygame.image.load('images/coin2.png').convert_alpha(),
        pygame.image.load('images/coin3.png').convert_alpha(),
        pygame.image.load('images/coin4.png').convert_alpha(),
    )

    game_image['die'] = pygame.image.load(die).convert_alpha()
    game_image['start'] = pygame.image.load(start).convert_alpha()
    game_image['message'] = pygame.image.load('images/message.png').convert_alpha()
    game_image['pipeFlip'] = pygame.transform.flip(pygame.image.load(pipe_image).convert_alpha(), True, False)
    game_image['pipe'] = (pygame.transform.rotate(game_image['pipeFlip'], 180),
                          pygame.image.load(pipe_image).convert_alpha()
                          )
    #
    # Game sounds
    game_audio_sound['die'] = pygame.mixer.Sound('sounds/die.wav')
    game_audio_sound['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    game_audio_sound['coin'] = pygame.mixer.Sound('sounds/coin.mp3')
    game_audio_sound['coin'].set_volume(0.4)
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
    while True:
        welcome_main_screen()  # Shows welcome screen to the user until he presses a button
        main_gameplay()  # This is the main game function

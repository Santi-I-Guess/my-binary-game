from curses import wrapper
import curses
from random import randint

from aux_functions import big_num_layer, little_num_layer, box_layers, bit_updater

def big_num_printing(challenge: int, y_offset: int, x_offset: int, screen) -> None:
    for layer in range(7): # shadow & background
        screen.addstr(layer+y_offset+1, x_offset, \
            " "*18, curses.color_pair(3))
        screen.addstr(layer+y_offset, x_offset-1, \
            " "*18, curses.color_pair(5)) 
    # basically, print red background whereever there's a #
    for layer in range(5):
        curr_layer: str = big_num_layer(challenge, layer)
        for idx, letter in enumerate(curr_layer):
            if letter != '#': continue
            screen.addch(layer+y_offset+1, x_offset+idx+1, \
                '#', curses.color_pair(4))

def little_num_printing(curr_guess: list[int], y_offset: int, x_offset: int, screen) -> None:
    length: int = 35
    for layer in range(5): # background 
        if layer == 0:   curr_layer = box_layers(0, length)
        elif layer == 4: curr_layer = box_layers(2, length)
        else:            curr_layer = box_layers(1, length)
        
        screen.addstr(y_offset+layer-1, x_offset-2, \
            curr_layer, curses.color_pair(6))

    for layer in range(3):
        curr_layer: str = little_num_layer(curr_guess, layer)
        for idx, letter in enumerate(curr_layer):
            if letter != '#':
                continue
            using_idx = idx if idx < 15 else idx + 2
            screen.addch(y_offset+layer, (x_offset) + using_idx, letter, \
                curses.color_pair(3))

def score_printing(score: int, y_offset: int, x_offset: int, screen):
    length: int = 16
    for layer in range(7): # background
        if layer == 0:   curr_layer = box_layers(0, length)
        elif layer == 6: curr_layer = box_layers(2, length)
        else:            curr_layer = box_layers(1, length)
        screen.addstr(y_offset-1+layer, x_offset-2, curr_layer, curses.color_pair(7))

    for layer in range(5):
        curr_layer = big_num_layer(score, layer)
        for idx, letter in enumerate(curr_layer):
            if letter != '#': continue
            screen.addch(y_offset+layer,x_offset+idx, ' ', curses.color_pair(0))



def main(screen):
    curses.curs_set(0)

    curses.init_pair(1, 196, 135)   # generic blue-purple background
    curses.init_pair(2, 196, 15)    # red on white for text background
    curses.init_pair(3, 0, 0)       # black shadow & little_num text
    curses.init_pair(4, 196, 196)   # pure red for big_num
    curses.init_pair(5, 196, 223)   # beige-y background for big_num
    curses.init_pair(6, 0, 15)      # white on black for boxed background
    
    curses.init_color(255, 400, 631, 509) # green
    curses.init_color(254, 376, 286, 352) # eggshell

    curses.init_pair(7, 255, 254)      # eggplant on green for score

    screen.bkgd(' ', curses.color_pair(1))

    score: int = 0
    
    # challenge loop
    while True:
        screen.clear()
        challenge: int = randint(1, 255)
        score_printing(score, 2, 4, screen)

        # print big num
        max_y, max_x = screen.getmaxyx()
        big_num_printing(challenge, (max_y-5)//6, (max_x-16)//2, screen)

        # input loop
        given: int = 0
        curr_guess: list[int] = [0 for i in range(8)]
        while given != ord('q'):
            little_num_printing(curr_guess, max_y//2, (max_x-34)//2, screen)
            screen.refresh()
            if given == ord('*'):
                break
            given: int = screen.getch()
            curr_guess = bit_updater(curr_guess, given)
            if int("".join(str(i) for i in curr_guess), 2) == challenge:
                score += 1
                break
        if given == ord('q'):
            break



wrapper(main)

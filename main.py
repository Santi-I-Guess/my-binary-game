from curses import wrapper
import curses
from random import randint

from aux_functions import big_num_layer, little_num_layer, box_layers, bit_updater

def big_num_printing(challenge: int, y_offset: int, x_offset: int, screen) -> None:
    for back_layer in range(7): # shadow & background
        settings = lambda i,j, k: (back_layer+i, j, " "*18, curses.color_pair(k))
        screen.addstr(*settings(y_offset+1, x_offset, 3))
        screen.addstr(*settings(y_offset, x_offset-1, 5))

    for fore_layer in range(5): # red background where text
        curr_layer: str = big_num_layer(challenge, fore_layer)
        indices = [idx for idx, i in enumerate(curr_layer) if i == '#']
        for idx in indices:
            settings = (fore_layer+y_offset+1, x_offset+idx+1)
            screen.addch(*settings, '#', curses.color_pair(4))

def little_num_printing(curr_guess: list[int], y_offset: int, x_offset: int, screen) -> None:
    length: int = 35
    for back_layer in range(5): # background         
        if back_layer == 0:   curr_layer = box_layers(0, length)
        elif back_layer == 4: curr_layer = box_layers(2, length)
        else:            curr_layer = box_layers(1, length)
        
        location = (y_offset+back_layer-1, x_offset-2) 
        screen.addstr(*location, curr_layer, curses.color_pair(6))

    for fore_layer in range(3):
        curr_layer: str = little_num_layer(curr_guess, fore_layer)
        indices = [idx for idx, i in enumerate(curr_layer) if i == '#']
        for idx in indices:
            if idx >= 15: idx += 2
            settings = (y_offset+fore_layer, x_offset+idx)
            screen.addch(*settings, '#', curses.color_pair(3))

def score_printing(score: int, y_offset: int, x_offset: int, screen):
    length: int = 16
    for back_layer in range(7): # background
        if back_layer == 0:   curr_layer = box_layers(0, length)
        elif back_layer == 6: curr_layer = box_layers(2, length)
        else:            curr_layer = box_layers(1, length)
        location = (y_offset+back_layer-1, x_offset-2)
        screen.addstr(*location, curr_layer, curses.color_pair(7))

    for fore_layer in range(5):
        curr_layer = big_num_layer(score, fore_layer)
        for idx, letter in enumerate(curr_layer):
            if letter != '#': continue
            screen.addch(y_offset+fore_layer,x_offset+idx, ' ', curses.color_pair(0))



def main(screen):
    curses.curs_set(0)

    curses.init_pair(1, 196, 135)   # generic blue-purple background
    curses.init_pair(2, 196, 15)    # red on white for text background
    curses.init_pair(3, 0, 0)       # black shadow & little_num text
    curses.init_pair(4, 196, 196)   # pure red for big_num
    curses.init_pair(5, 196, 223)   # beige-y background for big_num
    curses.init_pair(6, 0, 15)      # white on black for boxed background 

    curses.init_color(7, 376, 286, 352) # eggshell
    curses.init_color(8, 400, 631, 509) # green

    curses.init_pair(7, 8, 7)      # eggplant on green for score

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

from curses import wrapper
import curses
from random import randint

from aux import bit_updater
from l_print import big_num_printing, little_num_printing, score_printing


def main(screen):
    curses.curs_set(0) 
    curses.init_color(7, 376, 286, 352) # eggshell
    curses.init_color(8, 400, 631, 509) # green
    curses.init_pair(1, 196, 135)   # generic blue-purple background
    curses.init_pair(2, 196, 15)    # red on white for text background
    curses.init_pair(3, 0, 0)       # black shadow & little_num text
    curses.init_pair(4, 196, 196)   # pure red for big_num
    curses.init_pair(5, 196, 223)   # beige-y background for big_num
    curses.init_pair(6, 0, 15)      # white on black for boxed background 
    curses.init_pair(7, 8, 7)      # eggplant on green for score
    screen.bkgd(' ', curses.color_pair(1))

    
    # challenge loop
    score: int = 0
    while score < 256:
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
            settings = (curr_guess, max_y//2, (max_x-34)//2)
            little_num_printing(*settings, screen)
            screen.refresh()
            if given == ord('*'):
                break

            given: int = screen.getch()
            curr_guess = bit_updater(curr_guess, given)
            curr_int = "".join(str(i) for i in curr_guess)
            if int(curr_int, 2) == challenge:
                score += 1
                break

        if given == ord('q'):
            break


wrapper(main)

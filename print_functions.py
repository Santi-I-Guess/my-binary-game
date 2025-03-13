
from curses import color_pair
from aux_functions import box_layers, big_num_layer, little_num_layer

def big_num_printing(challenge: int, y_offset: int, x_offset: int, screen) -> None:
    for back_layer in range(7): # shadow & background
        settings = lambda i,j, k: (back_layer+i, j, " "*18, color_pair(k))
        screen.addstr(*settings(y_offset+1, x_offset, 3))
        screen.addstr(*settings(y_offset, x_offset-1, 5))

    for fore_layer in range(5): # red background where text
        curr_layer: str = big_num_layer(challenge, fore_layer)
        indices = [idx for idx, i in enumerate(curr_layer) if i == '#']
        for idx in indices:
            settings = (fore_layer+y_offset+1, x_offset+idx+1)
            screen.addch(*settings, '#', color_pair(4))

def little_num_printing(curr_guess: list[int], y_offset: int, x_offset: int, screen) -> None:
    length: int = 35
    for back_layer in range(5): # background         
        if back_layer == 0:   curr_layer = box_layers(0, length)
        elif back_layer == 4: curr_layer = box_layers(2, length)
        else:                 curr_layer = box_layers(1, length)
        
        location = (y_offset+back_layer-1, x_offset-2) 
        screen.addstr(*location, curr_layer, color_pair(6))

    for fore_layer in range(3):
        curr_layer: str = little_num_layer(curr_guess, fore_layer)
        indices = [idx for idx, i in enumerate(curr_layer) if i == '#']
        for idx in indices:
            if idx >= 15: idx += 2
            settings = (y_offset+fore_layer, x_offset+idx)
            screen.addch(*settings, '#', color_pair(3))

def score_printing(score: int, y_offset: int, x_offset: int, screen):
    length: int = 16
    for back_layer in range(7): # background
        if back_layer == 0:   curr_layer = box_layers(0, length)
        elif back_layer == 6: curr_layer = box_layers(2, length)
        else:                 curr_layer = box_layers(1, length)
        location = (y_offset+back_layer-1, x_offset-2)
        screen.addstr(*location, curr_layer, color_pair(7))

    for fore_layer in range(5):
        curr_layer = big_num_layer(score, fore_layer)
        for idx, letter in enumerate(curr_layer):
            if letter != '#': continue
            screen.addch(y_offset+fore_layer,x_offset+idx, ' ', color_pair(0))

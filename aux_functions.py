import math

big_nums = [
    [' ## ', '##  ', '### ', '####', '#  #', '####', ' ###', '####', '####', '####'],
    ['#  #', ' #  ', '   #', '   #', '#  #', '#   ', '#   ', '   #', '#  #', '#  #'],
    ['#  #', ' #  ', ' ## ', '  ##', '####', '### ', '####', '  # ', '####', '####'],
    ['#  #', ' #  ', '#   ', '   #', '   #', '   #', '#  #', ' #  ', '#  #', '   #'],
    [' ## ', '####', '####', '####', '   #', '### ', '####', '#   ', '####', '####']
]

little_nums = [
    ['###', '## '],
    ['# #', ' # '],
    ['###', '###']
]

def big_num_layer(number: int, layer: int) -> str:
    global big_nums
    A: int = number // 100
    B: int = (number % 100) // 10
    C: int = number % 10
    first: str = big_nums[layer][A]
    second: str = big_nums[layer][B]
    third: str = big_nums[layer][C]
    return f"{first} {second} {third}"

def little_num_layer(number: list[int], layer: int) -> str:
    global little_nums
    result = []
    for i in range(8):
        result.append(little_nums[layer][number[i]])
    return " ".join(result)

def box_layers(layer: int, length: int) -> str:
    global box_lines
    if layer == 0:   return "╔" + '═' * length + "╗"
    elif layer == 2: return "╚" + '═' * length + "╝"
    else:            return "║" + ' ' * length + "║"

def bit_updater(curr_guess: list[int], given: int) -> list[int]:
    given_chr: str = chr(given)
    if given_chr.lower() in "asdfjkl;":
        idx: int = "asdfjkl;".index(given_chr)
        curr_guess[idx] = 0 if curr_guess[idx] == 1 else 1
        return curr_guess
    elif given_chr == '!':
        return [0 if i == 1 else 1 for i in curr_guess]
    elif given_chr in '<r':
        return curr_guess[1:] + [0]
    elif given_chr in '>u':
        return [0] + curr_guess[:7]
    else:
        return curr_guess

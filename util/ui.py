from colorama import Style



def color_text(fore_color, text):
    return fore_color + str(text) + Style.RESET_ALL


def color_sign(value, positive, negative, default=''):
    if value > 0:
        return positive
    elif value < 0:
        return negative
    else:
        return default


def clear_screen():
    print('\033[2J', end='')


def clear_line(lines=1):
    for i in range(lines-1):
        print('\033[2K')
    print('\033[2K', end='')


def move_cursor(x, y):
    print('\033[{};{}f'.format(y, x), end='')

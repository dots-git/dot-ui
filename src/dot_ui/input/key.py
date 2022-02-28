import numpy as np
import pygame


class Key:
    # The corresponding pygame key id for each index
    ids = np.array(
        [
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            1073742094,
            38,
            42,
            64,
            96,
            92,
            8,
            1073741896,
            1073741881,
            94,
            1073741980,
            58,
            44,
            1073742005,
            1073742004,
            127,
            36,
            1073741905,
            1073741901,
            61,
            27,
            1073742004,
            33,
            1073741882,
            1073741891,
            1073741892,
            1073741893,
            1073741928,
            1073741929,
            1073741930,
            1073741883,
            1073741884,
            1073741885,
            1073741886,
            1073741887,
            1073741888,
            1073741889,
            1073741890,
            62,
            35,
            1073741941,
            1073741898,
            1073741897,
            1073741922,
            1073741913,
            1073741914,
            1073741915,
            1073741916,
            1073741917,
            1073741918,
            1073741919,
            1073741920,
            1073741921,
            1073741922,
            1073741913,
            1073741914,
            1073741915,
            1073741916,
            1073741917,
            1073741918,
            1073741919,
            1073741920,
            1073741921,
            1073741908,
            1073741912,
            1073741927,
            1073741910,
            1073741909,
            1073741923,
            1073741911,
            1073742050,
            1073742048,
            1073741904,
            91,
            40,
            60,
            1073742051,
            1073742051,
            1073742049,
            1073742051,
            1073741942,
            45,
            1073742081,
            1073741907,
            1073741907,
            1073741902,
            1073741899,
            1073741896,
            37,
            46,
            43,
            1073741926,
            1073741894,
            1073741894,
            63,
            39,
            34,
            1073742054,
            1073742052,
            13,
            1073742055,
            1073741903,
            93,
            41,
            1073742055,
            1073742053,
            1073742055,
            1073741895,
            1073741895,
            59,
            47,
            32,
            1073741978,
            9,
            95,
            0,
            1073741906,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            113,
            114,
            115,
            116,
            117,
            118,
            119,
            120,
            121,
            122,
        ]
    )
    
    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2
    NUMBER_3 = 3
    NUMBER_4 = 4
    NUMBER_5 = 5
    NUMBER_6 = 6
    NUMBER_7 = 7
    NUMBER_8 = 8
    NUMBER_9 = 9
    AC_BACK = 10
    AMPERSAND = 11
    ASTERISK = 12
    AT = 13
    BACKQUOTE = 14
    BACKSLASH = 15
    BACKSPACE = 16
    PAUSE = 17
    CAPSLOCK = 18
    CARET = 19
    CLEAR = 20
    COLON = 21
    COMMA = 22
    CURRENCYSUBUNIT = 23
    CURRENCYUNIT = 24
    DELETE = 25
    DOLLAR = 26
    DOWN = 27
    END = 28
    EQUALS = 29
    ESCAPE = 30
    EURO = 31
    EXCLAIM = 32
    F1 = 33
    F10 = 34
    F11 = 35
    F12 = 36
    F13 = 37
    F14 = 38
    F15 = 39
    F2 = 40
    F3 = 41
    F4 = 42
    F5 = 43
    F6 = 44
    F7 = 45
    F8 = 46
    F9 = 47
    GREATER = 48
    HASH = 49
    HELP = 50
    HOME = 51
    INSERT = 52
    NUMPAD_0 = 53
    NUMPAD_1 = 54
    NUMPAD_2 = 55
    NUMPAD_3 = 56
    NUMPAD_4 = 57
    NUMPAD_5 = 58
    NUMPAD_6 = 59
    NUMPAD_7 = 60
    NUMPAD_8 = 61
    NUMPAD_9 = 62
    KEYPAD_0 = 63
    KEYPAD_1 = 64
    KEYPAD_2 = 65
    KEYPAD_3 = 66
    KEYPAD_4 = 67
    KEYPAD_5 = 68
    KEYPAD_6 = 69
    KEYPAD_7 = 70
    KEYPAD_8 = 71
    KEYPAD_9 = 72
    KEYPAD_DIVIDE = 73
    KEYPAD_ENTER = 74
    KEYPAD_EQUALS = 75
    KEYPAD_MINUS = 76
    KEYPAD_MULTIPLY = 77
    KEYPAD_PERIOD = 78
    KEYPAD_PLUS = 79
    L_ALT = 80
    L_CTRL = 81
    LEFT = 82
    LEFTBRACKET = 83
    LEFTPAREN = 84
    LESS = 85
    L_GUI = 86
    L_META = 87
    L_SHIFT = 88
    L_SUPER = 89
    MENU = 90
    MINUS = 91
    MODE = 92
    NUMLOCK = 93
    NUMLOCKCLEAR = 94
    PAGEDOWN = 95
    PAGEUP = 96
    PAUSE = 97
    PERCENT = 98
    PERIOD = 99
    PLUS = 100
    POWER = 101
    PRINT = 102
    SCREEN = 103
    QUESTION = 104
    QUOTE = 105
    QUOTEDBL = 106
    R_ALT = 107
    R_CTRL = 108
    ENTER = 109
    R_GUI = 110
    RIGHT = 111
    RIGHTBRACKET = 112
    RIGHTPAREN = 113
    R_META = 114
    R_SHIFT = 115
    R_SUPER = 116
    SCROLLLOCK = 117
    SCROLLOCK = 118
    SEMICOLON = 119
    SLASH = 120
    SPACE = 121
    SYSREQ = 122
    TAB = 123
    UNDERSCORE = 124
    UNKNOWN = 125
    UP = 126
    A = 127
    B = 128
    C = 129
    D = 130
    E = 131
    F = 132
    G = 133
    H = 134
    I = 135
    J = 136
    K = 137
    L = 138
    M = 139
    N = 140
    O = 141
    P = 142
    Q = 143
    R = 144
    S = 145
    T = 146
    U = 147
    V = 148
    W = 149
    X = 150
    Y = 151
    Z = 152

    pressed = np.array([])
    just_pressed = pressed.copy()
    just_released = pressed.copy()

    _pressed_last_tick = pressed.copy()

    repeat = (None, None)

    _initialized = False

    @staticmethod
    def init():
        Key.pressed = np.zeros((len(Key.ids),), dtype=np.bool_)
        Key.just_pressed = Key.pressed.copy()
        Key.just_released = Key.pressed.copy()

        Key._pressed_last_tick = Key.pressed.copy()

        Key._initialized = True

        Key.set_repeat(Key.repeat[0], Key.repeat[1])

    @staticmethod
    def tick():
        Key._pressed_last_tick[:] = Key.pressed
        is_pressed = pygame.key.get_pressed()
        for i in range(len(Key.ids)):
            Key.pressed[i] = is_pressed[Key.ids[i]]
        Key.just_pressed  = np.zeros((len(Key.ids),), dtype=np.bool_)
        Key.just_released = np.zeros((len(Key.ids),), dtype=np.bool_)
    
    @staticmethod
    def events(event):
        if event.type == pygame.KEYDOWN:
            Key.just_pressed[np.where(Key.ids == event.key)[0][0]] = True
        if event.type == pygame.KEYUP:
            Key.just_released[np.where(Key.ids == event.key)[0][0]] = True

    @staticmethod
    def set_repeat(delay=None, interval=None):
        if Key._initialized:
            repeat = [pygame.key.get_repeat()[i] for i in range(2)]
            if delay is not None:
                repeat[0] = delay
            if interval is not None:
                repeat[1] = interval
            pygame.key.set_repeat(repeat[0], repeat[1])
        else:
            Key.repeat = (delay, interval)
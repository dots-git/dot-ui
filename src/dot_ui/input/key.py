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

    number_0 = 0
    number_1 = 1
    number_2 = 2
    number_3 = 3
    number_4 = 4
    number_5 = 5
    number_6 = 6
    number_7 = 7
    number_8 = 8
    number_9 = 9
    ac_back = 10
    ampersand = 11
    asterisk = 12
    at = 13
    backquote = 14
    backslash = 15
    backspace = 16
    pause = 17
    capslock = 18
    caret = 19
    clear = 20
    colon = 21
    comma = 22
    currencysubunit = 23
    currencyunit = 24
    delete = 25
    dollar = 26
    down = 27
    end = 28
    equals = 29
    escape = 30
    euro = 31
    exclaim = 32
    f1 = 33
    f10 = 34
    f11 = 35
    f12 = 36
    f13 = 37
    f14 = 38
    f15 = 39
    f2 = 40
    f3 = 41
    f4 = 42
    f5 = 43
    f6 = 44
    f7 = 45
    f8 = 46
    f9 = 47
    greater = 48
    hash = 49
    help = 50
    home = 51
    insert = 52
    numpad0 = 53
    numpad1 = 54
    numpad2 = 55
    numpad3 = 56
    numpad4 = 57
    numpad5 = 58
    numpad6 = 59
    numpad7 = 60
    numpad8 = 61
    numpad9 = 62
    numpad_0 = 63
    numpad_1 = 64
    numpad_2 = 65
    numpad_3 = 66
    numpad_4 = 67
    numpad_5 = 68
    numpad_6 = 69
    numpad_7 = 70
    numpad_8 = 71
    numpad_9 = 72
    numpad_divide = 73
    numpad_enter = 74
    numpad_equals = 75
    numpad_minus = 76
    numpad_multiply = 77
    numpad_period = 78
    numpad_plus = 79
    l_alt = 80
    l_ctrl = 81
    left = 82
    leftbracket = 83
    leftparen = 84
    less = 85
    l_gui = 86
    l_meta = 87
    l_shift = 88
    l_super = 89
    menu = 90
    minus = 91
    mode = 92
    numlock = 93
    numlockclear = 94
    pagedown = 95
    pageup = 96
    pause = 97
    percent = 98
    period = 99
    plus = 100
    power = 101
    print = 102
    screen = 103
    question = 104
    quote = 105
    quotedbl = 106
    r_alt = 107
    r_ctrl = 108
    enter = 109
    r_gui = 110
    right = 111
    rightbracket = 112
    rightparen = 113
    r_meta = 114
    r_shift = 115
    r_super = 116
    scrolllock = 117
    scrollock = 118
    semicolon = 119
    slash = 120
    space = 121
    sysreq = 122
    tab = 123
    underscore = 124
    unknown = 125
    up = 126
    a = 127
    b = 128
    c = 129
    d = 130
    e = 131
    f = 132
    g = 133
    h = 134
    i = 135
    j = 136
    k = 137
    l = 138
    m = 139
    n = 140
    o = 141
    p = 142
    q = 143
    r = 144
    s = 145
    t = 146
    u = 147
    v = 148
    w = 149
    x = 150
    y = 151
    z = 152

    pressed = np.array([])
    just_pressed = pressed.copy()
    just_released = pressed.copy()

    _pressed_last_tick = pressed.copy()

    @staticmethod
    def init():
        Key.pressed = np.array([False for _ in range(len(Key.ids))])
        Key.just_pressed = Key.pressed.copy()
        Key.just_released = Key.pressed.copy()

        Key._pressed_last_tick = Key.pressed.copy()

    @staticmethod
    def tick():
        Key._pressed_last_tick[:] = Key.pressed
        is_pressed = pygame.key.get_pressed()
        for i in range(len(Key.ids)):
            Key.pressed[i] = is_pressed[Key.ids[i]]
        Key.just_pressed = np.logical_and(
            np.logical_not(Key._pressed_last_tick), Key.pressed
        )
        Key.just_released = np.logical_and(
            Key._pressed_last_tick, np.logical_not(Key.pressed)
        )

    @staticmethod
    def set_repeat(delay=None, interval=None):
        repeat = [pygame.key.get_repeat()[i] for i in range(2)]
        if delay is not None:
            repeat[0] = delay
        if interval is not None:
            repeat[1] = interval
        pygame.key.set_repeat(repeat[0], repeat[1])

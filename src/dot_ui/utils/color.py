from typing import Iterable
import colorsys

class Color:
    WHITE: 'Color' = (255, 255, 255)
    BLACK: 'Color'  = (0,   0,   0  )
    PURE_RED: 'Color'    = (255, 0,   0  )
    PURE_GREEN: 'Color'  = (0,   255, 0  )
    PURE_BLUE: 'Color'   = (0,   0,   255)
    PURE_YELLOW: 'Color'   = (255, 255, 0  )
    PURE_MAGENTA: 'Color'  = (255, 0,   255)
    PURE_CYAN: 'Color'     = (0,   255, 255)
    RED: 'Color'     = (225, 60,  60 )
    BLUE: 'Color'    = (60,  60,  225)
    GREEN: 'Color'   = (30,  112, 30 )
    LIME: 'Color'    = (60,  225, 60 )
    YELLOW: 'Color'  = (225, 205, 60 )
    DARK_GRAY: 'Color'        = (55,  55,  55)
    LIGHT_GRAY: 'Color'       = (120, 120, 120)
    OFFWHITE: 'Color'  = (215, 215, 215)

    def __init__(self, v1: 'int | float | Iterable | str', v2: 'int | float' = None, v3: 'int | float' = None, v4: 'int | float' = None, color_format: str = 'rgb', clip_values = False):
        '''
        :attr v1: Iterable of three or four values OR hex string, optionally with leading # OR first value (then v2 and v3 are required). The meaning of each value is determined by the format
        :attr v2: Second value
        :attr v3: Third value
        :attr v4: Final value. This will always be alpha and will default to 255 | 1
        :attr color_format: The format of the values. Must start with 'rgb', 'hsv' or 'hls'. If it ends with 'f' or 'float', the values will be mapped from [0, 1] to [0, 255]
         '''
        # Check if the color format is a string, otherwise default to rgb
        if not isinstance(color_format, str):
            color_format = 'rgb'
        convert_from_float = (
            color_format.endswith('f') 
            or color_format.endswith('float')
        )
        if isinstance(v1, str):
            if v1.startswith('#'):
                v1 = v1[1:]
            if len(v1) >= 4:
                try:
                    v2 = int(v1[2:4], base=16)
                    v3 = int(v1[4:6], base=16)
                    if len(v1) >= 8:
                        v4 = int(v1[6:8], base=16)
                    v1 = int(v1[0:2], base=16)
                except ValueError:
                    raise ValueError('Unsupported string format')
            else:
                raise ValueError('Unsupported string format')
        elif isinstance(v1, Iterable):
            if len(v1) >= 3:
                v2 = v1[1]
                v3 = v1[2]
                if len(v1) >= 4:
                    v4 = v1[3]
                v1 = v1[0]
        elif v2 is None or v3 is None:
            raise ValueError('Use hex string or iterable as first argument or give at least values 1 through 3')
        if v4 is None:
            v4 = 1 if convert_from_float else 255
        for v in (v1, v2, v3, v4):
            if not isinstance(v, (int, float)):
                raise ValueError('Unsupported type ' + type(v).__name__ + '. Use int, float or hex string representation')
        if convert_from_float:
            v1, v2, v3, v4 = [int(v * 255) for v in (v1, v2, v3, v4)]
        for v in (v1, v2, v3, v4):
            if clip_values:
                if v > 255:
                    v = 255
                if v < 0:
                    v = 0
            elif not 0 <= v <= 255:
                raise ValueError('Color values out of range')
        if color_format.startswith('rgb'):
            self.r = v1
            self.g = v2
            self.b = v3
        elif color_format.startswith('hsv'):
            self.r, self.g, self.b = colorsys.hsv_to_rgb(v1 / 255., v2 / 255., v3 / 255.)  
            self.r = int(self.r * 255)
            self.g = int(self.g * 255)
            self.b = int(self.b * 255)  
        elif color_format.startswith('hls'):
            self.r, self.g, self.b = colorsys.hls_to_rgb(v1 / 255., v2 / 255., v3 / 255.)
            self.r = int(self.r * 255)
            self.g = int(self.g * 255)
            self.b = int(self.b * 255)
        else:
            raise ValueError('Unknown color format')
        self.a = v4

    def tuple(self, include_alpha=True):
        if include_alpha:
            return (self.r, self.g, self.b, self.a)
        else:
            return (self.r, self.g, self.b)

    @property
    def t(self):
        return (self.r, self.g, self.b, self.a)
    
    def as_hsv(self, include_alpha=True):
        h, s, v = colorsys.rgb_to_hsv(self.r / 255., self.g / 255., self.b / 255.)
        if include_alpha:
            return (h, s, v, self.a / 255.)
        else:
            return (h, s, v)
    
    def as_hls(self, include_alpha=True):
        h, l, s = colorsys.rgb_to_hls(self.r / 255., self.g / 255., self.b / 255)
        if include_alpha:
            return (h, l, s, self.a / 255)
        else:
            return (h, l, s)

    def __str__(self):
        return f'Color{self.r, self.g, self.b, self.a}'
    
    def __iter__(self):
        return _ColorIterator(self)
    
    def __getitem__(self, index):
        if index == 0:
            return self.r
        if index == 1:
            return self.g
        if index == 2:
            return self.b
        if index == 3:
            return self.a
        raise IndexError

class _ColorIterator:
    ''' Iterator Class '''
    def __init__(self, color):
        self._color = color
        self._index = -1
    
    def __next__(self):
        if self._index >= 3:
            raise StopIteration
        self._index += 1
        return self._color[self._index]

# Color constants
Color.WHITE = Color(255, 255, 255)
Color.BLACK = Color(0,   0,   0  )

# Pure colors (only containing 255 and 0 values)
Color.PURE_RED   = Color(255, 0,   0  )
Color.PURE_GREEN = Color(0,   255, 0  )
Color.PURE_BLUE  = Color(0,   0,   255)

Color.PURE_YELLOW  = Color(255, 255, 0  )
Color.PURE_MAGENTA = Color(255, 0,   255)
Color.PURE_CYAN    = Color(0,   255, 255)

# Handpicked colors, more aesthetically pleasing
Color.RED    = Color(225, 60,  60 )
Color.BLUE   = Color(60,  60,  225)
Color.GREEN  = Color(30,  112, 30 )
Color.LIME   = Color(60,  225, 60 )
Color.YELLOW = Color(225, 205, 60 )

# Perfectly gray colors
Color.DARK_GRAY  = Color(55,  55,  55)
Color.LIGHT_GRAY = Color(120, 120, 120)
Color.OFFWHITE   = Color(215, 215, 215)
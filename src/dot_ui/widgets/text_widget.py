from .base_widget import *

class Text(Widget):
    def __init__(
        self,
        text = "",
        x = 0,
        y = 0,
        width = 100,
        height = 100,
        alignment_x="center",
        alignment_y="center",
        typeface=None,
        font_size=20,
        color=Color.WHITE,
        bold=False,
        italic=False,
        bold_font=None,
        italic_font=None,
        bold_italic_font=None,
        system_font=False,
        antialias=True,
        **kwargs
    ):
        Widget.__init__(self, x, y, width, height, **kwargs)
        self.background_color = Color(0, 0, 0, 0)
        self.text = text
        self.alignment_x = alignment_x
        self.alignment_y = alignment_y
        self.typeface = typeface
        self.font_size = font_size
        self.color = color
        self._bold = bold
        self._italic = italic
        self.system_font = system_font
        self.antialias = antialias

        self.bold_font = bold_font
        self.italic_font = italic_font
        self.bold_italic_font = bold_italic_font

        if self.typeface is None:
            self.typeface = UI_MODULE_PATH + '/data/font/Poppins-Regular.ttf'
        if self.bold_font is None:
            self.bold_font = UI_MODULE_PATH + '/data/font/Poppins-Black.ttf'
        if self.italic_font is None:
            self.italic_font = UI_MODULE_PATH + '/data/font/Poppins-Italic.ttf'
        if self.bold_italic_font is None:
            self.bold_italic_font = UI_MODULE_PATH + '/data/font/Poppins-BlackItalic.ttf'
    
    def _init(self):
        Widget._init(self)
        self.generate_fonts()

    def generate_fonts(self):
        if self.system_font:
            self.font = pygame.font.SysFont(self.typeface, self.font_size, self.bold, self.italic)
        else:
            self.regular_font = pygame.font.Font(self.typeface, self.font_size)
            if self.bold_font is not None:
                self.bold_font = pygame.font.Font(self.bold_font, self.font_size)
            if self.italic_font is not None:
                self.italic_font = pygame.font.Font(self.italic_font, self.font_size)
            if self.bold_italic_font is not None:
                self.bold_italic_font = pygame.font.Font(self.bold_italic_font, self.font_size)
            self.update_font()

    def update_font(self):
        if self.system_font:
            self.font = pygame.font.SysFont(self.typeface, self.font_size, self.bold, self.italic)
        else:
            if self.bold:
                if self.italic:
                    self.font = self.bold_italic_font
                else:
                    self.font = self.bold
            elif self.italic:
                self.font = self.italic_font
            else:
                self.font = self.regular_font

    @property
    def bold(self):
        return self._bold
    
    @bold.setter
    def bold(self, value):
        self._bold = value
        self.update_font()
    
    @property
    def italic(self):
        return self._italic
    
    @italic.setter
    def italic(self, value):
        self._italic = value
        self.update_font()

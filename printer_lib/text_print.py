'Things used by Text Printing feature'

from .pf2 import PF2

class TextCanvas():
    'Canvas for text printing, requires PF2 lib'
    width: int
    height: int
    canvas: bytearray = None
    rtl: bool
    wrap: bool
    pf2 = None
    def __init__(self, width, *, wrap=False, rtl=False):
        self.pf2 = PF2()
        self.width = width
        self.wrap = wrap
        self.rtl = rtl
        self.height = self.pf2.max_height + self.pf2.descent
        self.flush_canvas()
    def flush_canvas(self):
        'Flush the canvas, returning the canvas data'
        if self.canvas is None:
            pbm_data = None
        else:
            pbm_data = bytearray(self.canvas)
        self.canvas = bytearray(self.width * self.height // 8)
        return pbm_data
    def puttext(self, text):
        ''' Put the specified text to canvas.
            It's a generator, will `yield` the data produced, per line.
        '''
        text = text.replace('\t', ' ' * 4)
        canvas_length = len(self.canvas)
        pf2 = self.pf2
        current_width = 0
        last_space_at = -1
        width_at_last_space = 0
        break_points = set()
        characters = {}
        for i, s in enumerate(text):
            if s not in characters:
                characters[s] = pf2[s]
            char = characters[s]
            if s == ' ':
                last_space_at = i
                width_at_last_space = current_width
            if (current_width > self.width and
                last_space_at != -1):
                break_points.add(last_space_at)
                current_width -= width_at_last_space
            if s == '\n':
                current_width = 0
                continue
            current_width += pf2.point_size // 2 # + char.x_offset
        current_width = 0
        for i, s in enumerate(text):
            char = characters[s]
            if (i in break_points or s == '\n' or
                current_width + char.width > self.width):
                # print(current_width, end=' ')
                yield self.flush_canvas()
                current_width = 0
                if s in ' ':
                    continue
            if ord(s) in range(0x00, 0x20):   # glyphs that should not be printed out
                continue
            for x in range(char.width):
                for y in range(char.height):
                    rtl_current_width = self.width - current_width - char.width - 1
                    target_x = x + char.x_offset
                    target_y = pf2.ascent + (y - char.height) - char.y_offset
                    canvas_byte = (self.width * target_y + current_width + target_x) // 8
                    canvas_bit = 7 - (self.width * target_y + current_width + target_x) % 8
                    if self.rtl:
                        canvas_byte = (self.width * target_y + rtl_current_width + target_x) // 8
                        canvas_bit = 7 - (self.width * target_y + rtl_current_width + target_x) % 8
                    else:
                        canvas_byte = (self.width * target_y + current_width + target_x) // 8
                        canvas_bit = 7 - (self.width * target_y + current_width + target_x) % 8
                    if canvas_byte < 0 or canvas_byte >= canvas_length:
                        continue
                    char_byte = (char.width * y + x) // 8
                    char_bit = 7 - (char.width * y + x) % 8
                    self.canvas[canvas_byte] |= (
                        char.bitmap_data[char_byte] & (0b1 << char_bit)
                    ) >> char_bit << canvas_bit
            current_width += char.device_width

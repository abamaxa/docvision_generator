import os

from PIL import Image, ImageDraw, ImageFont

from .text_renderer import TextRenderer

class Draw:
    AlignLeft = 0
    AlignRight = 1
    AlignCenter = 2
    AlignJustify = 3

    def __init__(self, state):
        self.params = state
        self.image = None
        self.font = None
        self.draw = None
        self._measure_only = False

    def init_image(self):
        self.image = Image.new('RGBA', self.get_image_size(), (0,0,0,0))

    def create_draw(self):
        self.cleanup()
        this_dir = os.path.dirname(os.path.realpath(__file__))
        font_path = os.path.join(this_dir, "fonts", self.params.font_name)
        
        self.font = ImageFont.truetype(font_path, self.params.font_size)
        self.draw = ImageDraw.Draw(self.image)

    def get_line_height(self):
        return self.draw.textsize("Hg", font=self.font)[1]

    def get_image_size(self):
        return (self.params.width, self.params.height)

    def set_measure_only_mode(self, mode):
        self._measure_only = mode
        
    def get_measure_only_mode(self):
        return self._measure_only
    
    measure_only_mode = property(get_measure_only_mode, set_measure_only_mode)
        
    @property
    def line_spacing(self) :
        return self.params.line_spacing

    def draw_rectangle(self, points, fill=None, outline=None):
        if not self.measure_only_mode:
            self.draw.rectangle(points, fill, outline)

    def draw_line(self, points, width=1, color = None, style=None):
        if self.measure_only_mode:
            return
        
        _color = color
        if _color is None :
            _color = self.params.border_color
        
        self.draw.line(points, fill=_color, width=width)
            
    def draw_circle(self, center, radius, color = None):
        if self.measure_only_mode:
            return
        
        point = ((center[0] - radius,
                  center[1] - radius),
                 (center[0] + radius,
                  center[1] + radius))
        
        _color = color
        if _color is None :
            _color = self.params.border_color        
        
        self.draw.ellipse(point, None, self.params.border_color)  
            
    def draw_text_line(self, position, text, text_color) :
        if self.measure_only_mode:
            return
            
        self.draw.text(position, text, text_color, self.font)
            
    def draw_question_circle(self, top_left):
        if not self.measure_only_mode:
            extra = int(self.params.font_size * 0.2)
            point = ((top_left[0] - extra,
                      top_left[1] - extra),
                     (top_left[0] + self.params.line_height + extra,
                      top_left[1] + self.params.line_height + extra))
            self.draw.ellipse(point,
                              fill=self.params.question_fill_color,
                              outline=self.params.border_color)

    def text_size(self, text) :
        return self.draw.textsize(text, font=self.font)
    
    def draw_horizontal_styles(self, rect, is_top):
        left = rect[0][0]
        right = rect[1][0]
        
        if self.params.has_top_column_line() and is_top:
            line_top = rect[0][1]
            self.draw_line(((left, line_top), (right,line_top)),
                                self.params.horizontal_line_width,
                                style=self.params.horizontal_linestyle)

        elif self.params.has_bottom_column_line() and not is_top:
            line_top = rect[1][1]
            self.draw_line(((left,line_top), (right, line_top)),
                                self.params.horizontal_line_width,
                                style=self.params.horizontal_linestyle)

        return self.params.get_horizontal_padding()

    def save(self, filename, rect=None, resize_to=None):
        dirname = os.path.dirname(filename)
        if dirname :
            os.makedirs(dirname, exist_ok=True)

        if rect is None and resize_to is None:
            img = self.image
        else:
            img = self.copy_rect(rect, resize_to)

        img.save(filename)
        
        return img
            
    def get_image(self) :
        return self.image
    
    def blit(self, image, points) :
        self.image.paste(image, tuple(points))
    
    def copy_rect(self, rect, color):
        img = Image.new(
            'RGB',
            (rect[1][0] -
             rect[0][0],
             rect[1][1] -
             rect[0][1]), color)
        img_src = self.image.crop(
            (rect[0][0], rect[0][1], rect[1][0], rect[1][1]))
        img.paste(img_src, (0,0), img_src)
        
        return img

    def cleanup(self):
        if self.draw:
            del self.draw
            self.draw = None
            
    @staticmethod
    def debug_rects(img, rectangles, save_as_file):
        draw = ImageDraw.Draw(img)
        for rect in rectangles:
            draw.rectangle(rect, outline="red")
        img.save(save_as_file)
        
    #def __render_text(
            #self,
            #position,
            #line_width,
            #word_list,
            #align,
            #text_color):
        #if align in (Draw.AlignLeft, Draw.AlignJustify):
            #write_position = position
        #else:
            #last_text_width, _ = self.draw.textsize(
                #" ".join(word_list), font=self.font)
            #if align == Draw.AlignRight:
                #write_position = (
                    #position[0] + (line_width - last_text_width), position[1])
            #elif align == Draw.AlignCenter:
                #write_position = (
                    #position[0] + ((line_width - last_text_width) / 2), position[1])

        #if align == Draw.AlignJustify and len(word_list) > 1:
            #justify_space = []
            #for justify_word in word_list:
                #jwidth, _ = self.draw.textsize(justify_word, font=self.font)
                #justify_space.append(jwidth)

            #extra_space = (line_width - sum(justify_space)
                           #) / (len(word_list) - 1)
            #curx = position[0]
            #jw_count = 0

            #for justify_word, jwidth in zip(word_list, justify_space):
                #jw_count += 1
                #if jw_count == len(word_list):
                    #curx = position[0] + line_width - jwidth

                #if not self.measure_only_mode:
                    #self.draw.text((curx, position[1]), justify_word,
                                   #font=self.font, fill=text_color)

                #curx += jwidth + extra_space

        #elif not self.measure_only_mode:
            #self.draw.text(write_position, " ".join(word_list),
                           #font=self.font, fill=text_color)
            
    #def draw_text(
            #self,
            #position,
            #width,
            #text,
            #align=AlignLeft,
            #first_line_offset=0,
            #force_color=None):

        #if force_color:
            #text_color = force_color
        #else:
            #text_color = self.params.text_color

        #words = text.split(' ')
        #word_list = []
        #total_height = 0
        #counter = 0

        #for word in words:
            #counter += 1
            #if total_height == 0:
                #line_width = width - first_line_offset
            #else:
                #line_width = width

            #text_width, text_height = self.draw.textsize(
                #" ".join(word_list + [word]), font=self.font)

            #if text_width > line_width or counter == len(words):
                #if text_width <= line_width or not word_list:
                    #word_list.append(word)
                    #if align == Draw.AlignJustify:
                        #align = Draw.AlignLeft

                #if total_height == 0 and first_line_offset:
                    #offset_position = (
                        #position[0] + first_line_offset, position[1])
                    #self.__render_text(
                        #offset_position,
                        #line_width,
                        #word_list,
                        #align,
                        #text_color)
                #else:
                    #self.__render_text(
                        #position, line_width, word_list, align, text_color)

                #total_line_height = int(
                    #text_height * self.params.line_spacing)
                #position = (position[0], position[1] + total_line_height)
                #total_height += total_line_height

                #if text_width > width and counter == len(words):
                    #self.__render_text(
                        #position, width, [word], align, text_color)
                    #total_height += total_line_height

                #word_list = []

            #word_list.append(word)

        #return total_height
    
    #def calculate_text_height(self, width, text) :
        #initial_mode = self.measure_only_mode
        #try :
            #self.set_measure_only_mode(True)
            #return self.draw_text((0,0), width, text)
        
        #finally :
            #self.set_measure_only_mode(initial_mode)      



import os
import re
import string

from PIL import Image, ImageDraw, ImageFont
from .text_renderer import TextRenderer
from .bounds import Bounds
from .frame import Frame, RotatedFrame

class Draw:
    AlignLeft = 0
    AlignRight = 1
    AlignCenter = 2
    AlignJustify = 3

    def __init__(self, state):
        self.params = state
        self.image = None
        self.font = None
        self.font_bold = None
        self.font_italic = None
        self.draw = None
        self._measure_only = False
        self.word_boxes = []

    def init_image(self):
        self.image = Image.new('RGBA', self.get_image_size(), (0,0,0,0))

    def create_draw(self):
        self.cleanup()
        this_dir = os.path.dirname(os.path.realpath(__file__))
        font_path = os.path.join(this_dir, "fonts", self.params.font_name)
        self.font = ImageFont.truetype(font_path, self.params.font_size)
        
        font_path = os.path.join(this_dir, "fonts", self.params.font_bold_name)
        self.font_bold = ImageFont.truetype(font_path, self.params.font_size)
        
        font_path = os.path.join(this_dir, "fonts", self.params.font_italic_name)
        self.font_italic = ImageFont.truetype(font_path, self.params.font_size)
        
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
            _color = outline
            if _color is None :
                _color = self.params.border_color
                
            self.draw.rectangle(points, fill, _color)

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
            
    def draw_text_line(self, position, text, text_color = None) :
        self.__draw_text_line(position, text, text_color, False)  
        
    def draw_bold_text_line(self, position, text, text_color = None) :
        self.__draw_text_line(position, text, text_color, True)  
        
    def __draw_text_line(self, position, text, text_color, bold) :
        if self.measure_only_mode:
            return
        
        _color = text_color
        if _color is None :
            _color = self.params.text_color  
            
        if bold :
            font = self.font_bold
        else :
            font = self.font
         
        if self.params.options["wordboxes"] :   
            self.__text_with_word_boxes(position, text, _color, font)
        else :  
            self.draw.text(position, text, _color, font)
        
    def __text_with_word_boxes(self, position, text, color, font) :
        #word_list = re.split(r'([\W]+)', text)
        word_list = re.split(r'([\W]+)', text)
        x, y = position
        
        space_width = self.draw.textsize(" ", font=font)
        for word in word_list :
            word = word.strip()
            if not word :
                continue
            
            sz = self.draw.textsize(word, font=font)
                        
            if not word in string.punctuation :
                box = (x - 1, y + 2, x + sz[0] +1, y + sz[1] + 2)
                self.__add_text_box(box, word)
                
            self.draw.text((x,y), word, color, font)
            
            x += sz[0] + space_width[0]
    
    def draw_question_circle(self, top_left) :
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
       
    def blit_text(self, image, points) :
        self.blit(image, points)
        box = list(points)
        box[2] = min(box[0] + image.size[0], points[2])
        self.__add_text_box(box, '###')
        
    def blit(self, image, points) :
        width, height = image.size
        if len(points) == 4 and \
           (width != points[2] - points[0] or \
            height != points[3] - points[1]) :
            img_crop = image.crop((0,0,
                                   points[2] - points[0],
                                   points[3] - points[1]))
            self.image.paste(img_crop, tuple(points))
        else :
            self.image.paste(image, tuple(points[:2]))
    
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
    
    def __add_text_box(self, box, label) :
        if not self.params.options["wordboxes"] :
            return

        points = (box[0], box[1], 
                  box[2], box[1],
                  box[2], box[3],
                  box[0], box[3])
        
        #self.draw.polygon(points, outline="red")
        
        frame = RotatedFrame(points, label)
        self.word_boxes.append(frame)
        
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
        


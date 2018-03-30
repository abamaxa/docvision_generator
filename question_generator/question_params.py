import random
import string
import json
import os

from graphics import Draw
from .util import pick_from_list, generate_shade_of_dark_grey, generate_shade_of_light_grey

HSep_None = 0
HSep_BlankLine1 = 0.5
HSep_BlankLine2 = 0.75
HSep_BlankLine3 = 1.
HSep_BlankLine4 = 1.25

HSep_SolidLine = 0x8
HSep_DashedLine = 0x10
HSep_DottedLine = 0x20

HLine_Top = 0x40
HLine_Bottom = 0x80

VSep_None = 0
VSep_BlankLine1 = 1
VSep_BlankLine2 = 1.25
VSep_BlankLine3 = 1.5
VSep_BlankLine4 = 1.75

VSep_SolidLine = 0x8
VSep_DashedLine = 0x10
VSep_DottedLine = 0x20

VLine_Left = 0x40
VLine_Right = 0x80
VLine_LeftAndRight = 0x100
VLine_Internal = 0x40
VLine_ExternalAndInternal = 0x80

ROMAN_DIGITS = [
    "i",
    "ii",
    "iii",
    "iv",
    "v",
    "vi",
    "vii",
    "viii",
    "ix",
    "x",
    "xi"
    "xii",
    "xiii",
    "xiv",
    "xv"]

# This class is starting to merge parameters applicable to individual questions
# with parameters that apply to the whole document. This is adding to complexity
# - need seperate question/document parameters. Also, could layout be more 
# within the domain of individual questions to allow pages where some questios are 
# in columns but others cut across page.
# Perhaps a question template file, with a set of parameters that are randomised
# and then rendered.
#
# Commands: text(location/length), graphic(location/content), drawing(relative position/parameters)
#
class QuestionParams(dict):
    def __init__(self, name, options):
        super(QuestionParams, self).__init__()
        self.__dict__ = self

        self.name = str(name)
        self.options = options

        dimensions = options["dimensions"]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.image_format = options.get("format", "png")

        self.draw_debug_rects = False

        self.left_margin = self.right_margin = 0
        self.top_margin = self.bottom_margin = 0

        self.line_height = self.font_size = 0
        self.font_name = None
        self.minimum_question_gap = 0

        self.line_height = 0
        #===
        self.line_spacing = 0
        self.para_spacing = 0

        self.text_align = None
        self.columns = 0

        self.horizontal_space = None
        self.horizontal_linestyle = None
        self.horizontal_lineposition = None

        self.vertical_space = None
        self.vertical_linestyle = None
        self.vertical_lineposition = None

        self.horizontal_priority = 0

        self.number_color = None
        self.text_color = None
        self.border_color = None
        # This is only used for graphics, the actual page background is 
        # is draw during augmentation
        self.fake_background_color = None

        self.horizontal_line_width = 0
        self.vertical_line_width = 0

        self.question_fill_color = None
        
        self.para_margin = 0
        self.sub_para_prefix = None
        self.sub_para_margin_left = 0
        self.sub_para_margin_right = 0
        self.sub_para_terminator = None
        self.sub_para_digits = None     
        
        self.embedded_image_frames = []

    def generate_random_parameters(self):
        self.is_maths_question = random.choice((True, False))
        
        self.left_margin = self.width * (0.03 + (0.05 * random.random()))
        self.right_margin = self.width * (0.03 + (0.05 * random.random()))
        self.top_margin = self.height * (0.04 + (0.05 * random.random()))
        self.bottom_margin = self.height * (0.04 + (0.05 * random.random()))

        fontnames = ["verdana.ttf", "times.ttf", "georgia.ttf", "arial.ttf"]

        # Assume that its A4 size, calculate relative to width
        #self.line_height = self.font_size = random.randint(18,24)
        self.line_height = self.font_size = random.randint(
            int(self.width / 70), int(self.width / 50))
        self.font_name = random.choice(fontnames)

        columns = ((0.66, 1), (0.9, 2), (1., 3))
        hseps_lines = (
            (0.2, HSep_BlankLine1),
            (0.6, HSep_BlankLine2),
            (0.85, HSep_BlankLine3),
            (1.0, HSep_BlankLine4),
        )

        vseps_lines = (
            (0.2, VSep_BlankLine1),
            (0.6, VSep_BlankLine2),
            (0.85, VSep_BlankLine3),
            (1.0, VSep_BlankLine4),
        )

        hseps_styles = (
            (0.7, HSep_None),
            (0.8, HSep_SolidLine),
            (0.9, HSep_DashedLine),
            (1.0, HSep_DottedLine),
        )

        vseps_styles = (
            (0.7, VSep_None),
            (0.8, VSep_SolidLine),
            (0.9, VSep_DashedLine),
            (1.0, VSep_DottedLine),
        )

        hseps_positions = (
            (0.65, HSep_None),
            (0.9, HLine_Bottom),
            (1.0, HLine_Top),
        )

        vseps_positions = (
            (0.65, VSep_None),
            (0.85, VLine_LeftAndRight),
            (0.93, VLine_Left),
            (1.0, VLine_Right),
        )

        alignment = (
            (0.65, Draw.AlignLeft),
            (0.85, Draw.AlignJustify),
        )

        self.line_spacing = pick_from_list(
            ((0.65, 1.2), (0.85, 1.3), (1.0, 1.5)))
        self.para_spacing = self.line_height * \
            self.line_spacing * (0.25 + (random.random() * 0.5))

        self.text_align = pick_from_list(alignment)
        self.columns = pick_from_list(columns)

        if self.columns > 1:
            vseps_styles = [(p * .5, a) for p, a in vseps_styles]

        self.horizontal_space = pick_from_list(hseps_lines)
        self.horizontal_linestyle = pick_from_list(hseps_styles)
        self.horizontal_lineposition = pick_from_list(hseps_positions)

        self.vertical_space = pick_from_list(vseps_lines)
        self.vertical_linestyle = pick_from_list(vseps_styles)
        self.vertical_lineposition = pick_from_list(vseps_positions)

        self.horizontal_priority = random.random()

        self.fake_background_color = generate_shade_of_light_grey()
        self.number_color = self.fake_background_color 
        self.text_color = generate_shade_of_dark_grey()

        if random.random() > 0.7:
            self.border_color = generate_shade_of_dark_grey()
        else:
            self.border_color = self.text_color

        self.horizontal_line_width = random.choice(list(range(1, 5)))
        self.vertical_line_width = random.choice(list(range(1, 5)))

        self.question_fill_color = random.choice(
            [self.border_color, self.text_color, "blue", "grey", "green", "purple"])

        self.minimum_question_gap = self.para_spacing * 1.5

        #self.line_height = draw.get_line_height()
        self.generate_random_paragraph_features()
        self.generate_embedded_image_frames()
        
        self.padding = random.randint(int(self.line_height / 4), self.line_height * 2)
        self.margins = self.padding // 2
        self.debug_dump()

    def generate_random_paragraph_features(self) :  
        para_margin = (
            (0.80, 0),
            (0.90, 2.2 * self.line_height),
            (1.00, 1.8 * self.line_height),
        )        
        self.para_margin = int(pick_from_list(para_margin))
        self.sub_para_prefix = int(random.randint(0, 2) * self.line_height * 0.3)
        if self.para_margin:
            sub_para_margin = (
                (0.80, self.para_margin),
                (1.00, self.para_margin + (random.random() * self.get_column_width() / 3)),
            )               
            self.sub_para_margin_left = int(pick_from_list(sub_para_margin))
            self.sub_para_margin_right = self.sub_para_margin_left
        else:
            self.sub_para_margin_left = int(random.choice(
                    [0, 2.2 * self.line_height, 1.8 * self.line_height]))
            self.sub_para_margin_right = self.sub_para_margin_left
            
            
        self.sub_para_terminator = random.choice([".", ")", ")."])
        if random.random() < 0.5:
            self.sub_para_digits = string.ascii_lowercase
        else:
            self.sub_para_digits = ROMAN_DIGITS    
            
    def generate_embedded_image_frames(self) :
        if self.is_maths_question :
            prob = 0.6
        else :
            prob = 0.2
            
        for i in range(20) :
            if random.random() < prob :
                width = self.get_column_width() * (0.5 + (0.5 * random.random()))
                height = width * (0.7 + (0.6 * random.random()))       
                self.embedded_image_frames.append((width, height))
            else :
                self.embedded_image_frames.append(None)
            
    def get_column_width(self) :
        return self.get_available_width() / self.columns

    def get_available_width(self):
        return self.width - self.left_margin - self.right_margin

    def get_column_rect(self, column_number):
        column_width = self.get_column_width()

        return (
            (self.left_margin + (column_number * column_width), self.top_margin),
            (self.left_margin + ((1 + column_number) * column_width),
             self.height - self.bottom_margin)
        )

    def has_left_column_line(self, column):
        line_pos = self.vertical_lineposition
        if column == 1 and line_pos in (VLine_Left, VLine_LeftAndRight):
            return True

        elif self.columns > 1 and line_pos == VLine_ExternalAndInternal:
            return True

        elif line_pos == VLine_Internal and column > 1 :
            return True

        return False
    
    def has_right_column_line(self, column):
        line_pos = self.vertical_lineposition
        if column == self.columns and line_pos in (VLine_Right, VLine_LeftAndRight):
            return True

        elif self.columns > 1 and line_pos == VLine_ExternalAndInternal:
            return True

        elif line_pos == VLine_Internal and column != self.columns:
            return True

        return False    
    
    def get_column_padding_left(self, column):
        if self.has_left_column_line(column) :
            return self.get_vertical_padding()
        else :
            return 0
        
    def get_column_padding_right(self, column):
        if self.has_right_column_line(column) :
            return self.get_vertical_padding()
        else :
            return 0    
        
    def has_top_column_line(self) :
        return self.horizontal_lineposition == HLine_Top
        
    def get_column_padding_top(self):
        if self.has_top_column_line() :
            return self.get_horizontal_padding()
        else :
            return 0
        
    def has_bottom_column_line(self) :
        return self.horizontal_lineposition == HLine_Bottom    
        
    def get_column_padding_bottom(self):
        if self.has_bottom_column_line() :
            return self.get_vertical_padding()
        else :
            return 0
        
    def get_horizontal_padding(self) :
        padding = self.line_height * self.horizontal_space
        if padding < self.minimum_question_gap:
            padding = self.minimum_question_gap 
        return padding
    
    def get_vertical_padding(self) :
        return self.line_height * self.vertical_space
        
    def adjust_rect_for_style(self, rect, column=1):
        top = rect[0][1] + self.get_column_padding_top()
        bottom = rect[1][1] - self.get_column_padding_bottom()
        left = rect[0][0] + self.get_column_padding_left(column)
        right = rect[1][0] - self.get_column_padding_right(column)
        
        return ((left, top), (right, bottom))        
    
    def adjust_rect(self, rect, column=1):
        top = rect[0][1] + self.get_horizontal_padding()
        bottom = rect[1][1] - self.get_horizontal_padding()
        left = rect[0][0] + self.get_vertical_padding()
        right = rect[1][0] - self.get_vertical_padding()
        
        return ((left, top), (right, bottom))      
    
    def debug_dump(self) :
        filename = "{}-parameters.json".format(self.name)
        dirname = self.options.get("outputDir", "output")
        os.makedirs(dirname, exist_ok = True)
        filepath = os.path.join(dirname, filename)
        with open(filepath, "w") as dump_file :
            json.dump(self, dump_file, indent=4)
            
    def generate_question_texts(self, sentence=False):
        if sentence:
            return self.generator.generate_sentence()[2]
        else:
            return self.generator.generate_sentence()[2]    
    
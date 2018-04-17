import random
import string
import json
import os

from graphics import Draw, TextRenderer
from graphics.util import pick_from_list, generate_shade_of_dark_grey, generate_shade_of_light_grey
from .dictionary_generator import TextGen

class PageParameters(dict):
    FONTS = {"roboto" : "Roboto", 
             "robotocondensed" : "RobotoCondensed",
             "robotomono" : "RobotoMono",
             "ibmplexsans" : "IBMPlexSans",
             "ibmplexserif" : "IBMPlexSerif"}
    
    def __init__(self, name, options):
        super(PageParameters, self).__init__()
        self.__dict__ = self

        self.name = str(name)
        self.options = options
        self.width, self.height = options["dimensions"]
        self.image_format = options.get("format", "png")

        self.line_height = 0
        self.font_size = 0
        self.font_name = None
        self.font_bold_name = None  
        self.font_italic_name = None        
        
        self.left_margin = self.right_margin = 0
        self.top_margin = self.bottom_margin = 0        

        self.line_spacing = 0
        self.columns = 0

        self.number_color = None
        self.text_color = None
        self.border_color = None
        
        self.line_weight = 1
        self.padding_top_bottom = 0
        self.padding_left_right = 0
        self.margin_left_right = 0
        self.margin_top_bottom = 0
        self.inter_question_gap = 0
        self.end_text = False
        
        self.generator = TextGen.get_generator()
        
    def generate_random_parameters(self) : 
        self.create_column_parameters()
        self.select_text_parameters()
        self.generate_colours()
        self.generate_margins_and_padding()
                
        self.line_weight = random.choice(list(range(1, 5)))
        
    def generate_colours(self) :
        self.fake_background_color = generate_shade_of_light_grey()
        self.number_color = self.fake_background_color 
        self.text_color = generate_shade_of_dark_grey()
        
        if random.random() > 0.7:
            self.border_color = generate_shade_of_dark_grey()
        else:
            self.border_color = self.text_color        
        
        self.question_fill_color = random.choice(
            [self.border_color, self.text_color, "blue", "grey", "green", "purple"])
        
    def create_column_parameters(self) :
        #columns = ((0.66, 1), (0.9, 2), (1., 3))
        columns = ((0.8, 1), (1.0, 2))
        self.columns = pick_from_list(columns)
        #self.columns = 1
        
    def select_text_parameters(self) :
        font = random.choice(list(PageParameters.FONTS.keys()))  
        
        self.font_name = os.path.join(font, PageParameters.FONTS[font] + "-Regular.ttf")   
        self.font_bold_name = os.path.join(font, PageParameters.FONTS[font] + "-Bold.ttf")   
        self.font_italic_name = os.path.join(font, PageParameters.FONTS[font] + "-Italic.ttf")  
        
        self.line_height = self.font_size = random.randint(
            int(self.width / 70), int(self.width / 50))

        self.line_spacing = pick_from_list(
            ((0.65, 1.2), (0.85, 1.3), (1.0, 1.5)))
        
        self.text_align = pick_from_list(((0.9, TextRenderer.AlignLeft), 
                                          (1.0, TextRenderer.AlignJustify)))
        
        if 1 or random.random() < 0.1 :
            self.end_text = True

    def generate_margins_and_padding(self) :
        self.left_margin = self.width * (0.03 + (0.05 * random.random()))
        self.right_margin = self.width * (0.03 + (0.05 * random.random()))
        self.top_margin = self.height * (0.04 + (0.05 * random.random()))
        self.bottom_margin = self.height * (0.04 + (0.05 * random.random()))
        
        self.padding_top_bottom = 0 # random.randint(int(self.line_height / 4), int(self.line_height * 1.2))
        #self.padding_left_right = random.randint(int(self.line_height * 1.5), int(self.line_height * 2.5))
        self.padding_left_right = 0 #random.randint(int(self.line_height * 0.5), int(self.line_height * 1.5))
        self.margin_left_right = 0
        self.margin_top_bottom = 0
        self.inter_question_gap = max(self.line_height * 2,
                                      (self.padding_top_bottom + self.margin_top_bottom))

    def get_sentences(self, count):
        generator = self.generator.generate_sentences(count)
        sentences = [sentence[2] for sentence in generator]
        return " ".join(sentences)
    
    def get_words(self, count):
        word_list = self.generator.generate_sentence()[2]
        return " ".join(word_list.split(' ')[:count])   
    
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
        return False
    
    def has_right_column_line(self, column):
        return False        
import random
import string
from functools import partial

from graphics import Draw
from .page import Page

class Paragraph :
    def __init__(self, question, rect, question_number, paragraph, subparagraph, endparagraph) :
        self.height_consumed = 0
        self.params = question.parameters
        self.draw = question.draw
        self.rect = rect
        self.text_rect = self.params.adjust_rect(self.rect)
        self.width = self.text_rect[1][0] - self.text_rect[0][0]
        self.question_text_rect = None
        self.question_number = question_number
        self.paragraph = paragraph
        self.subparagraph = subparagraph
        self.endparagraph = endparagraph
        
        self.should_draw_question_number = True
               
    def reset(self) :
        self.height_consumed = 0
        
    def write_question_header(self):
        self.height_consumed += self.draw.draw_horizontal_styles(self.rect, True)
    
    def write_question_footer(self):
        bottom_rect = self.calculate_area_consumed()

        self.height_consumed += self.draw.draw_horizontal_styles(bottom_rect, False)
        
    def write_paragraphs(self):
        initial_consumed = self.height_consumed
        
        self.__write_main_paragraphs()
        self.__write_sub_paragraphs()
        self.__write_end_paragraphs()
         
        self.question_text_rect = (
            (
                self.text_rect[0][0] - self.params.line_height * 0.5, 
                self.text_rect[0][1] + initial_consumed - self.params.line_height * 0.5
            ), 
            (
                self.text_rect[1][0] + self.params.line_height * 0.5, 
                self.text_rect[0][1] + self.height_consumed + self.params.line_height * 0.5
            ), 
        )
        
        
    def __write_main_paragraphs(self) :
        paragraph_number = 0

        for text in self.paragraph:
            offset = 0
            if paragraph_number == 0:
                offset = self.__draw_question_number()
    
            self.__draw_paragraph_text(text, offset)
                
            paragraph_number += 1
            if paragraph_number != len(self.paragraph) or (self.subparagraph or self.endparagraph):
                self.height_consumed += self.params.para_spacing

    def __write_sub_paragraphs(self) :    
        paragraph_number = 0
        for text in self.subparagraph:
            self.__draw_sub_question_number(paragraph_number)
            self.__draw_sub_paragraph_text(text)
    
            paragraph_number += 1
            if paragraph_number != len(self.subparagraph) or self.endparagraph:
                self.height_consumed += self.params.para_spacing
                
    def __write_end_paragraphs(self) :
        paragraph_number = 0
        for text in self.endparagraph:
            self.__draw_paragraph_text(text)
            
            paragraph_number += 1
            if paragraph_number != len(self.endparagraph):
                self.height_consumed += self.params.para_spacing
                
    def __draw_paragraph_text(self, text, offset = 0) :
        self.height_consumed += self.draw.draw_text(
            (self.get_left(), self.get_top()),
            self.get_paragraph_width(), 
            text, 
            self.params.text_align, 
            first_line_offset=offset)      
        
    def __draw_sub_paragraph_text(self, text) :
        self.height_consumed += self.draw.draw_text(
                (self.get_left_sub_paragraph_margin(), self.get_top()),
                self.get_sub_paragraph_width(), text, self.params.text_align)    
    
        
    def __draw_sub_question_number(self, paragraph_number) :
        if not self.params.sub_para_margin_left:
            return
        
        self.draw.draw_text(
                (self.get_left_sub_paragraph_prefix(), self.get_top()),
                self.get_sub_paragraph_prefix_width(),
                self.get_sub_paragraph_number(paragraph_number),
                self.params.text_align)        
    
    def __draw_question_number(self) :
        offset = 0
        if not self.should_draw_question_number :
            return offset

        if self.params.para_margin == 0:
            self.draw.draw_question_circle(
                (self.text_rect[0][0], self.get_top()))
            offset = self.params.font_size * 1.5
            number_color = self.params.number_color
        else:
            number_color = self.params.text_color

        self.draw.draw_text(
            (self.text_rect[0][0], self.get_top()),
            self.width,
            str(self.question_number) + ".",
            Draw.AlignLeft,
            force_color=number_color)

        return offset
                
    
    def get_left(self) :
        return self.text_rect[0][0] + self.params.para_margin
    
    def get_top(self) :
        return self.text_rect[0][1] + self.height_consumed
    
    def get_left_sub_paragraph_prefix(self) :
        return self.get_left() + self.params.sub_para_prefix
    
    def get_left_sub_paragraph_margin(self) :
        return self.get_left_sub_paragraph_prefix() + self.params.sub_para_margin_left
    
    def get_paragraph_width(self) :
        return self.width - self.params.para_margin 
    
    def get_sub_paragraph_prefix_width(self) :
        return self.get_paragraph_width() - self.params.sub_para_prefix
    
    def get_sub_paragraph_width(self) :
        return self.get_sub_paragraph_prefix_width() - \
               self.params.sub_para_margin_left - self.params.sub_para_margin_right
    
    def get_sub_paragraph_number(self, paragraph_number) :
        return self.params.sub_para_digits[paragraph_number] + self.params.sub_para_terminator
    
    def calculate_area_consumed(self):
        bottom = self.question_text_rect[1][1] + self.params.get_vertical_padding()
        return (self.rect[0], (self.rect[1][0], bottom))

    def write_simple_question(self):
        """
        Number = 1-20, a-g
        Usually in a margin but can be indented.
        Often bold and followed by dot or bracket.
        """
        self.write_question_header()
        self.write_paragraphs()
        self.write_question_footer()

        return self.calculate_area_consumed(), self.question_text_rect

    def write_multipart_question(self):
        self.write_question_header()
        self.write_paragraphs()
        self.write_question_footer()

        return self.calculate_area_consumed(), self.question_text_rect    

class SimpleQuestion(Page):
    def generate_question_texts(self, sentence=False):
        if sentence:
            return self.generator.generate_sentence()[2]
        else:
            return self.generator.generate_sentence()[2]

    def write_question(self, question_number):
        trys = 0
        new_rect = scan_rect = None
        while True:
            rect = self.get_current_write_location()
            if rect is None:
                break

            trys += 1
            self.set_measure_only_mode(True)

            subparagraph = []
            endparagraph = []
            paragraph = [self.generate_question_texts()]
            if trys < 3:
                if random.random() < 0.5:
                    paragraph.append(self.generate_question_texts())

                if random.random() < 0.75:
                    for _ in range(random.randint(1, 3)):
                        subparagraph.append(self.generate_question_texts(True))

            if trys < 2 and random.random() < 0.5:
                endparagraph.append(self.generate_question_texts())

            paragraph_generator = Paragraph(self, rect, question_number, 
                                           paragraph, 
                                           subparagraph, 
                                           endparagraph)
            if subparagraph or endparagraph:
                func = partial(paragraph_generator.write_multipart_question)
            else:
                func = partial(paragraph_generator.write_simple_question)

            new_rect, scan_rect = func()
            if self.rect_fits_in_current_frame(new_rect):
                self.set_measure_only_mode(False)
                paragraph_generator.reset()
                new_rect, scan_rect = func()
                break

            elif trys > 4:
                scan_rect = None
                break

        return new_rect, scan_rect

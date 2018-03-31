import os
import random
import json
import zipfile
from io import BytesIO
import abc

from .dictionary_generator import TextGen
from .util import *
from graphics import Draw
from .question_params import QuestionParams

class Page(object):
    def __init__(self, name, options):
        super(Page, self).__init__()
        self._draw = None
        self.name = str(name)
        self.options = options
        self._params = QuestionParams(self.name, self.options)
        
        self.frames = []   
        self.question_frames = []
        self.question_text_frames = []
        
        self.draw_debug_rects = False

        self.generate_page()

    @property
    def draw(self) :
        return self._draw
    
    @property
    def parameters(self) :
        return self._params
    
    def generate_page(self):        
        self.parameters.generate_random_parameters()
        
        self._draw = Draw(self.parameters)
        self._draw.init_image()        
        self._draw.create_draw()    
        
        self.generate_layout()
       
    def draw_page_background(self) :
        self.draw_columns()        

    def set_measure_only_mode(self, mode):
        self._draw.measure_only_mode = mode

    def draw_columns(self):
        params = self.parameters
        column = 1

        for rect in self.frames:
            if self.parameters.has_left_column_line(column) :
                line = (rect[0], (rect[0][0], rect[1][1]))
                self._draw.draw_line(line, params.vertical_line_width,
                                    style=params.vertical_linestyle)
 
            if self.parameters.has_right_column_line(column) :
                line = ((rect[1][0], rect[0][1]), rect[1])
                self._draw.draw_line(line, params.vertical_line_width,
                                    style=params.vertical_linestyle)
                
            column += 1

    def generate_layout(self):
        for i in range(self.parameters.columns):
            rect = self.parameters.get_column_rect(i)

            self.frames.append(rect)
           
    def get_current_write_location(self):
        """
        This should return a rectangle specifiying where to write the next
        question.
        """
        if self.frames:
            return self.frames[0]
        
    def rect_fits_in_current_frame(self, remove_rect):
        height = remove_rect[1][1] - remove_rect[0][1]
        current_frame = self.frames[0]

        remaining_height = current_frame[1][1] - current_frame[0][1]
        return height < remaining_height

    def update_current_write_location(self, remove_rect):
        """
        Remove rect specifies an area to remove from the available space, either
        because a question has been written to it or because its too small to
        write the next question into.
        """
        height = remove_rect[1][1] - remove_rect[0][1]
        current_frame = self.frames[0]

        remaining_height = current_frame[1][1] - current_frame[0][1]
        if height >= remaining_height:
            self.frames.remove(current_frame)
        else:
            self.frames.remove(current_frame)
            self.frames.insert(
                0, ((current_frame[0][0], current_frame[0][1] + height), current_frame[1]))

    
    def create_page(self):
        self.draw_page_background()
        inflate_by = self._draw.get_line_height() * 0.5
        
        question_number = random.randint(1, 20)
        while True:
            rect = self.get_current_write_location()
            if rect is None:
                break

            new_rect, scan_rect = self.write_question(question_number)

            if scan_rect and self.rect_fits_in_current_frame(new_rect):
                self.question_text_frames.append(scan_rect)
                self.question_frames.append(inflate_rect(
                    new_rect, inflate_by, inflate_by))

                if self.options.get("draw_debug_rects") :
                    self._draw.draw_rectangle(scan_rect, outline="red")
                    self._draw.draw_rectangle(new_rect, outline="blue")

                question_number += 1

            self.update_current_write_location(new_rect)

    @abc.abstractmethod
    def write_question(self, question_number):
        pass
    
    def get_image(self) :
        return self._draw.get_image()    
     
    def get_frames(self) :
        return {
            "text" : self.question_text_frames,
            "question" : self.question_frames,
        }
    
    def get_sentences(self, count):
        return self.parameters.get_sentences(count)
    
    def get_words(self, count):
        return self.parameters.get_words(count)
        
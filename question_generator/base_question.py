import os
import random
import json
import zipfile
from io import BytesIO
import abc

from .dictionary_generator import TextGen
from .util import *
from .draw import Draw
from .question_params import QuestionParams

class Question(object):
    def __init__(self, name, options):
        super(Question, self).__init__()

        self.name = str(name)
        self.options = options
        self.params = QuestionParams(self.name, self.options)
        
        self.frames = []   
        self.question_frames = []
        self.question_text_frames = []
        
        self.draw_debug_rects = False

        self.generate_page()

    def generate_page(self):        
        self.params.generate_random_parameters()
        self.generator = TextGen.get_generator()
        
        self.draw = Draw(self.params)
        self.draw.init_image()        
        self.draw.create_draw()    
        
        self.generate_layout()
       
    def draw_page_background(self) :
        self.draw_columns()        

    def set_measure_only_mode(self, mode):
        self.draw.measure_only = mode

    def draw_columns(self):
        params = self.params
        column = 1

        for rect in self.frames:
            if self.params.has_left_column_line(column) :
                line = (rect[0], (rect[0][0], rect[1][1]))
                self.draw.draw_line(line, params.vertical_line_width,
                                    style=params.vertical_linestyle)
 
            if self.params.has_right_column_line(column) :
                line = ((rect[1][0], rect[0][1]), rect[1])
                self.draw.draw_line(line, params.vertical_line_width,
                                    style=params.vertical_linestyle)
                
            column += 1

    def generate_layout(self):
        for i in range(self.params.columns):
            rect = self.params.get_column_rect(i)

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
        inflate_by = self.draw.get_line_height() * 0.5
        
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
                    self.draw.rectangle(scan_rect, outline="red")
                    self.draw.rectangle(new_rect, outline="blue")

                question_number += 1

            self.update_current_write_location(new_rect)

    @abc.abstractmethod
    def write_question(self, question_number):
        pass
    
    def get_image(self) :
        return self.draw.get_image()    
     
    def get_frames(self) :
        return {
            "text" : self.question_text_frames,
            "question" : self.question_frames,
        }
import os
import random
import json
import zipfile
import time
from io import BytesIO
import abc
import logging

from .dictionary_generator import TextGen
from graphics import Draw
from .page_params import PageParameters
from augmentation import ImgAugAugmentor, ImageTiler

class Page(object):
    def __init__(self, name, options, persister):
        super(Page, self).__init__()
        self._draw = None
        self.name = str(name)
        self.options = options
        self.persister = persister
        self.seed = None
        
        self.seed_random_number_generator()
        
        self._params = PageParameters(self.name, self.options)
        
        self.frames = []   
        self.fragment_frames = []        
        self.draw_debug_rects = False
        self.current_fragment_number = random.randint(1, 20)

        self.generate_page()
        
    def seed_random_number_generator(self) :
        if self.options["random_seed"] :
            self.seed = self.options["random_seed"]
        elif self.options["deterministic"] :
            self.seed = self.name
        else :
            self.seed= "{}-{}".format(time.time(), self.name)
        
        random.seed(self.seed)
                    
    def generate_page(self):        
        self.parameters.generate_random_parameters()
        
        self._draw = Draw(self.parameters)
        self._draw.init_image()        
        self._draw.create_draw()    
        
        self.generate_layout()

    def generate_layout(self):
        for i in range(self.parameters.columns):
            rect = self.parameters.get_column_rect(i)

            self.frames.append(rect)    

    def create_page(self) :
        try :
            self.draw_columns()
            self.create_page_fragments()     
            self.draw_fragment_frames()
            
        except Exception as general_error :
            message = "Creating page name '{}' with seed '{}'".format(self.name, self.seed)
            logging.exception(message)
            
    def create_page_fragments(self) :
        while not self.is_page_full() :
            new_rect = self.create_fragment()
    
            if self.rect_fits_in_current_frame(new_rect):
                self.update_current_write_location(new_rect)
    
            else :
                self.mark_page_as_full()   
                
        if not self.fragment_frames :
            message = "Empty page, name '{}' with seed '{}'".format(self.name, self.seed)
            logging.error(message)
               
    def save(self) :
        tiler = ImageTiler(self)
        augmentor = ImgAugAugmentor(self, tiler, self.options)
    
        for aug_image, aug_frames in augmentor :
            self.persister.save_image(aug_image, aug_frames)
           
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
            
    def get_current_write_location(self):
        """
        This should return a rectangle specifiying where to write the next
        fragment.
        """
        if self.frames:
            return self.frames[0]
        
    def rect_fits_in_current_frame(self, remove_rect) :
        if remove_rect is None :
            return False
        
        height = remove_rect[1][1] - remove_rect[0][1]
        current_frame = self.frames[0]

        remaining_height = current_frame[1][1] - current_frame[0][1]
        return height < remaining_height

    def update_current_write_location(self, remove_rect):
        """
        Remove rect specifies an area to remove from the available space, either
        because a fragment has been written to it or because its too small to
        write the next fragment into.
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
           
    def add_detection_frame(self, frame) :
        self.fragment_frames.append(frame)
        
    def draw_fragment_frames(self) :
        if self.options.get("draw_debug_rects") :
            for frame in self.fragment_frames :
                self._draw.draw_rectangle(frame.rectangle, outline="blue")  
                            
    def is_page_full(self) :
        if self.options["single"] and self.fragment_frames :
            return True
        
        return self.get_current_write_location() is None
    
    def mark_page_as_full(self) :
        self.update_current_write_location(self.get_current_write_location())
    
    @abc.abstractmethod
    def create_fragment(self):
        pass
    
    @property
    def draw(self) :
        return self._draw
    
    @property
    def parameters(self) :
        return self._params
    
    def set_measure_only_mode(self, mode):
        self._draw.measure_only_mode = mode        

    def get_image(self) :
        return self._draw.get_image()    
     
    def get_frames(self) :
        return self.fragment_frames
    
    def get_sentences(self, count):
        return self.parameters.get_sentences(count)
    
    def get_words(self, count):
        return self.parameters.get_words(count)
        
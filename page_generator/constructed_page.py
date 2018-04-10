import logging

from graphics import Bounds, BoundsError
from .page import Page
from .constructed_page_factory import ConstructedQuestionFactory
from question_templates import ParameterParser, Numerator

class ConstructedPage(Page) :
    def __init__(self, name, options, persister):
        super().__init__(name, options, persister)
        self.factory = ConstructedQuestionFactory()
        self.current_question = None
        self.area_for_next_question = None
        self._numerator = None
        self.__create_numerator()
                      
    def create_question(self) :
        if self.name == "20" :
            print(self.name)
            
        for attempts in range(3) :
            try :
                self.get_area_for_next_question()
                if self.area_for_next_question is None:
                    logging.debug("No space available")
                    break
    
                self.get_template()
                self.prepare_question()
                new_rect = self.get_question_area()
                
                if self.rect_fits_in_current_frame(new_rect):
                    self.set_measure_only_mode(False)
                    logging.info("Rendering %s to %s", self.current_question.type, 
                             self.current_question.bounds)
                    self.current_question.render(self.draw)
                    self.add_detection_frame(self.current_question.frame)
                    return new_rect
                else :
                    logging.info("Could not render %s, %s into %s", self.current_question.type, 
                             self.current_question.bounds, self.area_for_next_question.size)                    

            except BoundsError as e :
                # Ran out of space
                logging.info("Ran out of space %s %s %s", self.current_question.type, 
                             self.current_question.bounds.size,
                             self.area_for_next_question.size)
            
    def get_area_for_next_question(self) :
        self.area_for_next_question = None
        rect = self.get_current_write_location()
        if rect is None:
            return

        self.area_for_next_question = Bounds(rect[0][0], rect[0][1], 
                        x2 = rect[1][0], y2 = rect[1][1])         
        
    def get_template(self) :
        name = self.options.get("template")
        if name :
            self.current_question = self.factory.create_question_from_template(name)           
        else :
            self.current_question = self.factory.create_question_from_random_template()
            
        logging.info("Current template is '%s'", self.current_question.type)
    
    def prepare_question(self) :
        self.current_question.update_page_parameters(self)
        self.current_question.set_numerator(self._numerator)
        self.current_question.calculate_dimensions(self.draw, 
                                                   self.area_for_next_question.size)
        self.current_question.layout(self.area_for_next_question)       
        
    def get_question_area(self) :
        return self.current_question.bounds.rectangle
    
    def __create_numerator(self) :
        numerator_parameters = {
            "probability" : 0.97,
            "style" : {
                "0" : [[0.9, "decimal"], [1.0, "letter"]],
                "1" : ["roman", "letter", "decimal"]
            }
        }
        
        parser = ParameterParser(numerator_parameters)
        if not parser.realize_parameter("probability", True) :
            return
        
        self._numerator = Numerator(numerator_parameters, self.current_question_number)    


    
    
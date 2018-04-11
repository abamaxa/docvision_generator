import logging

from graphics import Bounds, BoundsError
from .page import Page
from .fragment_factory import FragmentFactory
from page_fragments import ParameterParser, Numerator

class FragmentPage(Page) :
    def __init__(self, name, options, persister):
        super().__init__(name, options, persister)
        self.factory = FragmentFactory()
        self.current_fragment = None
        self.area_for_next_fragment = None
        self._numerator = None
        self.__create_numerator()
        self.attempts = 0
                      
    def create_fragment(self) :            
        for self.attempts in range(4) :
            try :
                self.get_area_for_next_fragment()
                if self.area_for_next_fragment is None:
                    logging.debug("No space available")
                    break
    
                self.get_template()
                self.prepare_fragment()
                new_rect = self.get_fragment_area()
                
                if self.rect_fits_in_current_frame(new_rect):
                    self.set_measure_only_mode(False)
                    logging.info("Rendering %s to %s", self.current_fragment.type, 
                             self.current_fragment.bounds)
                    self.current_fragment.render(self.draw)
                    self.add_detection_frame(self.current_fragment.frame)
                    return new_rect
                else :
                    logging.info("Could not render %s, %s into %s", self.current_fragment.type, 
                             self.current_fragment.bounds, self.area_for_next_fragment.size)                    

            except BoundsError as e :
                # Ran out of space
                logging.info("Ran out of space %s %s %s", self.current_fragment.type, 
                             self.current_fragment.bounds.size,
                             self.area_for_next_fragment.size)
            
    def get_area_for_next_fragment(self) :
        self.area_for_next_fragment = None
        rect = self.get_current_write_location()
        if rect is None:
            return

        self.area_for_next_fragment = Bounds(rect[0][0], rect[0][1], 
                        x2 = rect[1][0], y2 = rect[1][1])         
        
    def get_template(self) :
        if self.attempts >= 2 :
            name = "paragraph"
        else :
            name = self.options.get("template")
            
        if name :
            self.current_fragment = self.factory.create_fragment_from_template(name)           
        else :
            self.current_fragment = self.factory.create_fragment_from_random_template()
            
        logging.info("Current template is '%s'", self.current_fragment.type)
    
    def prepare_fragment(self) :
        self.current_fragment.update_page_parameters(self)
        self.current_fragment.set_numerator(self._numerator)
        self.current_fragment.calculate_dimensions(self.draw, 
                                                   self.area_for_next_fragment.size)
        self.current_fragment.layout(self.area_for_next_fragment)       
        
    def get_fragment_area(self) :
        return self.current_fragment.bounds.rectangle
    
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
        
        self._numerator = Numerator(numerator_parameters, self.current_fragment_number)    


    
    
from .drawable import Drawable
from .text import Text
from .line import HorizontalLine
from .parameter_parser import ParameterParser

class Container(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self._children = []
        self.create_children(parameters)

    def create_children(self, parameters) :
        for element in parameters.get("elements", []) :
            self.__create_elements(element)   
            
    def __create_elements(self, element) :
        parser = ParameterParser(element)
        class_name = parser.realize_parameter("class")
        if not class_name :
            raise ValueError("Elements must specify a class") 
        
        klass = globals()[class_name]
        for _ in range(self.__number_of_elements_to_create(parser)) :
            self._children.append(klass(element))             
            
    def __number_of_elements_to_create(self, parser) :
        if not parser.realize_parameter("probability", True) :
            return 0
        
        return parser.realize_parameter("repeat", 1)
      
    def update_page_parameters(self, page) :
        super().update_page_parameters(page)
        for child in self._children :
            child.update_page_parameters(page)         
            
    def calculate_dimensions(self, draw, bounds) :
        super().calculate_dimensions(draw, bounds)
        for child in self._children :
            child.calculate_dimensions(draw, bounds)   
    
    def layout(self, bounds) :
        super().layout(bounds)
        y = self.bounds.y
        bounds = self.bounds
        for child in self._children :
            child.layout(bounds)   
            bounds = child.bounds.move(0, child.bounds.height)
                
    def render(self, draw) :
        super().render(draw)
        for child in self._children :
            child.render(draw)    

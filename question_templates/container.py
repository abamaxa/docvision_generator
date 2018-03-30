from .drawable import Drawable
from .text import Text
from .line import HorizontalLine
from .parameter_parser import ParameterParser
from .formula import Formula
from .graph import Graph
from .diagram import Diagram
from .layout import VerticalLayout, GridLayout

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
        layout_policy = self.__get_layout_policy(bounds)
        max_child_size = layout_policy.get_max_child_size()
        for child in self._children :
            child.calculate_dimensions(draw, max_child_size) 
            
        super().calculate_dimensions(draw, bounds)
    
    def layout(self, bounds) :
        super().layout(bounds)
        layout_policy = self.__get_layout_policy(bounds)
        layout_policy.layout(self._children)
                
    def render(self, draw) :
        super().render(draw)
        for child in self._children :
            child.render(draw)    
            
    def __get_layout_policy(self, parent_bounds) :
        policy_params = self.parameters.get("layout")
        if policy_params :
            parser = ParameterParser(policy_params)
            class_name = parser.realize_parameter("class")  
            klass = globals()[class_name]
            values = parser.realize_as_dict()
            return klass(parent_bounds, **values)
        
        else :
            return VerticalLayout(parent_bounds)
            
            

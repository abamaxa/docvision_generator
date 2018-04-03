from .drawable import Drawable
from .text import Text
from .line import HorizontalLine
from .parameter_parser import ParameterParser
from .formula import Formula
from .graph import Graph
from .diagram import Diagram
from .layout import VerticalLayout, GridLayout

from graphics import Bounds, Size

class Container(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self._children = [] 
        self.column_width = 0
        self.create_children(parameters)
        
    def get_content_size(self) :
        if self._children :
            layout_policy = self.__get_layout_policy(self.inner_bounds)
            return layout_policy.get_content_size()    
        else :
            return super().get_content_size()
    
    def create_children(self, parameters) :
        for element in parameters.get("elements", []) :
            self.__create_elements(element)   
            
    def __create_elements(self, element) :
        parser = ParameterParser(element)
        class_name = parser.realize_parameter("class")
        if not class_name :
            raise ValueError("Elements must specify a class") 
        
        if self.__skip_element(parser) :
            return
        
        klass = globals()[class_name]
        primary_element = klass(element)
        self._children.append(primary_element)
        
        for _ in range(self.__number_of_extra_elements_to_create(parser)) :
            new_element = klass(element)
            new_element.set_primary_element(primary_element)
            self._children.append(new_element)  
            
    def __skip_element(self, parser) :
        return not parser.realize_parameter("probability", True)
            
    def __number_of_extra_elements_to_create(self, parser) :
        return parser.realize_parameter("repeat", 0)
      
    def update_page_parameters(self, page) :
        for child in self._children :
            child.update_page_parameters(page)   
            
        super().update_page_parameters(page)
            
    def calculate_dimensions(self, draw, size) : 
        inner_size = self.calculate_content_from_size(size)
        layout_policy = self.__get_layout_policy(inner_size)
        max_child_size = layout_policy.get_max_child_size()
        for child in self._children :
            child.calculate_dimensions(draw, max_child_size) 
            
        super().calculate_dimensions(draw, size)
    
    def layout(self, bounds) :
        super().layout(bounds)
        layout_policy = self.__get_layout_policy(self.inner_bounds)
        layout_policy.layout()
        size = layout_policy.get_content_size()
        outer_size = self.calculate_size_from_inner_size(size)
        self._bounds = Bounds(bounds.x, bounds.y, bounds.width, outer_size.height)
                
    def render(self, draw) :
        super().render(draw)
        for child in self._children :
            child.render(draw)    
            
    def set_numerator(self, numerator) :
        for child in self._children :
            child.set_numerator(numerator)
            
    def __get_layout_policy(self, parent_bounds) :
        policy_params = self.parameters.get("layout")
        if policy_params :
            parser = ParameterParser(policy_params)
            class_name = parser.realize_parameter("class")  
            klass = globals()[class_name]
            values = parser.realize_as_dict()
            return klass(parent_bounds, self._children, **values)
        
        else :
            return VerticalLayout(parent_bounds, self._children)
            
            

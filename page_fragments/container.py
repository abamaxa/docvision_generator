from .drawable import Drawable
from .text import Text
from .line import HorizontalLine
from .parameter_parser import ParameterParser, ParameterError
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
        self.layout_policy = self.__get_layout_policy(Bounds(0,0,
                                                             Drawable.FILL_PARENT,
                                                             Drawable.FILL_PARENT))
        self.create_children(parameters)
        
    def get_element_size(self) :
        if self._children :
            self.layout_policy.update_bounds(self.inner_bounds)
            return self.layout_policy.get_element_size()    
        else :
            return super().get_element_size()
    
    def create_children(self, parameters) :
        for element in parameters.get("elements", []) :
            self.__create_elements(element)   
            
    def __create_elements(self, element) :
        parser = ParameterParser(element)
        class_name = parser.realize_parameter("class")
        if not class_name :
            raise ParameterError("Elements must specify a class") 
        
        if self.__skip_element(parser) :
            return
        
        klass = globals()[class_name]
        primary_element = None
        
        for _ in range(self.__number_of_elements_to_create(parser)) :
            new_element = klass(element)
            if primary_element :
                new_element.primary_element = primary_element
            else :
                primary_element = new_element
                
            self._children.append(new_element)  
            
    def __skip_element(self, parser) :
        return not parser.realize_parameter("probability", True)
            
    def __number_of_elements_to_create(self, parser) :
        rows = 1 + parser.realize_parameter("repeat", 0)
        return self.layout_policy.columns * rows
      
    def update_page_parameters(self, page) :
        for child in self._children :
            child.update_page_parameters(page)   
            
        super().update_page_parameters(page)
            
    def calculate_dimensions(self, draw, size) : 
        inner_size = self._calculate_content_from_size(size)
        self.layout_policy.update_bounds(inner_size)
        max_child_size = self.layout_policy.get_max_child_size()
        for child in self._children :
            child.calculate_dimensions(draw, max_child_size) 
            
        super().calculate_dimensions(draw, size)
    
    def layout(self, bounds) :
        super().layout(bounds)
        self.layout_policy.update_bounds(self.inner_bounds)
        self.layout_policy.layout()
        size = self.layout_policy.get_element_size()
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
            
            

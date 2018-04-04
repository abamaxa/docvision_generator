import random

from graphics import Bounds, Size, Origin
from .parameter_parser import ParameterParser, ParameterError
from .abstract_drawable import AbstractDrawable
from .numerator import SectionNumber
from .spacing_parser import SpacingParser

class Drawable(AbstractDrawable) :
    FILL_PARENT = 0
    
    def __init__(self, parameters) :
        self._parameters = parameters
        self._bounds = Bounds()
        
        self._margin_left = 0
        self._margin_top = 0
        self._margin_right = 0
        self._margin_bottom = 0
        
        self._padding_left = 0
        self._padding_top = 0
        self._padding_right = 0
        self._padding_bottom = 0
                
        self._border_style = None
        self._border_width = 1  
        self._border_color = None
        
        self._foreground_color = None
        self._background_color = None
        
        self._section_number = None
        self._primary_element = None
        
    @property
    def parameters(self) :  return self._parameters
                
    @property
    def origin(self) :  return self.bounds.origin
    
    @property
    def size(self) :  return self.bounds.size
    
    def get_bounds(self) :  return self._bounds
    def set_bounds(self, new_bounds) :  self._bounds = new_bounds
    bounds = property(get_bounds, set_bounds)
    
    def __set_primary_element(self, element) : self._primary_element = element
    def __get_primary_element(self) : return self._primary_element
    primary_element = property(__get_primary_element, __set_primary_element)    
        
    @property
    def border_bounds(self) :
        if self._has_border() :
            return Bounds(self._bounds.x + self._margin_left,
                          self._bounds.y + self._margin_top,
                          x2 = self._bounds.x2 - self._margin_right,
                          y2 = self._bounds.y2 - self._margin_bottom)    
        
    def _has_border(self) :
        return not self._border_style is None    
        
    @property
    def inner_bounds(self) :
        size = self._calculate_content_from_size(self._bounds.size)
        left = self._bounds.x + self._margin_left
        left += self._padding_left + self.get_section_number_width()
        top = self._bounds.y + self._margin_top + self._padding_top
        
        return Bounds(left, top, size.width, size.height)   
    
    def _calculate_content_from_size(self, size) :
        dx = self._margin_left + self._padding_left + self._margin_right + self._padding_right
        dx += self.get_section_number_width()
        dy = self._margin_top + self._padding_top + self._margin_bottom + self._padding_bottom
        return Size(size.width - dx, size.height - dy)
    
    def calculate_size_from_inner_size(self, size) :
        dy = self._margin_top + self._padding_top + self._margin_bottom + self._padding_bottom
        dx = self._margin_left + self._padding_left + self._margin_right + self._padding_right
        dx += self.get_section_number_width()        
        return Size(size.width + dx, size.height + dy)  
        
    def set_numerator(self, numerator) :
        self._section_number = SectionNumber(self, numerator)
        
    def get_section_number_width(self) :
        if self._section_number :
            return self._section_number.get_width()
        return 0
            
    def update_page_parameters(self, page) :
        self.update_border(page)
        self.update_margins(page)
        self.update_padding(page)
        self.update_colors(page) 
                        
    def update_border(self, page) :
        border_dict = self.parameters.get("border")
        if not border_dict :
            return
        
        parser = ParameterParser(border_dict)
        if parser.realize_parameter("probability") :
            self._border_style = parser.realize_parameter("style", 1)
            self._border_width = parser.realize_parameter("width", 1)
    
    def update_margins(self, page) : 
        spacer = SpacingParser("margin", self, page)
        spacer.set_property_values()
        
    def update_padding(self, page) : 
        spacer = SpacingParser("padding", self, page)
        spacer.set_property_values()
      
    def update_colors(self, page) :
        self._foreground_color = self.realize_parameter("text_color", page.parameters.text_color)
        self._background_color = page.parameters.fake_background_color
        self._border_color = self.realize_parameter("border_color", page.parameters.border_color)  
            
    def calculate_dimensions(self, draw, size) :
        self._bounds = Bounds(0, 0, size.width, size.height)
        self.update_bounds()  
        
    def update_bounds(self) :
        content_size = self.get_element_size()
        if content_size.width != Drawable.FILL_PARENT :
            new_width = content_size.width
        else :
            new_width = self.bounds.width
            
        if content_size.height != Drawable.FILL_PARENT :
            new_height = content_size.height
        else :
            new_height = self.bounds.height   
            
        self.bounds = self.bounds.resize(new_width, new_height)    
        
    def get_element_size(self) :
        return Size(Drawable.FILL_PARENT, Drawable.FILL_PARENT)    
        
    def render(self, draw) :
        if self._has_border() :
            draw.draw_line(self.border_bounds, color=self._border_color)
        if self._section_number :
            self._section_number.render(draw)
                    
    def layout(self, bounds) :
        self._bounds = Bounds(bounds.x, bounds.y, bounds.width, self._bounds.height)       
            
    def realize_required_parameter(self, parameter_name, default = None) :
        if not parameter_name in self.parameters :
            msg = "class '{}' requires missing parameter '{}'".format(
                self.parameters.get("class"), parameter_name)
            raise ParameterError(msg)
        return self.realize_parameter(parameter_name, default)    
            
    def realize_parameter(self, parameter_name, default = None) :
        parser = ParameterParser(self.parameters)
        return parser.realize_parameter(parameter_name, default)
    
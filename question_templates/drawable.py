import random
from abc import ABC, abstractmethod

from graphics import Bounds, Size, Origin, 

class Drawable(ABC) :
    FILL_PARENT = -1
    
    def __init__(self, parameters) :
        self._parameters = parameters
        self._bounds = Bounds()
        self._left_margin = 0
        self._top_margin = 0
        self._right_margin = 0
        self._bottom_margin = 0
        
        self._left_padding = 0
        self._top_padding = 0
        self._right_padding = 0
        self._bottom_padding = 0
        
        self._border_style = None
        self._border_width = 1
        
        self._border_color = None
        self._foreground_color = None
        self._background_color = None
        
    def update_page_parameters(self, page) :
        self.update_border(page)
        self.update_margins_and_padding_for_border(page)
        self.update_colors(page)
    
    @abstractmethod
    def get_content_size(self) :
        return Size(FILL_PARENT, FILL_PARENT)
    
    @abstractmethod
    def calculate_dimensions(self, draw, bounds) :
        pass
    
    @abstractmethod
    def render(self, draw) :
        if self.__has_border() :
            draw.draw_line(self.border_bounds, outline = self._border_color)

    def layout(self, bounds) :
        self.bounds.move_to(bounds.x, bounds.y)    
        
    @property
    def border_bounds(self) :
        if self.__has_border() :
            return Bounds(bounds.x + self._margin_left,
                          bounds.y + self._margin_top,
                          x2 = bounds.x2 - self._margin_right,
                          y2 = bounds.y2 - self._margin_bottom)      
        
    @property
    def inner_bounds(self) :
        return Bounds(bounds.x + self._margin_left + self._padding_left,
                      bounds.y + self._margin_top + self._margin_top,
                      x2 = bounds.x2 - self._margin_right + self._padding_right,
                      y2 = bounds.y2 - self._margin_bottom + self._padding_bottom)       
        
    @property
    def parameters(self) :
        return self._parameters
                
    def get_bounds(self) :
        return self._bounds
    
    def set_bounds(self, new_bounds) :
        self._bounds = new_bounds
        
    bounds = property(get_bounds, set_bounds)
    
    @property
    def origin(self) :
        return self.bounds.origin
    
    @property
    def size(self) :
        return self.bounds.size
    
    def update_border(self, page) :
        border_dict = self.parameters.get("border")
        if border_dict :
            parser = ParameterParser(border_dict)
            self._border_style = parser.realize_parameter("style", 1)
            self._border_width = parser.realize_parameter("width", 1)
            
    def __has_border(self) :
        return not self._border_style is None
    
    def update_margins(self, page) :
        self._margin_left = 0
        self._margin_right = 0
        self._margin_top = 0
        self._margin_bottom = 0
                    
    def update_padding(self, page) :
        self._padding_left = 0
        self._padding_right = 0
        self._padding_top = 0
        self._padding_bottom = 0

    def update_colors(self, page) :
        self._foreground_color = page.parameters.text_color
        self._background_color = page.parameters.fake_background_color
        self._border_color = page.parameters.border_color

    def height(self) :
        return size.height
    
    def __width_of_all_padding_and_margins(self) :
        return self._margin_left + self._padding_left \
               + self._padding_right + self._margin_right
    
    def __height_of_all_padding_and_margins(self) :
        return self._margin_top + self._padding_top \
               + self._padding_bottom + self._margin_bottom    
    
    def update_bounds(self) :
        content_size = self.get_content_size()
        if content_size.width != Drawable.FILL_PARENT :
            new_width = content_size.width + self.__width_of_all_padding_and_margins()
        else :
            new_width = self.bounds.width
            
        if content_size.height != Drawable.FILL_PARENT :
            new_height = content_size.height + self.__height_of_all_padding_and_margins()
        else :
            new_height = self.bounds.height        
            
    def realize_parameter(self, parameter_name, default = None) :
        parser = ParameterParser(self.parameters)
        return parser.realize_parameter(parameter_name, default)
        

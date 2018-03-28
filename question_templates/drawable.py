import random

from graphics import Bounds, Size, Origin
from .parameter_parser import ParameterParser
from .abstract_drawable import AbstractDrawable

class Drawable(AbstractDrawable) :
    FILL_PARENT = -1
    
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
        
    def update_page_parameters(self, page) :
        self.update_border(page)
        self.update_margins(page)
        self.update_padding(page)
        self.update_colors(page)
    
    def get_content_size(self) :
        return Size(FILL_PARENT, FILL_PARENT)
    
    def calculate_dimensions(self, draw, bounds) :
        self._bounds = bounds
    
    def render(self, draw) :
        if self._has_border() :
            draw.draw_line(self.border_bounds, outline = self._border_color)

    def layout(self, bounds) :
        self._bounds = self._bounds.move_to(bounds.x, bounds.y)    
        
    @property
    def border_bounds(self) :
        if self._has_border() :
            return Bounds(self._bounds.x + self._margin_left,
                          self._bounds.y + self._margin_top,
                          x2 = self._bounds.x2 - self._margin_right,
                          y2 = self._bounds.y2 - self._margin_bottom)      
        
    @property
    def inner_bounds(self) :
        return Bounds(self._bounds.x + self._margin_left + self._padding_left,
                      self._bounds.y + self._margin_top + self._padding_top,
                      x2 = self._bounds.x2 - self._margin_right - self._padding_right,
                      y2 = self._bounds.y2 - self._margin_bottom - self._padding_bottom)       
        
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
        if not border_dict :
            return
        
        parser = ParameterParser(border_dict)
        if parser.realize_parameter("probability") :
            self._border_style = parser.realize_parameter("style", 1)
            self._border_width = parser.realize_parameter("width", 1)
            
    def _has_border(self) :
        return not self._border_style is None
    
    def update_margins(self, page) :
        default = page.parameters.margins
        self.__assign_side_attribute_group("margin", default)
        
    def update_padding(self, page) :
        default = page.parameters.padding
        self.__assign_side_attribute_group("padding", default)
            
    def __assign_side_attribute_group(self, group_name, default) :
        # TODO Multiples of line height / fraction of column width?
        default = self.realize_parameter(group_name, default)

        for name in ("left", "top", "right", "bottom") :
            param_name = group_name + "_" + name
            value = self.realize_parameter(param_name, 1)
            setattr(self, "_" + param_name, default * value)

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
            
        self.bounds = self.bounds.resize(new_width, new_height)
            
    def realize_parameter(self, parameter_name, default = None) :
        parser = ParameterParser(self.parameters)
        return parser.realize_parameter(parameter_name, default)
        

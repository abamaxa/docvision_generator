import random
from abc import ABC, abstractmethod

from .bounds import *

class Drawable(ABC) :
    def __init__(self, parameters) :
        self._parameters = parameters
        self._bounds = Bounds()
        self._margin = None
        self._padding = None
        self._border = False
        
    @abstractmethod
    def update_page_parameters(self, page) :
        pass
    
    @abstractmethod
    def calculate_dimensions(self, draw, bounds) :
        pass
    
    @abstractmethod
    def layout(self, bounds) :
        pass
    
    @abstractmethod
    def render(self, draw) :
        pass    
        
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
    
    @property
    def border(self) :
        return self._border
    
    def format(self, page) :
        print("Drawable.set_page_parameters")
        padding = page.params.padding
        if self.border :
            self._margin = Size(padding.width / 2, padding.height / 2)
            self._padding = self.margin            
        else :
            self._margin = Size(0,0)
            self._padding = padding

    def height(self) :
        return size.height
                
    def realize_parameter(self, parameter_name) :
        if not parameter_name in self.parameters :
            return None
        
        value = self.parameters[parameter_name]
        if self.is_probability(name) :
            return self.true_or_false(value)
        
        elif self.is_probability_list(value) :
            return pick_from_list(value)
        
        elif isinstance(value, list) :
            return random.choice(value)
        
        elif isinstance(value, dict) :
            rand_value = random.randint(value.get("min"), value.get("max"))
            return rand_value * value.get("scale", 1)
        
        else :
            return value
        
    def is_probability_list(self, value) :
        return isinstance(value, list) and isinstance(value[0], list) and \
               len(value[0]) == 2 and  isinstance(value[0][0], float)
    
    def is_probability(self, name) :
        return name.endswith("_probability")
    
    def true_or_false(self, value):
        return random.random() < value
        

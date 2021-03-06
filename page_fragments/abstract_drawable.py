from abc import ABC, abstractmethod

class AbstractDrawable(ABC) :
    @abstractmethod
    def get_element_size(self) :
        pass
    
    @abstractmethod
    def calculate_dimensions(self, draw, size) :
        pass
    
    @abstractmethod
    def render(self, draw) :    
        pass
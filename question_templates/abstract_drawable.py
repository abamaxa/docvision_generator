from abc import ABC, abstractmethod

class AbstractDrawable(ABC) :
    @abstractmethod
    def get_content_size(self) :
        pass
    
    @abstractmethod
    def calculate_dimensions(self, draw, bounds) :
        pass
    
    @abstractmethod
    def render(self, draw) :    
        pass
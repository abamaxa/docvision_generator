from .drawable import Drawable
from .text import Text
from .line import Line

class Container(Drawable) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self._children = []
        self.create_children(parameters)

    def create_children(self, parameters) :
        for element in parameters.get("elements", []) :
            klass = globals()[element["class"]]
            instance = klass(element)
            self._children.append(instance)   
            
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

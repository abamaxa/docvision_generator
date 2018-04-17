import random

from .text import Text
from .drawable import Drawable
from graphics import Bounds, Size, Origin, TextRenderer, Formula

# Maybe better to segment this into multiple lines
class MathText(Text) :
    def __init__(self, parameters) :
        super().__init__(parameters)
        self.formula = None
        self.image = None
        self.text_size = None
        self.text_y = 0
                 
    def update_page_parameters(self, page) :
        super().update_page_parameters(page)
        self.__get_formulas(page)
        
    def calculate_dimensions(self, draw, size) :
        self._bounds = Bounds(0, 0, size.width, size.height)
        self.text_size = draw.text_size(self.text + "  ")  
        
        formula_size = self.image.size
        
        while self.text and self.text_size[0] + formula_size[0] > self.inner_bounds.width :
            self.text = " ".join(self.text.split(' ')[:-2])
            self.text_size = draw.text_size(self.text + "  ")  
        
        if formula_size[1] > self.text_size[1] :
            self.text_height = formula_size[1]
            self.text_y = ((formula_size[1] - self.text_size[1]) // 2 - 1)
        else :
            self.text_height = self.text_size[1]
            self.text_y = 0            
        
        super().update_bounds()

    def render(self, draw) :
        Drawable.render(self, draw)
        inner_bounds = self.inner_bounds
        
        text_position = (inner_bounds.x, inner_bounds.y + self.text_y)
        draw.draw_text_line(text_position, self.text + "  ")
        
        image_bounds = Origin(inner_bounds.x + self.text_size[0], inner_bounds.y)
        draw.blit(self.image, (int(image_bounds.x),int(image_bounds.y)))       
                
    def _set_text(self, page) :
        super()._set_text(page)
        
    def __get_formulas(self, page) :
        self.formula = Formula(page.parameters.font_size)
        if random.random() < 0.5 :
            self.formula.generate_matrix()
        else :
            self.formula.generate_intergral()            
                        
        self.image = self.formula.image
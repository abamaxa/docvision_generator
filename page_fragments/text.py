import random

from .drawable import Drawable
from graphics import Bounds, Size, TextRenderer

# Maybe better to segment this into multiple lines
class Text(Drawable) :
    def __init__(self, parameters) :
        Drawable.__init__(self, parameters)
        self.text = ""
        self.align = None
        self.text_height = 0
        self.color = None
        self.text_render= None
        self.end_text = None
                 
    def update_page_parameters(self, page) :
        super().update_page_parameters(page)
        if self.primary_element :
            pass
        else :
            self.align = self.realize_parameter("align", page.parameters.text_align)
            
        self._set_text(page)
        self.color = page.parameters.text_color
        
    def get_element_size(self) :  
        size = self.calculate_size_from_inner_size(Size(Drawable.FILL_PARENT, self.text_height))
        return Size(Drawable.FILL_PARENT, size.height)
        
    def calculate_dimensions(self, draw, size) :
        self._bounds = Bounds(0, 0, size.width, size.height)
        self.text_render = TextRenderer(draw, self.text, self.color, 
                                        self.align, end_text = self.end_text) 
        self.text_height = self.text_render.calculate_text_height(self.inner_bounds)      
        super().update_bounds()
        
    def render(self, draw) :
        super().render(draw)
        self.text_render.draw_text(self.inner_bounds)
        
    def _set_text(self, page) :
        num_words = self.realize_parameter("words")
        if num_words :
            self.text = page.get_words(num_words)
        else :
            num_sentences = self.realize_parameter("sentences")
            self.text = page.get_sentences(num_sentences)

        self._set_end_text(page)
        
    def _set_end_text(self, page) :
        if not page.parameters.end_text or not self.get_section_number_width() :
            return
        
        self._generate_end_text()        

    def _generate_end_text(self) :
        self.end_text = "[{}]".format(random.randint(1,3))
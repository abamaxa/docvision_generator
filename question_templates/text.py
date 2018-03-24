from .drawable import Drawable

# Maybe better to segment this into multiple lines
class Text(Drawable) :
    def __init__(self, parameters) :
        Drawable.__init__(self, parameters)
        self.text = ""
        self.text_bounds = Bounds()
        
    def update_page_parameters(self, page) :
        Drawable.format(self, page)
        self.__set_text(page)
        
    def calculate_dimensions(self, draw, bounds) :
        # So, we don't need the origin at this satge, only the width
        height = draw.calculate_text_height(self.bounds.width, self.text, self.align)   
        # once we have width and height, we can position the element within the 
        # available space
                                
    def layout(self, bounds) :
        pass    
        
    def render(self, draw) :
        super().render(self, draw)
        draw.line(self.origin, self.size)    
        
    def __set_text(self, page) :
        num_words = self.realize_parameter("words")
        if num_words :
            self.text = page.get_words(num_words)
        else :
            num_sentences = self.realize_parameter("sentences")
            self.text = page.get_sentences(num_sentences)
            
        draw = page.draw
                
    def get_height(self) :
        return 
        

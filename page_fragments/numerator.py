import random

from page_generator import ParameterParser

ROMAN_DIGITS = ["i", "ii", "iii", "iv", "v","vi", "vii", "vii",
    "ix", "x", "xi""xii", "xii", "xi",  "xv"]

class Numerator :
    def __init__(self, parameters, question_number) :
        self._styles = {}
        
        parser = ParameterParser(parameters)
        self._start_number = question_number
        self._bold = parser.realize_parameter("probability_bold")
        self._circles = parser.realize_parameter("probability_circles")
        self._current_level = 0
        self._sublevel_numbers = {}
        self.scale = (0.75 + (0.5 * random.random()))
        
        self.__create_styles(parameters)
        self.reset()
       
    @property
    def bold(self) : return self._bold
    
    @property
    def circles(self) : return self._circles    
       
    def __create_styles(self, parameters) :
        parser = ParameterParser(parameters["style"])
        for level in parameters["style"].keys() :
            self._styles[level] = parser.realize_parameter(level)
            
    def reset(self) :
        self._current_level = 0
        self._sublevel_numbers = {0 : self._start_number}
        
    def get_next_number(self, level = 0) :
        self._current_level = level
        self.__remove_lower_levels()
        
        number = self._sublevel_numbers.get(self._current_level, 1)
        self._sublevel_numbers[self._current_level] = number + 1
        
        return self.__get_number_for_style(number)
            
    def __remove_lower_levels(self) :
        lower_level = self._current_level + 1
        if lower_level in self._sublevel_numbers.keys() :
            del self._sublevel_numbers[lower_level]
            
    def __get_number_for_style(self, number) :
        style = self.get_current_style()
        
        if style == "decimal" :
            return str(number)
        elif style == "roman" :
            return ROMAN_DIGITS[number % len(ROMAN_DIGITS)]
        elif style == "letter" :
            if self._current_level :
                return chr(96 + number)
            else :
                return chr(64 + number)
            
    def get_current_style(self) :
        style = self._styles.get(str(self._current_level))
        if not style :
            style = random.choice(("letter", "roman", "decimal"))
            self._styles[str(self._current_level)] = style
            
        return style
       
class SectionNumber :
    def __init__(self, drawable, numerator) :
        self._numerator = numerator
        self._drawable = drawable
        self._style = self._level = self._number = None
    
        if self._numerator :
            default = None
            if "numerator" in drawable.parameters :
                default = 0
                
            self._level = drawable.get_number_level(default)  
            
        if not self._level is None :
            self._number = numerator.get_next_number(self._level)  
            self._style = numerator.get_current_style()  
            
    def get_width(self) :
        if not self._level :
            return 0
        else :
            width = int(self.default_width() * self._numerator.scale * self._level)
            #print(self._level, self.default_width(), width)
            return width
    
    def default_width(self) :
        return 25
        
    def render(self, draw) :
        if not self._numerator or not self._number :
            return
        
        number_length = draw.text_size(self._number + "  ")
        inner_bounds = self._drawable.inner_bounds
        pos = (inner_bounds.x - number_length[0], inner_bounds.y)
        
        #width = self.get_width()
        #pos = (inner_bounds.x - int(width * 0.75), inner_bounds.y)
        
        if self._level == 0 and self._numerator.circles :
            draw.draw_question_circle(pos)
            draw.draw_text_line(pos, self._number)
            
        else :
            draw.draw_bold_text_line(pos, self._number)
            
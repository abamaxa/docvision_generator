import random

from graphics import Size
from .parameter_parser import ParameterParser

ROMAN_DIGITS = ["i", "ii", "iii", "iv", "v","vi", "vii", "viii",
    "ix", "x", "xi""xii", "xiii", "xiv",  "xv"]

class Numerator :
    def __init__(self, parameters) :
       self._styles = {}
       
       parser = ParameterParser(parameters)
       default_start = random.randint(1,10)
       self._start_number = parser.realize_parameter("start", default_start)
       self._bold = parser.realize_parameter("probability_bold")
       self._circles = parser.realize_parameter("probability_circles")
       self._current_level = 0
       self._sublevel_numbers = {}
       
       self.__create_styles(parameters)
       self.reset()
       
    @property
    def bold(self) : return self._bold
    
    @property
    def circles(self) : return self._circles    
       
    def __create_styles(self, parameters) :
        for level in range(len(parameters["style"])) :
            level_style = parameters["style"][level] 
            self._styles[level] = random.choice(level_style)
            
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
        style = self.__get_current_style()
        
        if style == "decimal" :
            return str(number)
        elif style == "roman" :
            return ROMAN_DIGITS[number % len(ROMAN_DIGITS)]
        elif style == "letter" :
            if self._current_level :
                return chr(96 + number)
            else :
                return chr(64 + number)
            
    def __get_current_style(self) :
        style = self._styles.get(self._current_level)
        if not style :
            style = random.choice(("letter", "roman", "decimal"))
            
        return style
       
class SectionNumber :
    def __init__(self, drawable, numerator) :
        self._numerator = numerator
        self._drawable = drawable
        self._level = self._number = None
    
        if self._numerator :
            default = None
            if "numerator" in drawable.parameters :
                default = 0
                
            self._level = drawable.realize_parameter("number_level", default)  
            
        if not self._level is None :
            self._number = numerator.get_next_number(self._level)            
    
    def render(self, draw) :
        if not self._numerator or not self._number :
            return
        
        number_length = draw.text_size(self._number + "  ")
        
        inner_bounds = self._drawable.inner_bounds
        pos = (inner_bounds.x - number_length[0], inner_bounds.y)
        
        if self._level == 0 and self._numerator.circles :
            draw_question_circle(pos)
        
        if self._numerator.bold :
            draw.draw_bold_text_line(pos, self._number)
        else :
            draw.draw_text_line(pos, self._number)
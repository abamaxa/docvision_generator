class TextRender :
    def __init__(self, draw, text, text_color, align=AlignLeft) :
        self.draw = draw
        self.text = text
        self.align = align
        self.text_color = text_color
        self.total_height = 0
        self.first_line_offset = 0
        self.words = text.split(' ')
        self.width = 0
        self.render_list = []
        self.counter = 0
        
    def calculate_text_height(self, bounds) :
        try :
            initial_mode = self.draw.get_measure_only_mode()
            self.draw.set_measure_only_mode(True)
            return draw_text(bounds)
        
        finally :
            self.draw.set_measure_only_mode(initial_mode)
            
    def reset_state(self) :
        self.__clear_render_list()
        self.counter = 0
        self.total_height = 0 
        self.width = 0
        
    def get_height(self) :
        return self.total_height

    def draw_text(self, bounds) :
        self.reset_state()
        self.width = bounds.width

        for word in self.words:
            self.counter += 1
            self.__add_word_and_render_line_if_fits(word, bounds)

    def __add_word_and_render_line_if_fits(self, word, bounds) :
        test_text = " ".join(self.render_list + [word])
        text_width, text_height = self.__measure_text_size(test_text)

        if self.__should_render_text(text_width) :
            if self.__is_room_on_line_for_word(text_width):
                self.__add_word_to_render_list(word)
            
            self.__render_line(bounds)

            line_height = self.__calculate_total_line_height(text_height)
            bounds = bounds.offset(0, line_height)
            self.total_height += line_height

            self.__clear_render_list()        
            if self.__last_word_not_rendered(text_width):
                self.__add_word_to_render_list(word)
                self.__render_line(bounds)
                self.total_height += total_line_height

        self.__add_word_to_render_list(word)    
    
    def __get_line_width(self) :
        width = self.width
        if self.__is_first_line() :
            width -= self.first_line_offset
            
        return width
    
    def __is_first_line(self) :
        return self.total_height == 0
    
    def __should_render_text(self, text_width) :
        return text_width > self.__get_line_width() or self.counter == len(self.words)
                
    def __is_room_on_line_for_word(self, text_width) :
        return text_width <= self.__get_line_width() or not self.render_list
        
    def __add_word_to_render_list(self, word) :
        self.render_list.append(word)
        
    def __clear_render_list(self) :
        self.render_list = []
        
    def __render_list_to_text(self) :
        return " ".join(self.render_list)
    
    def __size_render_list(self) :
        return len(self.render_list)
    
    def __calculate_total_line_height(self, text_height) :
        return int(text_height * self.draw.line_spacing)  
    
    def __last_word_not_rendered(self, text_width) :
        return text_width > self.width and self.counter == len(self.words)
    
    def __render_line(self, bounds):
        line_width = bounds.width
        position = bounds.origin

        write_position = self.__get_aligned_position(position)

        if self.__should_justify_render_list() :
            self.__output_justifed_line(write_position)
        else:
            self.__output_line(write_position, self.__render_list_to_text())    
            
    def __get_aligned_position(self, position) :
        x, y = position
        
        if not self.align in (Draw.AlignLeft, Draw.AlignJustify):
            text = self.__render_list_to_text()
            last_text_width = self.__measure_text_width(text)
            
            if self.align == Draw.AlignRight:
                x += line_width - last_text_width
            elif self.align == Draw.AlignCenter:
                x += (line_width - last_text_width) / 2
                
        return x, y
    
    def __measure_text_size(self, text) :
        width, height = self.draw.text_size(text)
        return width, height     
    
    def __measure_text_width(self, text) :
        return self.__measure_text_size(self, text)[0]
    
    def __should_justify_render_list(self) :
        return self.align == Draw.AlignJustify and self.__size_render_list() > 1
            
    def __output_line(self, position, text) :
        self.draw.draw_text_line(position, text, self.text_color)
            
    def __output_justifed_line(self, position) :   
        word_widths = self.__list_width_words()
        if self.__line_too_short_to_justify(word_width) :
            self.__output_line(position, self.__render_list_to_text())
            return
        
        inter_word_space = self.__calculate_inter_word_space(word_widths)
        line_width = self.__get_line_width()
        
        x, y = position
        count = 0
    
        for word, word_width in zip(self.render_list, word_widths):
            count += 1
            if count == self.__size_render_list() :
                x = position[0] + line_width - word_width
    
            self.draw.__output_line((x, y), word)
    
            x += word_width + inter_word_space
    
    def __calculate_inter_word_space(self, word_widths) :
        return (self.__get_line_width() - sum(word_widths)) / (self.__size_render_list() - 1)
    
    def __line_too_short_to_justify(self, word_widths) :
        return sum(word_widths) < (self.__get_line_width() * 0.6)
            
    def __list_width_words(self) :
        word_widths = []
        for word in self.render_list:
            word_width = self.__measure_text_width(word)
            word_widths.append(word_width)   
            
        return word_widths
            

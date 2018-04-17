class TextRenderer :
    AlignLeft = 0
    AlignRight = 1
    AlignCenter = 2
    AlignJustify = 3
    
    def __init__(
        self, 
        draw, 
        text, 
        text_color, 
        align=AlignLeft, 
        leave_spaces = {},
        end_text = ""
    ) :
        self.__draw = draw
        self.__align = align
        self.__text_color = text_color
        self.__total_height = 0
        self.__first_line_offset = 0
        self.__words = text.split(' ')
        self.__render_list = []
        self.__counter = 0
        self.__bounds = None
        self.__word_lengths = {}
        self.__leave_spaces = leave_spaces
        self.__current_line = 0
        self.__end_text = end_text
        self.__last_line_width = 0
        self.__last_line_height = 0
        
    def calculate_text_height(self, bounds) :
        try :
            initial_mode = self.__draw.measure_only_mode
            self.__draw.measure_only_mode = True
            self.draw_text(bounds)
        
        finally :
            self.__draw.measure_only_mode = initial_mode
            
        return self.get_height()
            
    def reset_state(self) :
        self.__clear_render_list()
        self.__counter = 0
        self.__total_height = 0 
        self.__current_line = 0
        self.__last_line_width = 0
        self.__last_line_height = 0
        
    def get_height(self) :
        return self.__total_height

    def draw_text(self, bounds) :
        self.reset_state()
        self.__bounds = bounds

        for word in self.__words:
            self.__counter += 1
            self.__add_word_and_render_line_if_fits(word)
            
        self.__render_any_remaining_text()
        self.__render_end_markers()

    def __add_word_and_render_line_if_fits(self, word) :
        test_text = " ".join(self.__render_list + [word])
        text_width, text_height = self.__measure_text_size(test_text)

        if self.__should_render_text(text_width) :
            if self.__is_room_on_line_for_word(text_width):
                self.__add_word_to_render_list(word)
                word = ""
            
            self.__render_line()

        if word :
            self.__add_word_to_render_list(word)    
            
    def __render_any_remaining_text(self) :
        if self.__render_list : 
            self.__render_line()
            
    def __update_state_for_next_line(self) :      
        self.__last_line_width, text_height = self.__measure_render_list_size()
        self.__last_line_height = self.__calculate_total_line_height(text_height)
        self.__move_render_positions(self.__last_line_height)
        self.__total_height += self.__last_line_height   
        self.__current_line += 1
        self.__clear_render_list() 
        
    def __move_render_positions(self, yoffset) :
        self.__bounds = self.__bounds.move(0, yoffset)
    
    def __get_line_width(self) :
        width = self.__bounds.width
        if self.__is_first_line() :
            width -= self.__first_line_offset
            
        return width
    
    def __is_first_line(self) :
        return self.__total_height == 0
    
    def __should_render_text(self, text_width) :
        return text_width > self.__get_line_width() or self.__counter == len(self.__words)
                
    def __is_room_on_line_for_word(self, text_width) :
        return text_width <= self.__get_line_width() or not self.__render_list
        
    def __add_word_to_render_list(self, word) :
        self.__render_list.append(word)
        
    def __clear_render_list(self) :
        self.__render_list = []
        
    def __render_list_to_text(self) :
        return " ".join(self.__render_list)
    
    def __size_render_list(self) :
        return len(self.__render_list)
    
    def __calculate_total_line_height(self, text_height) :
        reserved_height = self.__leave_spaces.get(self.__current_line, 0)
        if reserved_height > text_height :
            text_height = reserved_height
            
        return int(text_height * self.__draw.line_spacing)  
    
    def __last_word_not_rendered(self, text_width) :
        return text_width > self.__bounds.width and self.__counter == len(self.__words)
    
    def __render_line(self):
        write_position = self.__get_aligned_position()

        if self.__should_justify_render_list() :
            self.__output_justifed_line(write_position)
        else:
            self.__output_line(write_position, self.__render_list_to_text())   

        self.__update_state_for_next_line()        

    def __get_aligned_position(self) :
        x, y = self.__bounds.origin
        
        if not self.__align in (TextRenderer.AlignLeft, TextRenderer.AlignJustify):
            text = self.__render_list_to_text()
            last_text_width = self.__measure_text_width(text)
            
            if self.__align == TextRenderer.AlignRight:
                x += line_width - last_text_width
            elif self.__align == TextRenderer.AlignCenter:
                x += (line_width - last_text_width) / 2
                
        return x, y
    
    def __measure_word(self, word) :
        if word in self.__word_lengths :
            width, height = self.__word_lengths[word]
        else :
            width, height = self.__draw.text_size(word)
            self.__word_lengths[word] = (width, height)
            
        return width, height
    
    def __measure_text_size_fast_inaccurate(self, text) :
        total_width = 0
        text_height = 0
        words = text.split(" ")
        counter = 0
        for word in words :
            width, height = self.__measure_word(word)
                
            total_width += width
            text_height = max(text_height, height)
            
            if counter and counter != (len(words) - 1) :
                width, height = self.__measure_word(' ')
                total_width += width
                
            counter += 1
      
        return total_width, text_height    
    
    def __measure_text_size_accurate(self, text) :
        return self.__draw.text_size(text)    
    
    def __measure_text_size(self, text) :
        return self.__measure_text_size_fast_inaccurate(text)
    
    def __measure_render_list_size(self) :
        return self.__measure_text_size_fast_inaccurate(self.__render_list_to_text())    
    
    def __measure_text_width(self, text) :
        return self.__measure_text_size(text)[0]
    
    def __should_justify_render_list(self) :
        return self.__align == TextRenderer.AlignJustify and self.__size_render_list() > 1
            
    def __output_line(self, position, text) :
        self.__draw.draw_text_line(position, text, self.__text_color)
            
    def __output_justifed_line(self, position) :   
        word_widths = self.__list_width_words()
        if self.__line_too_short_to_justify(word_widths) :
            self.__output_line(position, self.__render_list_to_text())
            return
        
        inter_word_space = self.__calculate_inter_word_space(word_widths)
        line_width = self.__get_line_width()
        
        x, y = position
        count = 0
    
        for word, word_width in zip(self.__render_list, word_widths):
            count += 1
            if count == self.__size_render_list() :
                x = position[0] + line_width - word_width
    
            self.__output_line((x, y), word)
    
            x += word_width + inter_word_space
    
    def __calculate_inter_word_space(self, word_widths) :
        return (self.__get_line_width() - sum(word_widths)) / (self.__size_render_list() - 1)
    
    def __line_too_short_to_justify(self, word_widths) :
        return sum(word_widths) < (self.__get_line_width() * 0.6)
              
    def __list_width_words(self) :
        word_widths = []
        for word in self.__render_list:
            word_width, _ = self.__measure_word(word)
            word_widths.append(word_width)   
            
        return word_widths
                    
    def __render_end_markers(self) :
        if not self.__end_text or self.__align != TextRenderer.AlignLeft :
            return

        marker_width = self.__measure_text_width(" " + self.__end_text)
        if marker_width + self.__last_line_width < self.__bounds.width :
            yoffset = -self.__last_line_height
            self.__move_render_positions(yoffset)
        else :
            self.__total_height += self.__last_line_height
           
        current_pos = self.__get_aligned_position() 
        position = (self.__bounds.x2 - marker_width, current_pos[1])
        self.__output_line(position, self.__end_text) 
       
        
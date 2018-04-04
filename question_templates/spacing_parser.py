from .parameter_parser import ParameterParser

class SpacingParser :
    def __init__(self, name, drawable, page) :
        self.name = name
        self.parser = ParameterParser(drawable.parameters)
        self.drawable = drawable
        self.page = page
        self.drawable_default = self.realize_parameter(name, None)
        self.page_top_default = getattr(page.parameters, self.__get_top_name())
        self.page_left_default = getattr(page.parameters, self.__get_left_name())
        
    def set_property_values(self) :
        self.__assign_side_attribute_group()
        self.__assign_top_bottom_attribute_group()      
        
    def realize_parameter(self, parameter_name, default) :
        value = self.parser.realize_parameter(parameter_name, default)
        if self.parser.is_percentage_value(parameter_name) :
            value *= self.page.parameters.get_column_width() 
            
        return value
        
    def __get_top_name(self) :
        return self.name + "_top_bottom"
    
    def __get_left_name(self) :
        return self.name + "_left_right"    
            
    def __assign_top_bottom_attribute_group(self) :
        param_name = self.__get_top_name()
        default = self.realize_parameter(param_name, self.__get_top_default())
        for name in ("top", "bottom") :
            self.__assign_attribute(name, default)
            
    def __get_top_default(self) :
        if self.drawable_default is None :
            return self.page_top_default
        else :
            return self.drawable_default
            
    def __assign_side_attribute_group(self) :
        param_name = self.__get_left_name()
        default = self.realize_parameter(param_name, self.__get_left_default())
        for name in ("left", "right") :
            self.__assign_attribute(name, default)
            
    def __get_left_default(self) :
        if self.drawable_default is None :
            return self.page_left_default
        else :
            return self.drawable_default    
            
    def __assign_attribute(self, name, default) :
        param_name = self.name + "_" + name
        if self.drawable.primary_element :
            value = getattr(self.drawable.primary_element, "_" + param_name)
        else :
            value = self.realize_parameter(param_name, default)
            #value += default
        
        setattr(self.drawable, "_" + param_name, value)         
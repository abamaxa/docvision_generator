import random

from graphics.util import pick_from_list

class ParameterError(Exception) :
    pass

class ParameterParser :
    def __init__(self, parameters) :
        self.parameters = parameters
        
    def is_percentage_value(self, parameter_name) :
        return self.__is_percentage_value(self.parameters.get(parameter_name))

    def realize_parameter(self, parameter_name, default = None) :
        if not parameter_name in self.parameters :
            return default
        
        value = self.parameters[parameter_name]
        if self.is_probability(parameter_name) :
            return self.true_or_false(value)
        
        elif self.is_probability_list(value) :
            return pick_from_list(value)
        
        elif isinstance(value, list) :
            return self.random_choice(value)
        
        elif isinstance(value, dict) :
            return self.realize_dict(value)

        return self.as_value(value)
        
    def realize_dict(self, dict_value) :
        rand_value = None
        if self.__is_percentage_value(dict_value) :
            dict_value = self.__convert_percentage_value(dict_value)
                    
        if "min" in dict_value and "max" in dict_value :
            min_v = dict_value.get("min")
            max_v = dict_value.get("max")
            if isinstance(min_v, int) and isinstance(max_v, int) :
                rand_value = random.randint(dict_value.get("min"), dict_value.get("max"))
            else :
                rand_value = dict_value.get("min")
                rand_value += random.random() * (dict_value.get("max") - dict_value.get("min"))            
            
        if not rand_value is None :    
            return rand_value * dict_value.get("scale", 1)        
        
        #parser = ParameterParser(dict_value)
        #return parser.realize_parameter()
        error_msg = "Don't know how to parse this dictionary: " + str(dict_value)
        raise NotImplementedError(error_msg)
    
    def realize_as_dict(self) :
        values = {}
        for key in self.parameters.keys() :
            if key == 'class' :
                continue
            
            values[key] = self.realize_parameter(key)
            
        return values
        
    def is_probability_list(self, value) :
        return isinstance(value, list) and isinstance(value[0], list) and \
               len(value[0]) == 2 and  isinstance(value[0][0], float)
    
    def is_probability(self, name) :
        return name.endswith("probability")
    
    def true_or_false(self, value):
        return random.random() < value
    
    def random_choice(self, value) :
        value = random.choice(value)
        if self.__is_percentage_value(value) :
            value = self.__convert_percentage_value(value)
            
        return value
    
    def __is_percentage_value(self, value) :
        if isinstance(value, str) and value.endswith('%') :
            return True
        elif isinstance(value, list) :
            return all([self.__is_percentage_value(v) for v in value])
        elif isinstance(value, dict) :
            if "min" in value and "max" in value :
                return self.__is_percentage_value(value["min"]) and \
                       self.__is_percentage_value(value["max"])         
            
        return False 
    
    def __convert_percentage_value(self, value) :
        if isinstance(value, str) and value.endswith('%') :
            return float(value[:-1]) * 0.01
        elif isinstance(value, list) :
            return [self.__convert_percentage_value(v) for v in value]
        elif isinstance(value, dict) :
            if "min" in value and "max" in value :
                copy_value = dict(value)
                copy_value["min"] = self.__convert_percentage_value(value["min"])
                copy_value["max"] = self.__convert_percentage_value(value["max"])
                return copy_value                
                            
        raise ParameterError("Values {} could not be converted as a percerntage".format(value))
                        
    def as_value(self, value) :
        if self.__is_percentage_value(value) :
            value = self.__convert_percentage_value(value)
            
        return value
    
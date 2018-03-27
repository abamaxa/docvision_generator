import random

from question_generator.util import pick_from_list

class ParameterParser :
    def __init__(self, parameters) :
        self.parameters = parameters

    def realize_parameter(self, parameter_name, default = None) :
        if not parameter_name in self.parameters :
            return default
        
        value = self.parameters[parameter_name]
        if self.is_probability(parameter_name) :
            return self.true_or_false(value)
        
        elif self.is_probability_list(value) :
            return pick_from_list(value)
        
        elif isinstance(value, list) :
            return random.choice(value)
        
        elif isinstance(value, dict) :
            return self.realize_dict(value)
        
        else :
            return value
        
    def realize_dict(self, dict_value) :
        if "min" in dict_value and "max" in dict_value :
            rand_value = random.randint(dict_value.get("min"), dict_value.get("max"))
            return rand_value * dict_value.get("scale", 1)        
        
        #parser = ParameterParser(dict_value)
        #return parser.realize_parameter()
        error_msg = "Don't know how to parse this dictionary: " + str(dict_value)
        raise NotImplementedError(error_msg)
        
    def is_probability_list(self, value) :
        return isinstance(value, list) and isinstance(value[0], list) and \
               len(value[0]) == 2 and  isinstance(value[0][0], float)
    
    def is_probability(self, name) :
        return name.endswith("probability")
    
    def true_or_false(self, value):
        return random.random() < value
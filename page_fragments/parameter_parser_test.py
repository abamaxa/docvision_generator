import unittest
import random
from page_fragments.parameter_parser import ParameterParser

test_params = {
    "int" : 1,
    "string" : "Hello World!",
    "list" : [1,2,3,4],
    "win_probability" : 0.5,
    "probability_list" : [[0.5, "Option 1"], [1.0, "Option 2"]],
    "min_max_dict" : {"min" : 1, "max" : 100},
    "min_max_scale_dict" : {"min" : 100, "max" : 10000, "scale": 0.01},
    "invalid_dict" : {},
    "percent" : "10%",
    "percent_dict" : {"min" : "5%", "max" : "30%"},
    "percent_list" : ["5%", "10%", "15%"]
}

class ParameterParserTest(unittest.TestCase) :
    def setUp(self) :
        random.seed(42)
        self.parser = ParameterParser(test_params)
        
    def test_missing_value(self) :
        value = self.parser.realize_parameter("missing")
        self.assertIs(value, None)
        value = self.parser.realize_parameter("missing", "default")
        self.assertTrue(isinstance(value, str))
        self.assertEqual(value, "default")        
        
    def test_int_value(self):
        value = self.parser.realize_parameter("int")
        self.assertTrue(isinstance(value, int))
        self.assertEqual(value, test_params["int"])
        
    def test_string_value(self):
        value = self.parser.realize_parameter("string")
        self.assertTrue(isinstance(value, str))
        self.assertEqual(value, test_params["string"])
        
    def test_list_value(self):
        value = self.parser.realize_parameter("list")    
        self.assertTrue(isinstance(value, int))
        self.assertEqual(value, 1)
                
    def test_probability_value(self):
        did_win = self.parser.realize_parameter("win_probability") 
        self.assertTrue(isinstance(did_win, bool))
        self.assertFalse(did_win)
          
    def test_probability_list_value(self):
        value = self.parser.realize_parameter("probability_list")  
        self.assertTrue(isinstance(value, str))
        self.assertEqual(value, test_params["probability_list"][1][1])
                
    def test_min_max_dict_value(self):
        value = self.parser.realize_parameter("min_max_dict")  
        self.assertTrue(isinstance(value, int))
        self.assertEqual(value, 82)
        
    def test_min_max_scale_dict_value(self):
        value = self.parser.realize_parameter("min_max_scale_dict")  
        self.assertTrue(isinstance(value, float))
        self.assertAlmostEqual(value, 19.24)
        
    def test_percent_value(self):
        self.assertFalse(self.parser.is_percentage_value("min_max_scale_dict"))
        self.assertTrue(self.parser.is_percentage_value("percent"))
        value = self.parser.realize_parameter("percent")  
        self.assertTrue(isinstance(value, float))
        self.assertAlmostEqual(value, 0.1)    
        
    def test_percent_list_value(self):
        self.assertTrue(self.parser.is_percentage_value("percent_list"))
        value = self.parser.realize_parameter("percent_list")  
        self.assertTrue(isinstance(value, float))
        self.assertAlmostEqual(value, 0.15)  
        
    def test_percent_dict_value(self):
        self.assertTrue(self.parser.is_percentage_value("percent_dict"))
        value = self.parser.realize_parameter("percent_dict")  
        self.assertTrue(isinstance(value, float))
        self.assertAlmostEqual(value, 0.20985669)  
        
    def test_invalid_dict(self) :
        with self.assertRaises(NotImplementedError) :
            value = self.parser.realize_parameter("invalid_dict")
        
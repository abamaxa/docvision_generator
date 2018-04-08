import unittest
import random
import os

from PIL import Image

from graphics.formula import Formula
TEXT_SIZE = 14

class FormulaTest(unittest.TestCase) :
    def setUp(self) :
        self.formula = Formula(TEXT_SIZE)
        
    def __test_many_times(self, name) :
        for _ in range(10) :
            seed = random.randint(1,35000)
            random.seed(seed)
            self.formula = Formula(TEXT_SIZE)
            foo = getattr(self.formula, "generate_" + name) 
            foo()
            
            self.assertIsInstance(self.formula.image, Image.Image, "Seed was {}".format(seed))
        
        self.__debug_save(name + ".png")
        
    def __get_output_path(self, name) :
        root = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(root,'output',name)
        
    def __debug_save(self, name) :
        filepath = self.__get_output_path(name)
        os.makedirs(os.path.dirname(filepath), exist_ok = True)
        image = self.formula.image
        image.save(filepath)
        
    def test_quadratic(self) :
        self.__test_many_times("quadratic")    
        
    def test_angle_ranges(self) :
        self.__test_many_times("angle_ranges")    

    def test_intergral(self) :
        self.__test_many_times("intergral")    
        
    def test_inequalities(self) :
        self.__test_many_times("inequalities")    
        
    def test_surds(self) :
        self.__test_many_times("surds")    

    def test_factorizations(self) :
        self.__test_many_times("factorizations")    

    def test_trig(self) :
        self.__test_many_times("trig")    
import unittest

from question_templates.abstract_drawable import AbstractDrawable

class AbstractDrawableTest(unittest.TestCase) :
    def test_create_draw(self) :    
        with self.assertRaises(TypeError) :
            d = AbstractDrawable({}) 
            self.assertIs(d, AbstractDrawable)

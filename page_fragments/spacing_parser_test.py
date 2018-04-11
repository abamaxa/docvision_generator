from unittest.mock import MagicMock
from unittest import TestCase

from graphics.bounds import Bounds, Size
from page_generator.page import Page
from page_fragments.spacing_parser import SpacingParser
from page_fragments import *

BOUNDS_HEIGHT = 200
BOUNDS_WIDTH = 100

zero_page_parameters = {
    "margin_left_right" : 0,
    "margin_top_bottom" : 0
}

one_two_page_parameters = {
    "margin_left_right" : 1,
    "margin_top_bottom" : 2
}

def create_test_page(page_parameters) :
    attrs = {
        "parameters" : MagicMock(**page_parameters)
    }
    return MagicMock(spec=Page, **attrs)    

class SpacingParserTest(TestCase) :
    def test_default_zero(self) :
        page = create_test_page(zero_page_parameters)
        drawable = Drawable({})
        parser = SpacingParser("margin", drawable, page)
        
        parser.set_property_values()
        
        self.assertEqual(drawable._margin_left, 0)
        self.assertEqual(drawable._margin_right, 0)
        self.assertEqual(drawable._margin_top, 0)
        self.assertEqual(drawable._margin_bottom, 0)
        
    def test_default(self) :
        page = create_test_page(one_two_page_parameters)
        drawable = Drawable({})
        parser = SpacingParser("margin", drawable, page)
        
        parser.set_property_values()
        
        self.assertEqual(drawable._margin_left, 1)
        self.assertEqual(drawable._margin_right, 1)
        self.assertEqual(drawable._margin_top, 2)
        self.assertEqual(drawable._margin_bottom, 2)    
        
    def test_drawable_params(self) :
        page = create_test_page(zero_page_parameters)
        drawable = Drawable({"margin_left_right" : 1, "margin_top" : 2})
        parser = SpacingParser("margin", drawable, page)
        
        parser.set_property_values()
        
        self.assertEqual(drawable._margin_left, 1)
        self.assertEqual(drawable._margin_right, 1)
        self.assertEqual(drawable._margin_top, 2)
        self.assertEqual(drawable._margin_bottom, 0)    
        
    def test_global_params(self) :
        page = create_test_page(zero_page_parameters)
        drawable = Drawable({"margin" : 1})
        parser = SpacingParser("margin", drawable, page)
        
        parser.set_property_values()
        
        self.assertEqual(drawable._margin_left, 1)
        self.assertEqual(drawable._margin_right, 1)
        self.assertEqual(drawable._margin_top, 1)
        self.assertEqual(drawable._margin_bottom, 1)   
        
        
    def test_precedence(self) :
        page = create_test_page(one_two_page_parameters)
        drawable = Drawable({"margin" : 10, "margin_bottom" : 20})
        parser = SpacingParser("margin", drawable, page)
        
        parser.set_property_values()
        
        self.assertEqual(drawable._margin_left, 10)
        self.assertEqual(drawable._margin_right, 10)
        self.assertEqual(drawable._margin_top, 10)
        self.assertEqual(drawable._margin_bottom, 20)   
        
import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import draw_test
from graphics.bounds import Bounds, Size
from question_generator.page import Page
from question_generator.question_params import QuestionParams
from question_templates.drawable import Drawable

border_parameters = {
    "border" : {
        "probability" : 1.0,
        "style" : 1,
        "width" : {"min" : 1, "max" : 8},
    }
}

MARGIN = 5
PADDING = 10
LINE_HEIGHT = 12

page_parameters = {
    "margins" : MARGIN,
    "padding" : PADDING,
    "line_spacing" : draw_test.LINE_SPACING,
    "line_height" : LINE_HEIGHT,
}

BOUNDS_HEIGHT = 200
BOUNDS_WIDTH = 100

def create_test_page() :
    attrs = {
        "parameters" : MagicMock(**page_parameters)
    }
    return MagicMock(spec=Page, **attrs)    

class DrawableTest(unittest.TestCase) :
    def setUp(self) :
        random.seed(42)
        self.page = create_test_page()
        self.drawable = None
         
    def _create_drawable(self, parameters = {}) :
        self.drawable = Drawable(parameters) 
                
    def _get_draw_mock(self) :
        return MagicMock()
    
    def _get_test_bounds(self) :
        return Bounds(0,0,BOUNDS_WIDTH,BOUNDS_HEIGHT) 
    
    def _get_expected_inner_size(self) :
        width, height = self.drawable.get_content_size()
        padding_and_margin = MARGIN + PADDING
        if width == Drawable.FILL_PARENT :
            width = BOUNDS_WIDTH - (2 * padding_and_margin)
        if height == Drawable.FILL_PARENT :
            height = BOUNDS_HEIGHT - (2 * padding_and_margin)
        return Size(width, height)
              
    def test_inner_bounds(self) :    
        self._create_drawable() 
        
        with self.assertRaises(TypeError) :
            bounds = self.drawable.inner_bounds
        
        self.drawable.update_page_parameters(self.page)
        self.drawable.calculate_dimensions(self._get_draw_mock(), self._get_test_bounds())
        
        bounds = self.drawable.inner_bounds
        self.assertTrue(isinstance(bounds, Bounds))
        
    def test_border_exists(self) :
        self._create_drawable(border_parameters) 
        self.drawable.update_page_parameters(self.page)
        self.drawable.calculate_dimensions(self._get_draw_mock(), self._get_test_bounds())
        
        self.assertTrue(self.drawable._has_border())
                
    def test_border_bounds(self) :    
        self._create_drawable(border_parameters) 
        self.drawable.update_page_parameters(self.page)
        self.drawable.calculate_dimensions(self._get_draw_mock(), self._get_test_bounds())
        
        self.assertTrue(self.drawable._has_border())
        
        bounds = self.drawable.border_bounds 
        expected_inner_size = self._get_expected_inner_size()
        
        self.assertTrue(isinstance(bounds, Bounds))
        self.assertEqual(bounds.x, MARGIN)
        self.assertEqual(bounds.y, MARGIN)
        self.assertEqual(bounds.width, expected_inner_size.width + (2 * PADDING))
        self.assertEqual(bounds.height, expected_inner_size.height + (2 * PADDING))
        
        padding_and_margin = MARGIN + PADDING        
        bounds = self.drawable.inner_bounds 
        
        self.assertTrue(isinstance(bounds, Bounds))
        self.assertEqual(bounds.x, padding_and_margin)
        self.assertEqual(bounds.y, padding_and_margin)
        self.assertEqual(bounds.width, expected_inner_size.width)
        self.assertEqual(bounds.height, expected_inner_size.height)

    def test_no_border_bounds(self) :    
        self._create_drawable()
        self.drawable.update_page_parameters(self.page)
        self.drawable.calculate_dimensions(self._get_draw_mock(), self._get_test_bounds())
        
        expected_inner_size = self._get_expected_inner_size()
        bounds = self.drawable.border_bounds
        self.assertIs(bounds, None)

        padding_and_margin = MARGIN + PADDING        
        bounds = self.drawable.inner_bounds 
        
        self.assertTrue(isinstance(bounds, Bounds))
        self.assertEqual(bounds.x, padding_and_margin)
        self.assertEqual(bounds.y, padding_and_margin)
        self.assertEqual(bounds.width, expected_inner_size.width)
        self.assertEqual(bounds.height, expected_inner_size.height)
    
import unittest
import random
from unittest.mock import patch, call, MagicMock

from graphics import Bounds, Draw
from graphics.text_renderer_test import draw_attrs, CHAR_WIDTH, LINE_HEIGHT, LINE_SPACING
from question_templates.drawable_test import DrawableTest, MARGIN, PADDING, BOUNDS_WIDTH
from question_templates.text import Text

class TextTest(DrawableTest) :
    def _create_drawable(self, parameters = {}) :
        self.drawable = Text(parameters)
                
    def update_drawable(self) :
        self.drawable.update_page_parameters(self.page)
        self.drawable.text = "Hello"
        self.drawable.calculate_dimensions(self._get_draw_mock(), self._get_test_bounds())
        
    def _get_draw_mock(self) :
        attrs = dict(draw_attrs)
        attrs["calculate_text_height"] = lambda x,y : LINE_HEIGHT * (1 + ((len(y) * CHAR_WIDTH) // x))
        return MagicMock(spec=Draw, **attrs)  
                
    def test_bold_creation(self) :
        json = {
            "class" : "Text",
            "sentences" : 1,
            "bold_words_probability" : 0.1,
            "bold_words_count" : 0.1                
        }
        
        self._create_drawable(json)
        self.update_drawable()           

    def test_margin(self) :
        json ={
            "class" : "Text",
            "sentences" : 1,
            "margin_left" : 5                
        }
        
        self._create_drawable(json) 
        self.update_drawable() 
        
        bounds = self.drawable.inner_bounds
        self.assertEqual(bounds.x, 35)  
        
    def test_padding(self) :
        json ={
            "class" : "Text",
            "sentences" : 1,
            "margin_left" : 5                
        }
        
        self._create_drawable(json) 
        self.update_drawable() 
        
        bounds = self.drawable.inner_bounds
        self.assertEqual(bounds.x, 35)      

    def test_no_border_bounds(self) :   
        json ={
            "class" : "Text",
            "sentences" : 1              
        }
        
        self._create_drawable(json) 
        self.update_drawable() 
        
        bounds = self.drawable.border_bounds
        self.assertIs(bounds, None)
    
        padding_and_margin = MARGIN + PADDING        
        bounds = self.drawable.inner_bounds 
    
        self.assertTrue(isinstance(bounds, Bounds))
        self.assertEqual(bounds.x, padding_and_margin)
        self.assertEqual(bounds.y, padding_and_margin)
        self.assertEqual(bounds.width, BOUNDS_WIDTH - (2 * padding_and_margin))
        self.assertEqual(bounds.height, LINE_HEIGHT * LINE_SPACING)
    
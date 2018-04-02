import unittest
import random
from unittest.mock import patch, call

import graphics.draw
from page_generator.question_params import QuestionParams
#from graphics import Draw

DIMENSIONS = (600,1000)
LINE_SPACING = 1.2
POINT1 = (0,0)
POINT2 = (100,100)
FILL_COLOR = "#0"
LINE_WIDTH = 1

options = {
"dimensions" : DIMENSIONS
}

class DrawTest(unittest.TestCase) :
    def setUp(self) :
        random.seed(42)
        self.params = QuestionParams("test", options)
        self.params.generate_random_parameters()
        
        self.pil_image = None
        self.pil_font = None
        self.pil_draw = None
        self.draw = None
        
    @patch("graphics.draw.Image")
    @patch("graphics.draw.ImageDraw")
    @patch("graphics.draw.ImageFont")
    def create_draw(self, font, draw, image) :   
        self.pil_image = image
        self.pil_font = font
        self.pil_draw = draw
        
        self.draw = graphics.draw.Draw(self.params)
        self.draw.init_image()
        self.draw.create_draw()

    def test_create_draw(self) :        
        self.create_draw()
        
        self.assertEqual(self.pil_image.mock_calls[0],
            call.new('RGBA', DIMENSIONS, (0, 0, 0, 0)))

        self.assertEqual(len(self.pil_draw.mock_calls), 1)         
        
    def test_get_image_size(self) :
        self.create_draw()
        
        size = self.draw.get_image_size()
        self.assertEqual(size[0], DIMENSIONS[0])
        self.assertEqual(size[1], DIMENSIONS[1])
        
    def test_measure_only_mode(self) :
        self.create_draw()
        
        self.assertFalse(self.draw.measure_only_mode)
        self.draw.measure_only_mode = True
        self.assertTrue(self.draw.measure_only_mode)
        
    def test_line_spacing(self) :
        self.create_draw()
        self.assertEqual(self.draw.line_spacing, LINE_SPACING)
        
    def test_draw_rectangle(self):
        self.create_draw()
        self.pil_draw.reset_mock()
        
        self.draw.draw_rectangle((POINT1,POINT2))
        
        self.assertEqual(len(self.pil_draw.mock_calls), 1) 
        self.assertEqual(self.pil_draw.mock_calls[0], 
                        call.Draw().rectangle((POINT1, POINT2), None, None) ) 
        
        self.pil_draw.reset_mock()
        self.draw.measure_only_mode = True
        
        self.draw.draw_rectangle((POINT1,POINT2))
        
        self.assertEqual(len(self.pil_draw.mock_calls), 0)         
        
    def test_draw_line(self):
        self.create_draw()
        self.pil_draw.reset_mock()      
        
        self.draw.draw_line((POINT1,POINT2), LINE_WIDTH)
        
        self.assertEqual(len(self.pil_draw.mock_calls), 1) 
        self.assertEqual(self.pil_draw.mock_calls[0], 
                call.Draw().line((POINT1, POINT2), fill=self.params.border_color, width=LINE_WIDTH) ) 
    
        self.pil_draw.reset_mock()
        self.draw.measure_only_mode = True
    
        self.draw.draw_line((POINT1,POINT2))
    
        self.assertEqual(len(self.pil_draw.mock_calls), 0)                 
            
    def test_draw_circle(self):
        self.create_draw()
        self.pil_draw.reset_mock()
        
        self.draw.draw_circle(POINT1, LINE_WIDTH)
        
        self.assertEqual(len(self.pil_draw.mock_calls), 1) 
    
        self.pil_draw.reset_mock()
        self.draw.measure_only_mode = True
    
        self.draw.draw_circle(POINT1, LINE_WIDTH)
    
        self.assertEqual(len(self.pil_draw.mock_calls), 0)        
            
    def test_draw_text_line(self) :
        self.create_draw()
        self.pil_draw.reset_mock()
        
        self.draw.draw_text_line(POINT1, "Hello", (0,0,0,0))
        self.assertEqual(len(self.pil_draw.mock_calls), 1) 
    
        self.pil_draw.reset_mock()
        self.draw.measure_only_mode = True
    
        self.draw.draw_text_line(POINT1, "Hello", (0,0,0,0))
    
        self.assertEqual(len(self.pil_draw.mock_calls), 0)           
            
    def test_draw_question_circle(self):
        self.create_draw()
        self.pil_draw.reset_mock()
        
        self.draw.draw_question_circle(POINT1) 
        self.assertEqual(len(self.pil_draw.mock_calls), 1) 
            
        self.pil_draw.reset_mock()
        self.draw.measure_only_mode = True
    
        self.draw.draw_question_circle(POINT1)        
        self.assertEqual(len(self.pil_draw.mock_calls), 0)     

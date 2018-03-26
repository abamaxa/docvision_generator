import unittest
from unittest.mock import MagicMock

TEXT_COLOR = "#0"
LINE_HEIGHT = 10
LINE_SPACING = 1.2
CHAR_WIDTH = 10

draw_attrs = {
    'get_line_height.return_value': LINE_HEIGHT, 
    'get_image_size.return_value':(1000,600),
    'line_spacing' : LINE_SPACING,
    'text_size.side_effect' : lambda x: (len(x) * CHAR_WIDTH, LINE_HEIGHT)
}

from graphics import TextRenderer, Draw, Bounds

class TextRendererTest(unittest.TestCase) :
    def setUp(self) :
        self.draw = MagicMock(spec=Draw, **draw_attrs)
        
    def do_hello_world_alignment_test(self, align) :
        text = "Hello World"
        renderder = TextRenderer(self.draw, text, TEXT_COLOR)
        
        text_size = draw_attrs['text_size.side_effect']
        
        bounds = Bounds(0,0,text_size(text)[0],100)
        height = renderder.calculate_text_height(bounds)

        self.assertEqual(height, LINE_HEIGHT * LINE_SPACING)
        
        bounds = Bounds(0,0,text_size(text)[0] * 1.5,100)
        height = renderder.calculate_text_height(bounds)
    
        self.assertEqual(height, LINE_HEIGHT * LINE_SPACING)        
        
        bounds = Bounds(0,0,text_size(text)[0] / 2,100)
        height = renderder.calculate_text_height(bounds)  
        
        self.assertEqual(height, LINE_HEIGHT * LINE_SPACING * 2)
            
    def test_hello_world_left_align(self) :
        self.do_hello_world_alignment_test(TextRenderer.AlignLeft)
        
    def test_hello_world_centered_align(self) :
        self.do_hello_world_alignment_test(TextRenderer.AlignCenter)
        
    def test_hello_world_right_align(self) :
        self.do_hello_world_alignment_test(TextRenderer.AlignRight)
        
    def test_hello_world_justified(self) :
        self.do_hello_world_alignment_test(TextRenderer.AlignRight)
        
    

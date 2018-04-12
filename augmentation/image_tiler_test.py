from unittest.mock import MagicMock, patch, call
from unittest import TestCase
import re
import random

from augmentation.image_tiler import ImageTiler
from augmentation.compositor import PageCompositor
from graphics import Frame, Bounds

FRAMES = [Frame(Bounds(0,0,100,100), "0"), 
          Frame(Bounds(500,500,500,500), "1")]

class ImageTilerTest(TestCase) :
    def setUp(self) :
        random.seed(42)
        
    def create_tiler(self, document_size, frames) :
        self.page = MagicMock(**{
            "get_frames.return_value" : frames,
            "get_image.return_value" : MagicMock(**{
                "size" : document_size
            }),
        })
        
        self.image_tiler = ImageTiler(self.page)
        
    def __bounds_from_call(self, call) :
        m = re.search(r'x: ([-\d]+) y: ([-\d]+) Width: (\d+) Height: (\d+)', str(call))
        self.assertFalse(m is None)
        bounds = Bounds(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
        return bounds
                
    @patch.object(PageCompositor, "copy_image_from_rect")
    def test_page_tile(self, compositor) :
        DOC_SIZE = (1000,1000)
        self.create_tiler(DOC_SIZE, FRAMES)
        
        tile = self.image_tiler._ImageTiler__get_page_tile()
        self.assertIsInstance(tile, tuple)
        
        bounds = self.__bounds_from_call(compositor.mock_calls[0])
        self.assertEqual(bounds.width, DOC_SIZE[0])
        self.assertEqual(bounds.height, DOC_SIZE[1])
           
    @patch.object(PageCompositor, "copy_image_from_rect")  
    def test_offset_page_tile(self, compositor) :
        DOC_SIZE = (1000,2000)
        self.create_tiler(DOC_SIZE, FRAMES)
        
        tile = self.image_tiler._ImageTiler__get_page_tile()
        self.assertIsInstance(tile, tuple)
        
        bounds = self.__bounds_from_call(compositor.mock_calls[0])
        self.assertEqual(bounds.width, DOC_SIZE[0])
        self.assertEqual(bounds.y2, 1114)        

        
    @patch.object(PageCompositor, "copy_image_from_rect", lambda x, y: x)  
    def test_impossible_page_tile(self) :
        DOC_SIZE = (1000,2000)
        FRAMES = [Frame(Bounds(0,0,1000,1200), "0") ]
        
        self.create_tiler(DOC_SIZE, FRAMES)
        
        tile = self.image_tiler._ImageTiler__get_page_tile()
        self.assertIs(tile, None)
        
    @patch.object(PageCompositor, "__init__", return_value=None)
    @patch.object(PageCompositor, "make_composite_image") 
    def test_page_tile(self, make_composite_image, compositor) :
        DOC_SIZE = (1000,2000)        
        self.create_tiler(DOC_SIZE, FRAMES)
        
        tile = self.image_tiler._ImageTiler__get_fragment_tile(FRAMES[0])
        self.assertIsInstance(tile, tuple)
        
        frame_bounds = self.__bounds_from_call(tile)
        self.assertEqual(frame_bounds.width, FRAMES[0].width)
        self.assertEqual(frame_bounds.height, FRAMES[0].height)        
        self.assertEqual(frame_bounds.x, 45)
        self.assertEqual(frame_bounds.y, 45) 
        
        image_bounds = self.__bounds_from_call(compositor.mock_calls[0])
        self.assertEqual(image_bounds.x, -45)
        self.assertEqual(image_bounds.y, -45)        
        self.assertEqual(image_bounds.width, 190)
        self.assertEqual(image_bounds.height, 190)    
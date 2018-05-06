import random

from PIL import Image, ImageDraw
from .compositor import PageCompositor
from graphics import Frame, Bounds
import augmentation.postprocessor as postprocessor

class ImageTiler :
    def __init__(self, page) :
        self.image = page.get_image()
        self.frames = page.get_frames()
        self.erode_by = page.options["erode"]
        self.returned_whole_page = False
        self.current = 0
        self.chop = page.options["chop"]
        self.columns = page.parameters.columns
        self.num_page_tiles = 0
        
        if self.chop :
            self.num_page_tiles = 1
        elif page.options["augment"] :
            self.num_page_tiles = 3
              
    def get_tile(self) :
        num_frames = len(self.frames) 
        if num_frames == 0 :
            raise StopIteration
        
        tile = None
        
        if self.current == 0 :
            tile = self.__get_whole_page()
            
        elif self.__should_create_fragment_tiles() :
            frame = self.frames[self.current % num_frames]
            tile = self.__get_fragment_tile(frame)
            
        elif self.num_page_tiles :
            self.num_page_tiles -= 1
            tile = self.__get_page_tile()
            
        if tile is None :
            raise StopIteration

        self.current += 1
        return self.__postprocess(tile)
    
    def __should_create_fragment_tiles(self) :
        num_frames = len(self.frames)
        return self.current <= num_frames and self.chop and self.columns > 1
        
    def __get_whole_page(self) :
        rect = Bounds(0,0, self.image.width, self.image.height)
        image = PageCompositor.copy_image_from_rect(self.image, rect)
        return image, self.frames
        
    def __get_page_tile(self) :
        img_size = self.image.size
        
        for attempts in range(5) :
            y_offset = random.randint(0, img_size[1] - img_size[0])
            bounds = Bounds(0, y_offset, img_size[0], img_size[0])
            
            frames = self.__get_frames_for_region(bounds)
            
            if frames :
                img = self.__extract_image_region(bounds)
                return img, frames  

    def __get_fragment_tile(self, frame) :                
        mid_x = frame.x + frame.width / 2
        mid_y = frame.y + frame.height / 2
        
        max_dim = max(frame.width, frame.height)
        half_dim = max_dim / 2
                
        top = mid_y - half_dim
        left = mid_x - half_dim
        right = left + max_dim
        bottom = top + max_dim

        fragment_region = Bounds(left, top, x2=right, y2=bottom)
        inflate_by = random.randint(max_dim // 4, max_dim // 2)
        fragment_region = fragment_region.inflate(inflate_by, inflate_by)
        
        frames = self.__get_frames_for_region(fragment_region)
        
        compositor = PageCompositor(self.image, fragment_region)
        return compositor.make_composite_image(), frames
            
    def __get_frames_for_region(self, region_bounds) :
        region_frames = []
        for frame in self.frames :
            if not frame.enclosed_by_bounds(region_bounds) :
                continue
            
            region_frames.append(frame.move(-region_bounds.x, -region_bounds.y))
        
        return region_frames
    
    def __extract_image_region(self, bounds) :
        return PageCompositor.copy_image_from_rect(self.image, bounds)
    
    def __postprocess(self, tile) :
        if self.erode_by :
            image = postprocessor.postprocess(tile[0], self.erode_by)   
        return (image, tile[1])
    
    def get_frames(self) :
        return self.frames
    
      
      

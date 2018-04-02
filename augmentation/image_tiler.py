import random

from PIL import Image, ImageDraw
from .compositor import QuestionCompositor
from .rect import *

class ImageTiler :
    def __init__(self, question, options) :
        self.image = question.get_image()
        self.frames = question.get_frames()
        self.options = options
        self.questions_to_frame = list(self.frames)
        self.returned_whole_page = False
        
    def get_tile(self) :
        tile = None
        
        if not self.returned_whole_page :
            tile = self.__get_whole_page()
            self.returned_whole_page = True
            
        elif random.random() < 0.7 :
            tile = self.__get_question_tile()
            
        if not tile :
            tile = self.__get_page_tile()
            
        return tile
    
    def __get_whole_page(self) :
        rect = ((0,0), self.image.size)
        image = QuestionCompositor.copy_image_from_rect(self.image, rect)
        return image, self.frames
        
    def __get_page_tile(self) :
        img_size = self.image.size
        
        for attempts in range(5) :
            if attempts < 3 :
                y_offset = random.randint(0, img_size[1] - img_size[0])
                
            else :
                question_frames = self.frames
                
                question_tops = [1 + int(r[0][1]) for r,_ in question_frames]
                question_tops += [int(r[1][1]) - img_size[0] - 1 for r,_ in question_frames]
                question_tops = [t for t in question_tops 
                                 if t >= 0 and t < img_size[1] - img_size[0]]

                y_offset = random.choice(question_tops)

            rect = ((0, y_offset), (img_size[0], img_size[0] + y_offset))

            frames = self.__get_frames_for_region(rect)

            if frames :
                break

        img = self.__extract_image_region(rect)
        return img, frames  
    
    def __get_question_tile(self) :
        question_frames = self.questions_to_frame 
        if not question_frames :
            return
    
        frame_record = random.choice(question_frames)
        self.questions_to_frame.remove(frame_record)
        frame, object_type = frame_record
        
        width = frame[1][0] - frame[0][0]
        height = frame[1][1] - frame[0][1]
        
        mid_x = (frame[1][0] + frame[0][0]) / 2
        mid_y = (frame[1][1] + frame[0][1]) / 2
        
        max_dim = max(width, height)
        half_dim = max_dim / 2
                
        top = mid_y - half_dim
        left = mid_x - half_dim
        right = left + max_dim
        bottom = top + max_dim

        question_region = ((left, top), (right, bottom))
        inflate_by = random.choice([max_dim / 20, max_dim / 10, 
                                    max_dim / 5, max_dim / 4, 
                                    max_dim / 3, max_dim / 2])
        question_region = inflate_rect(question_region, inflate_by, inflate_by)
        
        frames = self.__get_frames_for_region(question_region)
        
        compositor = QuestionCompositor(self.image, question_region)
        return compositor.get_composite_image(), frames
            
    def __get_frames_for_region(self, region_rect) :
        question_frames = list(self.frames)
        
        x_offset = region_rect[0][0]
        y_offset = region_rect[0][1]

        region_frames = []
        for rect, object_type in question_frames :
            if not rect_enclosed_by_rect(region_rect, rect) :
                continue
            
            rect = offset_rects([rect], (x_offset, y_offset))
            region_frames.append((rect[0], object_type))
        
        return region_frames
    
    def __extract_image_region(self, rect) :
        return QuestionCompositor.copy_image_from_rect(self.image, rect)
    
    def get_frames(self) :
        return self.frames
    
      
      

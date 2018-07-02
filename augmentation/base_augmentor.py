import abc
import json

import cv2
import numpy as np
from PIL import Image, ImageDraw

import augmentation.postprocessor as postprocessor

from graphics import Bounds, Frame, RotatedFrame

CROP = "crop"
CROP_AND_PAD = "crop_and_pad"
AFFINE = "affine"
PERSPECTIVE = "perspective"
PIECEWISE_AFFINE = "piecewise"

PROBABILITY = "probability"
SCALE = "scale"
KEEP_SIZE = "keep_size"
MIN_PERCENT = "min_percent"
MAX_PERCENT = "max_percent"
PAD_MODE = "pad_mode"
CVAL = "cval"
TRANSLATE_PERCENT = "translate_percent"
ROTATE = "rotate"
SHEAR = "shear"
ORDER = "order"

class AbstractAugmentor(object) :
    def __init__(self, page, tiler, options) :
        self.options = options
        self.page = page
        self.augmentation_options = {}
        self.tiler = tiler
        
        self.image = None 
        self.image_np = None
        self.frames = None
        
        self.augmented_image = None
        self.augmented_frames = None
        self.num_page_tiles = 0
        
        self.current = 0
        self.load_augmentation_options()
                        
    def __iter__(self):
        return self

    def __next__(self): 
        self.augmented_image = None
        self.augmented_frames = None
        
        self.image, self.frames = self.tiler.get_tile()
        
        # Never augment the first image
        if self.options["augment"] and self.current :
            self.generate_augmented_image()
        else :
            self.resize_image()
                        
        self.draw_debug_rects()
        
        self.current += 1
        
        return self.__images_to_return()

    def __images_to_return(self) :
        if self.options["augment"] and self.augmented_image :
            return self.augmented_image, self.augmented_frames 
        else :
            return self.image, self.frames
        
    def draw_debug_rects(self) :
        if not self.options.get("draw_final_rects") :
            return
        
        image, frames = self.__images_to_return()
        
        draw = ImageDraw.Draw(image)
        
        for frame in frames :
            #if frame.x == -1 and frame.y == -1 :
            #    continue
            
            if isinstance(frame, Frame) :
                draw.rectangle(frame.rectangle, outline="green") 
            else :
                draw.polygon(frame.points, outline="green") 
                
        del draw
        
    def convert_image_to_numpy(self) :
        self.image_np = postprocessor.convert_image_to_numpy(self.image)
                    
    def set_augmented_image_from_numpy(self, np_image) :
        self.augmented_image = Image.fromarray(np_image)
    
    def get_parameter(self, augmentation_name, parameter, default = None) :
        section = self.augmentation_options.get(augmentation_name)
        
        return section.get(parameter, default)
    
    def load_augmentation_options(self) :
        with open(self.options.get("augmentation_file"), "r") as json_file :
            self.augmentation_options = json.load(json_file)
            
    def resize_image(self) :
        final_size = self.options.get("outputSize")
        if self.image.width == final_size[0] and self.image.height == final_size[1] :
            return
        
        xscale = final_size[0] / self.image.width
        yscale = final_size[1] / self.image.height
        
        self.frames =[f.scale(xscale, yscale) for f in self.frames]
        self.image = self.image.resize(final_size, Image.BICUBIC)
    
    @abc.abstractmethod
    def generate_augmented_image(self) :
        pass
    

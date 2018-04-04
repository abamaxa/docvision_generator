import abc
import json

from PIL import Image, ImageDraw

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
    def __init__(self, question, tiler, options) :
        self.options = options
        self.question = question
        self.augmentation_options = {}
        self.tiler = tiler
        
        self.image = None 
        self.frames = None
        
        self.augmented_image = None
        self.augmented_frames = None
        
        self.current = 0
        self.count = 0
        self.__calculate_number_of_images_to_generate()
        self.load_augmentation_options()
        
    def __iter__(self):
        return self

    def __next__(self): 
        if self.current > self.count:
            raise StopIteration
        else:
            self.augmented_image = None
            self.augmented_frames = None
            self.image, self.frames = self.tiler.get_tile()

            if self.options["augment"] :
                self.generate_augmented_image()
            
            self.draw_debug_rects()
            
            self.current += 1
            
            return self.__images_to_return()
            
            
    def __images_to_return(self) :
        if self.options["augment"] :
            return self.augmented_image, self.augmented_frames 
        else :
            return self.image, self.frames
        
    def __calculate_number_of_images_to_generate(self) :
        if self.options["chop"] :
            self.count = int(len(question.get_frames()) * 1.5)
        else :
            self.count = 1   

    def draw_debug_rects(self) :
        if not self.options.get("draw_final_rects") :
            return
        
        image, frames = self.__images_to_return()
        
        draw = ImageDraw.Draw(image)
        
        for rect, _ in frames :
            if rect[0][0] == -1 and rect[0][1] == -1 :
                continue
            
            draw.rectangle(rect, outline="green") 
            
        del draw
    
    def get_parameter(self, augmentation_name, parameter, default = None) :
        section = self.augmentation_options.get(augmentation_name)
        
        return section.get(parameter, default)
    
    def load_augmentation_options(self) :
        with open(self.options.get("augmentation_file"), "r") as json_file :
            self.augmentation_options = json.load(json_file)
    
    @abc.abstractmethod
    def generate_augmented_image(self) :
        pass
    

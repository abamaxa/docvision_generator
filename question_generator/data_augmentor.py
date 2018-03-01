from imgaug import augmenters as iaa

class DataAugmentor:
    CROP = 1
    PAD = 2
    PERSPECTIVE = 3
    
    def __init__(self, count, image, frames, options):
        self.image = image
        self.frames = frames
        
        self.augmented_image = None
        self.augmented_frames = None
        
        self.current = 0
        self.count = count
        
        self.prob_perspective = options.get("prob_perspective", 0.6)
        self.perspective_max_angle = options.get("perspective_max_angle", 15)
        
        self.prob_rescale = options.get("prob_rescale", 0.9)
        self.max_scale = options.get("max_scale", 0.5)
        
        self.prob_pad = options.get("prob_pad", 0.4)
        self.max_pad = options.get("max_pad", 0.2)
        
        self.crop_pad = options.get("prob_crop", 0.4)
        self.max_crop = options.get("max_crop", 0.2)        
        
    def __iter__(self):
        return self

    def __next__(self): # Python 3: def __next__(self)
        if self.current > self.count:
            raise StopIteration
        else:
            self.augmented_image = self.image
            self.augmented_frames = self.frames
            
            self.generate_augmented_image()
            self.current += 1
            return self.augmented_image, self.augmented_frames
        
    def generate_augmented_image(self) :
        # Rescale before perspective to save changes
        self.rescale()        
        self.crop_and_pad_image()
        self.apply_perspective()
        self.resize()
        
    def rescale(self) :
        #if self.prob_rescale > random.random() :
        pass
    
    def crop_and_pad_image(self) :
        pass
    
    def apply_perspective(self) :
        pass
    
    def resize(self) :
        pass

    def generate_tile(self, image) :
        image_width, image_height = image.size
        x1 = random.randint(0, image_width - self.output_size)
        y1 = random.randint(0, image_height - self.output_size)
        x2 = x1 + self.output_size
        y2 = y1 + self.output_size
     
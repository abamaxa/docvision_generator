from PIL import Image, ImageDraw

from graphics.util import generate_background_color, generate_shade_of_light_grey

class QuestionCompositor :
    def __init__(self, question_image, question_bounds) :
        self.question_image = question_image
        self.question_bounds = question_bounds
        self.background_color = generate_background_color()
        self.page_color = generate_shade_of_light_grey()

        self.question_region = self.question_bounds.region  
        self.composite_image = None
        
    def make_composite_image(self) :
        width = self.question_bounds.width
        height = self.question_bounds.height

        page_width = self.question_image.width
        page_height = self.question_image.height
        
        self.composite_image = Image.new('RGB', (width, height), self.background_color)

        draw = ImageDraw.Draw(self.composite_image)

        page_offset_x = -self.question_bounds.x
        page_offset_y = -self.question_bounds.y

        page_rect = ((page_offset_x, page_offset_y), 
                     (page_offset_x + page_width, page_offset_y + page_height)) 

        draw.rectangle(page_rect, fill=self.page_color)
        del draw

        img_src = self.question_image.crop(self.question_region)

        self.composite_image.paste(img_src, (0,0), img_src) 
        return self.composite_image
        
    @staticmethod 
    def copy_image_from_rect(image, bounds):
        width = bounds.width
        height = bounds.height
        region = bounds.region      
        img = Image.new('RGB', (width, height), generate_shade_of_light_grey())
        
        img_src = image.crop(region)
        
        img.paste(img_src, (0,0), img_src)
        
        return img    

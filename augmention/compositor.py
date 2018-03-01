from PIL import Image, ImageDraw

from question_generator.util import generate_background_color, generate_shade_of_light_grey

class QuestionCompositor :
    def __init__(self, question_image, question_rect) :
        self.question_image = question_image
        self.question_rect = question_rect
        self.background_color = generate_background_color()
        self.page_color = generate_shade_of_light_grey()

        self.question_region = (self.question_rect[0][0], self.question_rect[0][1], 
                                self.question_rect[1][0], self.question_rect[1][1])        

        self.background_image = None
        #self.origin = (-self.question_rect[0][0], -self.question_rect[0][1])

        self.__create_page_background()

    def __create_page_background(self) :
        width = int(self.question_rect[1][0] - self.question_rect[0][0])
        height = int(self.question_rect[1][1] - self.question_rect[0][1])

        page_width = self.question_image.width
        page_height = self.question_image.height

        self.background_image = Image.new('RGB', (width, height), self.background_color)

        draw = ImageDraw.Draw(self.background_image)

        page_offset_x = -self.question_rect[0][0]
        page_offset_y = -self.question_rect[0][1]

        page_rect = ((page_offset_x, page_offset_y), 
                     (page_offset_x + page_width, page_offset_y + page_height)) 

        draw.rectangle(page_rect, fill=self.page_color)
        del draw

        img_src = self.question_image.crop(self.question_region)

        self.background_image.paste(img_src, (0,0), img_src) 
       
    @staticmethod 
    def copy_image_from_rect(image, rect):
        width = rect[1][0] - rect[0][0]
        height = rect[1][1] - rect[0][1]
        region = (rect[0][0], rect[0][1], rect[1][0], rect[1][1])
        
        img = Image.new('RGB', (width, height), generate_shade_of_light_grey())
        
        img_src = image.crop(region)
        
        img.paste(img_src, (0,0), img_src)
        
        return img    

    def get_composite_image(self) :        
        return self.background_image        

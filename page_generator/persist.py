import os
import abc
import io
import zipfile
import json

from PIL import Image

class AbstractPersistence(object) :
    def __init__(self, name, options) :
        self.options = options
        self.counter = 0
        self.dirname = options.get("output_directory", "output")
        self.name = str(name)
        self.image_format = options.get("format", "png")
        
        self.check_directory_exisits()

    def get_meta_data_dict(self, image, frames) :
        meta_data = { 
            "width": image.width,
            "height": image.height,
            "filename": self.get_image_filename(),
        }
        
        frame_list = [frame.as_dict() for frame in frames]            
        meta_data.update({"frames" : frame_list})
        return meta_data
    
    def increment_file_count(self) :
        self.counter += 1
                
    def get_image_filename(self) :
        return os.path.join(self.dirname, 
            "{}-{}.{}".format(self.name, self.counter, self.image_format))
    
    def get_json_filename(self) :
        return os.path.join(self.dirname, 
            "{}-{}.json".format(self.name, self.counter))    
    
    def check_directory_exisits(self) :
        os.makedirs(self.dirname, exist_ok= True)
        
    def get_image_type(self) :
        return self.image_format.upper() == "PNG" and "PNG" or "JPEG"

    def prepare_image(self, image) :
        if self.options["color_model"] == "RGB" :
            return self.__convert_to_rgb(image)
        elif self.options["color_model"] == "HSV" :
            return self.__convert_to_hsv(image)        
    
    def __convert_to_rgb(self, image) :
        if image.mode == "RGB" :
            return image
        return image.convert("RGB")    
        
    def __convert_to_hsv(self, image) :
        image = image.convert("HSV")
        # cannot directly save HSV as a PNG/JPG with PIL so create a
        # new image and tell PIL the images raw bytes are RGB
        return Image.frombytes("RGB", image.size, image.tobytes())
           
    @abc.abstractmethod
    def save_image(self, image, frames) :
        pass
    
    def get_count(self) :
        return self.counter
    
class ZipBufferPersistence(AbstractPersistence) :
    def __init__(self, name, options) :
        super(ZipBufferPersistence, self).__init__(name, options)
        
        self.dirname = ""
        
        self.zip_buffer = io.BytesIO()
        self.zip_filename = self.name + ".zip"
        self.image_zip = zipfile.ZipFile(self.zip_buffer, 'w') 
        
    def save_image(self, image, frames) :
        image = self.prepare_image(image)
        image_buffer = io.BytesIO()
        image.save(image_buffer, self.get_image_type())
        
        self.image_zip.writestr(self.get_image_filename(), 
                       data = image_buffer.getvalue())  
        
        metadata = self.get_meta_data_dict(image, frames)
        json_buffer = json.dumps(metadata, indent=4)
        self.image_zip.writestr(self.get_json_filename(), data = json_buffer)
        
        self.increment_file_count()
        
    def get_zip_buffer(self) :
        return self.zip_buffer   
    
    def get_zip_filename(self) :
        return self.zip_filename
               
class FilePersistence(AbstractPersistence) :        
    def save_image(self, image, frames) :
        image = self.prepare_image(image)
        
        image.save(self.get_image_filename(), self.get_image_type())        
        
        meta_data = self.get_meta_data_dict(image, frames)
        
        self.__save_meta_data(meta_data)
        
        self.increment_file_count()
        
    def __save_meta_data(self, metadata):
        filepath = self.get_json_filename()
        tmp_path = "{}.tmp".format(filepath)
        with open(tmp_path, "w") as jsonfile:
            json.dump(metadata, jsonfile, indent=2)
            
        os.rename(tmp_path, filepath)    

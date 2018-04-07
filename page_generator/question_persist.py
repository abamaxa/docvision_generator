import os
import abc
import io
import zipfile
import json

class AbstractPersistence(object) :
    def __init__(self, name, options) :
        self.options = options
        self.counter = 0
        self.dirname = options.get("outputDir", "output")
        self.name = str(name)
        self.image_format = options.get("format", "png")
        
        self.check_directory_exisits()

    def get_meta_data_dict(self, image, frames) :
        meta_data = { 
            "width": image.width,
            "height": image.height,
            "filename": self.get_image_filename(),
        }
        
        frame_list = []
        for frame in frames :
            frame_list.append({
                "xmin" : frame[0][0][0],
                "ymin" : frame[0][0][1],
                "xmax" : frame[0][1][0],
                "ymax" : frame[0][1][1], 
                "label" : frame[1]
            })
            
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

    def get_rbg_image(self, image) :
        if image.mode == "RGB" :
            return image
        else :
            return image.convert("RGB")        

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
        image = self.get_rbg_image(image)
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
    def __init__(self, name, options) :
        super(FilePersistence, self).__init__(name, options)
        
    def save_image(self, image, frames) :
        image = self.get_rbg_image(image)
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

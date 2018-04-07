import os
import shutil
import logging

# For each image, Yolo uses a text file containing ground truth 
# bounding boxes, stored in a seperate directory
# Training and evalulation data are expected to be in 
# seperate directories

class YoloException(Exception) :
    pass
    
class YoloExport :
    def __init__(self, exporter, is_training) :
        self.overwrite_existing = exporter.overwrite_existing
        if is_training :
            self.data = exporter.training_data
            self.output_dir = exporter.make_output_path('train')
        else :
            self.data = exporter.evaulation_data
            self.output_dir = exporter.make_output_path('eval')
            
    def export(self) :
        self.__prepare_directory()
        self.__make_links()
            
    def __prepare_directory(self) :
        self.__check_and_delete_exisiting_directory()
            
        os.makedirs(self.output_dir)
        
    def __check_and_delete_exisiting_directory(self) :
        if not os.path.exists(self.output_dir) :
            return
        
        if not self.overwrite_existing :
            print("Directory {} already exists"
                  "Any files in this directory will be deleted".format(self.output_dir))
            answer=input("Are you sure you want to overwrite it?"
                         "Answer Y to proceed, anything else to abort:")
            if answer != "Y" :
                raise YoloException("Used cancelled")
            
        shutil.rmtree(self.output_dir)
            
    def __make_links(self) :
        for idx, json_data in enumerate(self.data) :
            if idx % 1000 == 0:
                logging.info('On image %d of %d', idx, len(self.data))
                
            yolo_image = YoloImage(json_data, self.output_dir) 
            yolo_image.write()            
            
class YoloImage :
    def __init__(self, json_data, output_dir) :
        self.output_dir = output_dir
        self.json_data = json_data
        self.labels_records = []
        self.__create_label_records()
        
    def write(self) :
        self.__create_symlink_to_image()
        self.__write_label_records()
    
    def __create_label_records(self) :
        image_width = self.json_data["width"]
        image_height = self.json_data["height"]
        
        for label in self.json_data["frames"] :
            class_name = label["label"]
             
            x = label["xmin"] / image_width
            y = label["ymin"] / image_height
            width = (label["xmin"] - label["xmax"]) / image_width
            height = (label["ymin"] - label["ymax"]) / image_height
           
            label_text = "{} {} {} {} {}".format(class_name, x,y,width,height)
            self.labels_records.append(label_text)
            
        self.labels_records.append("\n")
        
    def __create_symlink_to_image(self) :
        dest_path = os.path.join(self.output_dir, self.json_data["filename"])
        os.symlink(self.json_data["filepath"], dest_path)      
        
    def __write_label_records(self) :
        with open(self.__get_label_record_filename(), "w") as label_file :
            label_file.write("\n".join(self.labels_records))
    
    def __get_label_record_filename(self) :
        base_name = os.path.splitext(self.json_data["filename"])[0]
        return os.path.join(self.output_dir, base_name + ".txt")
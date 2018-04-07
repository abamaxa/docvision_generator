import os
import shutil
import logging

# For each image, Yolo uses a text file containing ground truth 
# bounding boxes, stored in a seperate directory
# Training and evalulation data are expected to be in 
# seperate directories

class YoloException(Exception) :
    pass
    
class YoloLabelExport :
    def __init__(self, exporter) :
        self.output_dir = exporter.output_dir
        self.label_map = exporter.label_map
        self.name = exporter.base_name
        
    def export(self) :
        labels = list(self.label_map.keys())
        labels.sort()
        
        with open(self.__get_label_filepath(), "w") as label_file :
            label_file.write("\n".join(labels))
            
    def __get_label_filepath(self) :
        return os.path.join(self.output_dir, "{}.names".format(self.name))
    
class YoloImageExport :
    def __init__(self, exporter, is_training) :
        self.overwrite_existing = exporter.overwrite_existing
        if is_training :
            self.data = exporter.training_data
            self.output_dir = exporter.make_output_path('train')
        else :
            self.data = exporter.evaulation_data
            self.output_dir = exporter.make_output_path('eval')
            
        self.file_list = []
        self.label_map = exporter.label_map
            
    def export(self) :
        self.__prepare_directories()
        self.__make_links()
        self.__write_file_list()
            
    def __prepare_directories(self) :
        self.__check_and_delete_exisiting_directory()
            
        os.makedirs(self.output_dir)
        os.makedirs(self.__get_label_directory())
        os.makedirs(self.__get_images_directory())
        
    def __get_label_directory(self) :
        return os.path.join(self.output_dir, "labels")
    
    def __get_images_directory(self) :
        return os.path.join(self.output_dir, "images")
    
    def __check_and_delete_exisiting_directory(self) :
        if not os.path.exists(self.output_dir) :
            return
        
        if not self.overwrite_existing :
            print("Directory {} already exists\n" \
                  "Any files in this directory will be deleted".format(self.output_dir))
            answer=input("Are you sure you want to overwrite it?\n"
                         "Answer Y to proceed, anything else to abort:")
            if answer != "Y" :
                raise YoloException("Used cancelled")
            
        shutil.rmtree(self.output_dir)
            
    def __make_links(self) :
        for idx, json_data in enumerate(self.data) :
            if idx % 1000 == 0:
                logging.info('On image %d of %d', idx, len(self.data))
                
            yolo_image = YoloImage(json_data, self.label_map, 
                                   self.__get_label_directory(), 
                                   self.__get_images_directory()) 
            yolo_image.write()    
            self.file_list.append(yolo_image.get_symlink_path())
            
    def __write_file_list(self) :
        with open(self.__get_filelist_path(), "w") as file_list :
            file_list.write("\n".join(self.file_list))
        
    def __get_filelist_path(self) :
        return os.path.join(self.output_dir, "filelist.txt")
            
class YoloImage :
    def __init__(self, json_data, label_map, labels_dir, images_dir) :
        self.labels_dir = labels_dir
        self.images_dir = images_dir
        self.json_data = json_data
        self.labels_records = []
        self.label_map = label_map
        self.__create_label_records()
        
    def write(self) :
        self.__create_symlink_to_image()
        self.__write_label_records()
    
    def __create_label_records(self) :
        image_width = self.json_data["width"]
        image_height = self.json_data["height"]
        
        for label in self.json_data["frames"] :
            class_name = self.label_map[label["label"]]
             
            x = label["xmin"] / image_width
            y = label["ymin"] / image_height
            width = (label["xmax"] - label["xmin"]) / image_width
            height = (label["ymax"] - label["ymin"]) / image_height

            if x < 0 or y < 0 :
                logging.info("Skipping label with invalid x/y")
                continue
            if x + width > 1 or y + height > 1 :
                logging.info("Skipping label with invalid width/height")
                continue

            label_text = "{} {} {} {} {}".format(class_name, x,y,width,height)
            self.labels_records.append(label_text)
            
        self.labels_records.append("\n")
        
    def __create_symlink_to_image(self) :
        dest_path = self.get_symlink_path()
        #os.symlink(self.json_data["filepath"], dest_path)      
        shutil.copyfile(self.json_data["filepath"], dest_path)
    def __write_label_records(self) :
        with open(self.__get_label_record_filename(), "w") as label_file :
            label_file.write("\n".join(self.labels_records))
            
    def get_symlink_path(self) :
        return os.path.join(self.images_dir, self.json_data["filename"])
    
    def __get_label_record_filename(self) :
        base_name = os.path.splitext(self.json_data["filename"])[0]
        return os.path.join(self.labels_dir, base_name + ".txt")

import os
import shutil
import logging

# For each image, ICDAR uses a text file containing ground truth 
# bounding boxes, stored in a seperate directory
# Training and evalulation data are expected to be in 
# seperate directories

class ICDARException(Exception) :
    pass
    
class ICDARImageExport :
    def __init__(self, exporter, is_training) :
        self.overwrite_existing = exporter.overwrite_existing
        if is_training :
            self.data = exporter.training_data
            self.output_dir = exporter.make_output_path('train')
        else :
            self.data = exporter.evaulation_data
            self.output_dir = exporter.make_output_path('eval')
            
        self.file_list = []
            
    def export(self) :
        self.__prepare_directories()
        self.__make_links()
            
    def __prepare_directories(self) :
        self.__check_and_delete_exisiting_directory()
            
        os.makedirs(self.output_dir)
            
    def __check_and_delete_exisiting_directory(self) :
        if not os.path.exists(self.output_dir) :
            return
        
        if not self.overwrite_existing :
            print("Directory {} already exists\n" \
                  "Any files in this directory will be deleted".format(self.output_dir))
            answer=input("Are you sure you want to overwrite it?\n"
                         "Answer Y to proceed, anything else to abort:")
            if answer != "Y" :
                raise ICDARException("Used cancelled")
            
        shutil.rmtree(self.output_dir)
            
    def __make_links(self) :
        for idx, json_data in enumerate(self.data) :
            if idx % 1000 == 0:
                logging.info('On image %d of %d', idx, len(self.data))
                
            icdar_image = ICDARImage(json_data, self.output_dir) 
            icdar_image.write()   
            
class ICDARImage :
    def __init__(self, json_data, output_dir) :
        self.output_dir = output_dir
        self.json_data = json_data
        self.labels_records = []
        self.__create_label_records()
        
    def write(self) :
        self.__create_symlink_to_image()
        self.__write_label_records()
    
    def __create_label_records(self) :        
        for frame in self.json_data["frames"] :
            if frame['type'] != "rotatedbox" :
                continue      

            label_text = u"{x0},{y0},{x1},{y1},{x2},{y2},{x3},{y3},{label}".format_map(frame)
            self.labels_records.append(label_text)
            
        self.labels_records.append("\n")
        
    def __create_symlink_to_image(self) :
        dest_path = self.get_symlink_path()   
        shutil.copyfile(self.json_data["filepath"], dest_path)
        
    def __write_label_records(self) :
        with open(self.__get_label_record_filename(), "w", encoding='utf-8') as label_file :
            label_file.write("\n".join(self.labels_records))
            
    def get_symlink_path(self) :
        return os.path.join(self.output_dir, self.json_data["filename"])
    
    def __get_label_record_filename(self) :
        base_name = os.path.splitext(self.json_data["filename"])[0]
        return os.path.join(self.output_dir, "gt_" + base_name + ".txt")

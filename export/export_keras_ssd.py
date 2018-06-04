import os
import shutil
import logging

# KerasSSD uses a csv text file containing ground truth 
# bounding boxes, class id and path to image. Its fine for
# this to be in the same directory as images. Evaluation and
# training images can reside in the same directory.
# This version leaves the files in place and just generates 
# the csv files

class KerasSSDException(Exception) :
    pass
    
class KerasSSDLabelExport :
    def __init__(self, exporter) :
        self.output_dir = exporter.output_dir
        self.label_map = exporter.label_map
        self.name = exporter.base_name
        
    def export(self) :
        labels = list(self.label_map.keys())
        labels.sort()
        
        with open(self.__get_label_filepath(), "w") as label_file :
            label_file.write("background\n")
            label_file.write("\n".join(labels))
            
    def __get_label_filepath(self) :
        return os.path.join(self.output_dir, "{}.names".format(self.name))
    
class KerasSSDImageExport :
    def __init__(self, exporter, is_training) :
        if is_training :
            self.data = exporter.training_data
            self.label_file = exporter.make_output_path("training.csv")
        else :
            self.data = exporter.evaulation_data
            self.label_file = exporter.make_output_path("eval.csv")

        self.labels_records = []
        self.label_map = exporter.label_map
            
    def export(self) :
        self.__export_labels()
        self.__write_label_file()
                
    def __export_labels(self) :
        for idx, json_data in enumerate(self.data) :
            if idx % 1000 == 0:
                logging.info('On image %d of %d', idx, len(self.data))
                
            self.__write_label_records(json_data)
            
    def __write_label_records(self, json_data) :
        image_width = json_data["width"]
        image_height = json_data["height"]
        image_name = os.path.basename(json_data['filename'])
        
        for label in json_data["frames"] :
            class_name = self.label_map[label["label"]]
             
            xmin = (label["xmin"] / image_width)
            ymin = (label["ymin"] / image_height)
            
            xmax = (label["xmax"] / image_width)
            ymax = (label["ymax"] / image_height)            

            # 'image_name', 'xmin', 'xmax', 'ymin', 'ymax', 'class_id'
            label_text = '"{}",{},{},{},{},{}'.format(image_name,xmin, xmax, ymin, ymax, class_name)
            self.labels_records.append(label_text)
               

    def __write_label_file(self) :
        with open(self.label_file, "w") as file_list :
            file_list.write("\n".join(self.labels_records))

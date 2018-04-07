import logging
import os
import random
import json

class Exporter(object) :
    def __init__(self, commandline_arguments) :
        self._image_dir = os.path.expanduser(commandline_arguments.image_dir)
        self._output_dir = os.path.expanduser(commandline_arguments.output_dir)
        self.args = commandline_arguments
        self._image_list = []
        self._label_map = {}
        self._label_number = 1
        self._num_train = 0
        self._file_list = []
                
        random.seed(42)
        
    @property
    def base_name(self) :   return self.args.name
    
    @property
    def output_dir(self) :  return self._output_dir
        
    @property
    def training_data(self) :  return self._image_list[:self._num_train]
    
    @property
    def evaulation_data(self) :  return self._image_list[self._num_train:]    
    
    @property
    def label_map(self) :   return self._label_map
    
    @property
    def convert_hsv(self) : return self.args.convert_hsv
    
    @property
    def overwrite_existing(self) : return self.args.force
        
    def make_output_path(self, suffix) :
        return os.path.join(self._output_dir, self.base_name + suffix)    
    
    def prepare(self) :
        self.__make_list_of_json_files()
        self.__load_json_data()
        self.__partition_data()
        self.__ensure_output_dir_exists()
        
    def __make_list_of_json_files(self) :
        for filename in os.listdir(self._image_dir) :
            if self.__is_json_data_file(filename) :
                self._file_list.append(filename)        

    def __is_json_data_file(self, filename) :
        if not filename.endswith(".json") :
            return False
        elif filename.endswith("parameters.json") :
            return False    
        elif filename.startswith("._") :
            return False

        return True
    
    def __load_json_data(self):
        for idx, filename in enumerate(self._file_list) :
            if idx % 10000 == 0:
                logging.info('On file %d of %d', idx, len(self._file_list))

            with open(os.path.join(self._image_dir, filename), "r") as fid:
                json_data = json.load(fid)
                
                self.__add_image_file_paths(json_data, filename)
                self.__add_missing_labels(json_data)
                self._image_list.append(json_data)
                
    def __add_image_file_paths(self, json_data, json_filename) :
        json_fileparts = os.path.splitext(os.path.basename(json_filename))
        image_fileparts = os.path.splitext(os.path.basename(json_data['filename']))
        json_data['filename'] = json_fileparts[0] + image_fileparts[1]
        json_data['filepath'] = os.path.join(self._image_dir, json_data['filename'])        

    def __add_missing_labels(self, data) :
        for obj in data.get("frames", []) :
            label = obj["label"]
            if not label in self.label_map.keys() :
                self.label_map[label] = self._label_number
                self._label_number += 1

    def __partition_data(self) :
        random.shuffle(self._image_list)
        num_examples = len(self._image_list)
        self._num_train = int(0.99 * num_examples)

        logging.info('%d training and %d validation examples.',
                 self._num_train, num_examples - self._num_train)
        
    def __ensure_output_dir_exists(self) :
        os.makedirs(self.output_dir, exist_ok=True)

    def create_tensorflow_records(self) :
        from export_tfrecord import TFRecordExport, TFLabelExport
        
        tf_label = TFLabelExport(self)
        tf_label.export()
        
        tf_training = TFRecordExport(self, is_training=True)
        tf_training.export()

        tf_eval = TFRecordExport(self, is_training=False)     
        tf_eval.export()
          
    def create_yolo_files(self) :
        from export_yolo import YoloExport, YoloException
        
        try :
            yolo_training = YoloExport(self, is_training=True)
            yolo_training.export()
            
            yolo_evaluate = YoloExport(self, is_training=False)
            yolo_evaluate.export()    
            
        except YoloException as yolo_except :
            logging.warn(yolo_except.message)
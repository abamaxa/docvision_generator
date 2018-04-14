import logging
import os
import random
import json

class ExporterException(Exception) :
    pass

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
    def overwrite_existing(self) : return self.args.force
    
    @property
    def single(self) : return self.args.single
        
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
                try :
                    json_data = json.load(fid)
                    
                    self.__remove_invalid_boxes(json_data)
                    self.__add_image_file_paths(json_data, filename)
                    self.__add_missing_labels(json_data)
                    self._image_list.append(json_data)
                    
                except ExporterException as e :
                    logging.info(e)
                
    def __remove_invalid_boxes(self, json_data) : 
        frames = []
        width = json_data["width"]
        height = json_data["height"]
        for frame in json_data["frames"] :
            if frame["xmin"] < 0 or frame["ymin"] < 0 :
                continue
            
            if frame["xmax"] > width or frame["ymax"] > height :
                continue   
            
            frames.append(frame)
            
        if not len(frames) :
            raise ExporterException("File contains no valid boxes")
        
        json_data["frames"] = frames
            
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
                if not self.single :
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
        from export_yolo import YoloImageExport, YoloLabelExport, YoloException
        
        try :
            yolo_training = YoloImageExport(self, is_training=True)
            yolo_training.export()
            
            yolo_evaluate = YoloImageExport(self, is_training=False)
            yolo_evaluate.export()    
            
            yolo_labels = YoloLabelExport(self)
            yolo_labels.export()
            
        except YoloException as yolo_except :
            logging.warn(yolo_except)
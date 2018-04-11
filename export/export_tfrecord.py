import hashlib
import io
import logging
import os

import PIL.Image
import tensorflow as tf

from object_detection.utils import dataset_util

class TFException(Exception) :
    pass

class TFLabelExport :
    def __init__(self, exporter) :
        self.label_map = exporter.label_map
        self.label_path = exporter.make_output_path('_label.pbtxt')
        
    def export(self) :
        with open(self.label_path, "w") as label_file :
            for label, _id in self.label_map.items() :
                label_file.write("item {\n  id: %d\n  name: '%s'\n}\n\n" % (_id, label))    

class TFRecordExport :
    def __init__(self, exporter, is_training) :
        self.label_map = exporter.label_map
        
        if is_training :
            self.data = exporter.training_data
            self.output_filename = exporter.make_output_path('_train.record')
        else :
            self.data = exporter.evaulation_data
            self.output_filename = exporter.make_output_path('_val.record')
        
    def export(self):
        writer = tf.python_io.TFRecordWriter(self.output_filename)
        for idx, data in enumerate(self.data):
            if idx % 1000 == 0:
                logging.info('On image %d of %d', idx, len(self.data))

            try:
                example = TFExample(data, self.label_map)
                tf_example = example.create_example()
                writer.write(tf_example.SerializeToString())
            except TFException:
                logging.warn('Invalid example: %s, ignoring.', data.get("filename"))
            except OSError:
                logging.warn('Invalid image: %s, ignoring.', data.get("filename"))
        writer.close()

class TFExample :
    def __init__(self, json_data, label_map) :
        self.json_data = json_data
        self.label_map = label_map

        self.width = int(json_data['width'])
        self.height = int(json_data['height'])
        self.boxes = json_data.get('frames')
        self.filename = json_data['filename'].encode('utf8')
        self.filepath = json_data["filepath"]

        self.xmins = []
        self.ymins = []
        self.xmaxs = []
        self.ymaxs = []
        self.classes = []
        self.classes_text = []
        self.truncated = []
        self.poses = []
        self.difficult_obj = []

        self.key = None
        self.image_bytes = None

    def create_example(self) :
        self.__populate_box_lists()
        self.__read_image()
        self.__check_and_convert_image_format()
        return self.__create_example_from_features()

    def __populate_box_lists(self) :
        for obj in self.boxes:
            xmin = float(obj["xmin"])
            xmax = float(obj["xmax"])
            ymin = float(obj["ymin"])
            ymax = float(obj["ymax"])

            self.xmins.append(xmin / self.width)
            self.ymins.append(ymin / self.height)
            self.xmaxs.append(xmax / self.width)
            self.ymaxs.append(ymax / self.height)

            class_name = obj["label"]

            self.classes_text.append(class_name.encode('utf8'))
            self.classes.append(self.label_map[class_name])
            self.truncated.append(0)
            self.poses.append("Unspecified".encode('utf8'))

    def __read_image(self) :
        with tf.gfile.GFile(self.filepath, 'rb') as fid:
            self.image_bytes = fid.read()

    def __check_and_convert_image_format(self) :
        encoded_jpg_io = io.BytesIO(self.image_bytes)
        image = PIL.Image.open(encoded_jpg_io)
        image_format = image.format

        if not image_format in ('JPEG', "PNG"):
            raise TFException('Image format {} not supported, must be JPEG or PNG'.format(image.format))

        self.image_format = image_format.lower().encode('utf8')

    def __create_example_from_features(self) :
        key = hashlib.sha256(self.image_bytes).hexdigest()

        feature_dict = {
            'image/height': dataset_util.int64_feature(self.height),
            'image/width': dataset_util.int64_feature(self.width),
            'image/filename': dataset_util.bytes_feature(self.filename),
            'image/source_id': dataset_util.bytes_feature(self.filename),
            'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
            'image/encoded': dataset_util.bytes_feature(self.image_bytes),
            'image/format': dataset_util.bytes_feature(self.image_format),
            'image/object/bbox/xmin': dataset_util.float_list_feature(self.xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(self.xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(self.ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(self.ymaxs),
            'image/object/class/text': dataset_util.bytes_list_feature(self.classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(self.classes),
            'image/object/truncated': dataset_util.int64_list_feature(self.truncated),
            'image/object/view': dataset_util.bytes_list_feature(self.poses),
            #'image/object/difficult': dataset_util.int64_list_feature(self.difficult_obj),
        }

        return tf.train.Example(features=tf.train.Features(feature=feature_dict))

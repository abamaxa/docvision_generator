import logging
import argparse

from exporter import Exporter

def main() :
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Create TF Records')

    parser.add_argument('--image_dir', dest='image_dir', action='store', required= True,
                      help='the name of the pipeline config file')    
    parser.add_argument('--output_dir', dest='output_dir', action='store', required= True,
                      default="records", help='the directory to store the records') 
    parser.add_argument('--name', dest='name', action='store', required= True,
                      default="images", help='the file name to use for the record sets')  
    parser.add_argument('--force', dest='force', action='store_true',
                      help='Force overwriting existing files without warning')   
    parser.add_argument('--single', dest='single', action='store_true',
                      help='Use single class to classify objects')       
    parser.add_argument('export_type', help="Specify the type of data to export.\n" \
                        "One of 'tensorflow', 'yolo', 'icdar' or 'keras_ssd'", 
                        choices=("tensorflow", "yolo", "icdar", "keras_ssd"))

    args = parser.parse_args()
    exporter = Exporter(args)

    exporter.prepare()
    if args.export_type == "tensorflow" :
        exporter.create_tensorflow_records()
    elif args.export_type == "yolo" :
        exporter.create_yolo_files()
    elif args.export_type == "keras_ssd" :
        exporter.create_keras_ssd_files()   
    elif args.export_type == "icdar" :
        exporter.create_icdar_files()    

if __name__ == '__main__':
    main()
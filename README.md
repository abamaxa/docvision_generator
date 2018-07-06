# Docvision Generator

## Introduction

This is a tool for generating synthetic text documents for training object detection neural networks. It provides a command line and web interface. The tool can also export the data in YOLO or TFRecord format (for use with Tensorflow).

## Installation

Dependancies can be installed by running the following command.

```shell
$ pip install -r requirements.txt
```

The tool also relies on latex, lmodern and dvipng when can be installed on Ubuntu/Debian based systems with the following command:

```shell
$ sudo apt-get install -y texlive-latex-base dvipng lmodern
```

## Usage

The style and layout of the generated documents are specified in a set of JSON configuration files. A top-level page configuration controls page level parameters such as margins, paddings and fonts. At a lower level, individual blocks of text or graphics (referred to as fragments) are specified in separate JSON files. Each fragment maps to a class of object for use when training an object detection net.

For further details and examples see the page templates and page fragments directories.

The tool can be run from the command line or as web server (see below).

For instance, the following command produces 20 images, 1000 x 600 in size using the specified template file:

```shell
$ python main.py -d 1000 -w 600 -l 1000 --template=template.json 20
```

See the built in help for more options.

## Docker Support

A docker image can be built for running the webserver using the provided Dockerfile:

```shell
$ docker build -t docvision_gen .
```

The following commands tests the docker build by downloading 20 images:

```shell
$ docker run -p 4000:80 docvision_gen --daemon -d 600 -l 600 -w 600 25
$ python webclient.py --url=http://localhost:4000/page --count=20
```

You can uploaded the docker image to your account on docker's public repository:

```shell
$ docker tag docvision_gen your_account_name/docvision_gen:v2.0
$ docker push your_account_name/docvision_gen:v2.0
```
The webclient supports starting and stopping a Google cloud compute instance running the docker image.

For instance, the following command will start a preconfigured Google compute cloud instance, download 20000 images and then stop the instance:

```shell
$ python webclient.py --zone=zone_hosting_your_instance \ --project=your_google_project \
--instance=your_instance_name \
--count=20000
```

## Export

Images can be exported for use with Tensorflow by using the following command (note this script requires the Tensorflow [object_detection](https://github.com/tensorflow/models/tree/master/research/object_detection) and [slim](https://github.com/tensorflow/models/tree/master/research/slim) modules to be on the python path

```shell
$ python export/main.py --image_dir=directory_containing_images \
--output_dir=directory_to_records_to \
--name=a_name_for_the_dataset \
tensorflow
```

and the following to export in YOLO format:

```shell
$ python export/main.py --image_dir=directory_containing_images \
--output_dir=directory_to_records_to \
--name=a_name_for_the_dataset \
yolo
```

## Tests

A comprehensive set of tests can be run using the following command.

```shell
$ python -m unittest discover -p "*_test.py"
```

## License

This software is released under the MIT licence.

## TODO

- Export to PASCAL VOC format
- Further develop web interface as the main method for using the tool.
- Then provide a manual.

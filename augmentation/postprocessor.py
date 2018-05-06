import os
import shutil
import json
import time

import cv2
import numpy as np
import PIL 

def convert_image_to_numpy(image) :
    (im_width, im_height) = image.size
    image_np = np.fromstring(image.tobytes(), dtype='uint8', count=-1, sep='')
    array_shape = (im_height, im_width, int(image_np.shape[0] / (im_height * im_width)))
    return image_np.reshape(array_shape).astype(np.uint8)
 
def convert_numpy_to_image(image_np) :
    image = PIL.Image.fromarray(image_np)
    return image

def postprocess(image, erode_by) :
    kernel = np.ones((erode_by, erode_by), np.uint8)
    if isinstance(image, PIL.Image.Image) :
        image = convert_image_to_numpy(image)
        image = cv2.erode(image, kernel)    
        return convert_numpy_to_image(image)
    else :
        return cv2.erode(image, kernel) 

def save_file(image, original_file, prefix, json_data) :
    new_file = prefix + "E-" + original_file

    cv2.imwrite(new_file, image)

    json_filename = new_file[:-3] + "json"
    json_data["filename"] = new_file

    with open(json_filename, "w") as json_file :
        json.dump(json_data, json_file, indent=4)

def erode_all(save_as_hsv) :
    kernel7 = np.ones((7,7),np.uint8)
    kernel5 = np.ones((5,5),np.uint8)
    kernel3 = np.ones((3,3),np.uint8)
    for file in os.listdir('.') :
        if not file.lower()[-3:] in ("png, ""jpg") :
            continue

        print(file)
        json_filename = file[:-3] + "json"
        with open(json_filename, "r") as json_file :
            json_data = json.load(json_file)

        image = cv2.imread(file)
        if save_as_hsv :
            image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        image3 = cv2.erode(image, kernel3)
        save_file(image3, file, "3", json_data)

        image5 = cv2.erode(image, kernel5)
        save_file(image5, file, "5", json_data)

        #image7 = cv2.erode(image, kernel7)
        #save_file("7E-" + file, image7)

if __name__ == '__main__' :
    erode_all(True)
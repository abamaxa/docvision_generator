import cv2
import numpy as np

def erorde_all(save_as_hsv) :
    kernel = np.ones((7,7),np.uint8)
    for file in os.listdir('.') :
        if not file.lower()[-3:] in ("png, ""jpg") :
            continue
    
        print(file)
        image = cv2.imread(file)
        image = cv2.erode(image, kernel)
        if save_as_hsv :
            image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        cv2.imwrite(file, image)

if __name__ == '__main__' :
    erode_all()
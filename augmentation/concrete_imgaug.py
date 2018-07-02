import imgaug as ia
from imgaug import augmenters as iaa
from PIL import Image
import numpy as np
import cv2

from .base_augmentor import *
from graphics import Bounds, Frame, RotatedFrame

class ImgAugAugmentor(AbstractAugmentor) :
    def __init__(self, page, tiler, options) :
        super(ImgAugAugmentor, self).__init__(page, tiler, options)
        
        ia.seed(abs(page.seed.__hash__()) % 0xFFFFFFFF)
        self.pipeline = None
        self.reset()
        
        self.prepare_pipeline()
        
    def reset(self) :
        self.ia_boxes = None
        self.ia_keypoints = []
        self.frozen_pipeline = None        
        
    def prepare_pipeline(self) :
        self.pipeline = iaa.Sequential(
            [
                self.crop_and_pad(),
                iaa.OneOf([
                    self.perspective(),
                    self.affine()
                ]),
                self.resize(),
                self.piecewise_affine(),
                
                #iaa.Fliplr(0.5)
            ],
            # do all of the above augmentations in random order
            random_order=False
        )    
        
    def sometimes(self, name, augmentation) :
        probability = self.get_parameter(name, PROBABILITY, 0.0)
        return iaa.Sometimes(probability, augmentation) 
    
    def perspective(self) :
        """
        scale : float or tuple of two floats or StochasticParameter, optional(default=0)
        Standard deviation of the normal distributions. These are used to sample
        the random distances of the subimage's corners from the full image's
        corners. The sampled values reflect percentage values (with respect
        to image height/width). Recommended values are in the range 0.0 to 0.1.
            * If a single float, then that value will always be used as the
              scale.
            * If a tuple (a, b) of floats, then a random value will be picked
              from the interval (a, b) (per image).
            * If a StochasticParameter, then that parameter will be queried to
              draw one value per image.

        keep_size : bool, optional(default=True)
            Whether to resize image's back to their original size after applying
            the perspective transform. If set to False, the resulting images
            may end up having different shapes and will always be a list, never
            an array.
        """
        augmentation = iaa.PerspectiveTransform(
            scale=self.get_parameter(PERSPECTIVE, SCALE)
        )
        
        return self.sometimes(PERSPECTIVE, augmentation) 
    
    def affine(self) :
        # Apply affine transformations to some of the images
        # - scale to 80-120% of image height/width (each axis independently)
        # - translate by -20 to +20 relative to height/width (per axis)
        # - rotate by -45 to +45 degrees
        # - shear by -16 to +16 degrees
        # - order: use nearest neighbour or bilinear interpolation (fast)
        # - mode: use any available mode to fill newly created pixels
        #         see API or scikit-image for which modes are available
        # - cval: if the mode is constant, then use a random brightness
        #         for the newly created pixels (e.g. sometimes black,
        #         sometimes white)
        augmentation = iaa.Affine(
            scale=self.get_parameter(AFFINE, SCALE),
            translate_percent=self.get_parameter(AFFINE, TRANSLATE_PERCENT),
            rotate=self.get_parameter(AFFINE, ROTATE),
            shear=self.get_parameter(AFFINE, SHEAR),
            order=self.get_parameter(AFFINE, ORDER),
            cval=self.get_parameter(AFFINE, CVAL),
            mode=["constant"],
        )
        
        return self.sometimes(AFFINE, augmentation)     
    
    def piecewise_affine(self) :
        augmentation = iaa.PiecewiseAffine(
            scale=self.get_parameter(PIECEWISE_AFFINE, SCALE)
        )
        return self.sometimes(PIECEWISE_AFFINE, augmentation) 
    
    def crop_and_pad(self) :
        augmentation = iaa.CropAndPad(
                percent=(self.get_parameter(CROP_AND_PAD,MIN_PERCENT), 
                         self.get_parameter(CROP_AND_PAD,MAX_PERCENT)),
                pad_mode=self.get_parameter(CROP_AND_PAD, PAD_MODE),
                pad_cval=tuple(self.get_parameter(CROP_AND_PAD, CVAL)),
                keep_size = self.get_parameter(CROP_AND_PAD, KEEP_SIZE),
            )
        return self.sometimes(CROP_AND_PAD, augmentation) 
    
    def resize(self) :
        final_size = self.options.get("outputSize")
        return iaa.Scale({"height": final_size[0], "width": final_size[1]},
                         interpolation=cv2.INTER_CUBIC)
       
    def generate_augmented_image(self) : 
        self.convert_image_to_numpy()
        self.freeze_pipeline()
        self.prepare_frames()
                
        self.augment_image()
        self.augment_frames()
                
                
    def freeze_pipeline(self) :
        self.frozen_pipeline = self.pipeline.to_deterministic()
        
    def prepare_frames(self) :
        self.__convert_frames_to_keypoints()
        self.__convert_frames_to_boxes()
            
    def __convert_frames_to_keypoints(self) :
        keypoints = []
        for frame in self.frames :
            if isinstance(frame, Frame) :
                continue
            
            for point in frame :
                keypoints.append(ia.Keypoint(x=int(point[0]),  y=int(point[1])))
                
            if len(keypoints) >= 20 :
                self.ia_keypoints.append(ia.KeypointsOnImage(keypoints, shape=self.image_np.shape))
                keypoints = []
                
        if keypoints :
            self.ia_keypoints.append(ia.KeypointsOnImage(keypoints, shape=self.image_np.shape))        
            
    def __convert_frames_to_boxes(self) :
        boxes = []
        for frame in self.frames :
            if isinstance(frame, RotatedFrame) :
                continue
            
            box = ia.BoundingBox(x1=int(frame.x),  y1=int(frame.y),
                                 x2=int(frame.x2), y2=int(frame.y2))
            boxes.append(box)

        self.ia_boxes = ia.BoundingBoxesOnImage(boxes, shape=self.image_np.shape)
        
    def augment_image(self) :
        # Augment BBs and images.
        # As we only have one image and list of BBs, we use
        # [image] and [bbs] to turn both into lists (batches) for the
        # functions and then [0] to reverse that. In a real experiment, your
        # variables would likely already be lists.
        image_aug = self.frozen_pipeline.augment_images([self.image_np])[0]
        self.set_augmented_image_from_numpy(image_aug)
        
    def augment_frames(self) :
        self.augmented_frames = []

        if self.ia_boxes and self.ia_boxes.bounding_boxes :
            self.ia_boxes = self.frozen_pipeline.augment_bounding_boxes([self.ia_boxes])[0]
            self.augmented_frames = self.__convert_boxes_to_frames()
        
        if self.ia_keypoints :
            self.ia_keypoints = self.frozen_pipeline.augment_keypoints(self.ia_keypoints)[0]
            self.augmented_frames.extend(self.__convert_keypoints_to_frames())
        
    def __convert_boxes_to_frames(self) :
        frames = []   
        for box, frame in zip(self.ia_boxes.bounding_boxes, self.frames) :
            if box.x1 == -1 and box.y1 == -1 :
                continue
            
            bounds = Bounds(box.x1, box.y1, x2 = box.x2, y2 = box.y2)
            frames.append(Frame(bounds, frame.label))
            
        return frames

    def __convert_keypoints_to_frames(self) :
        frames = []   
        points = []
        counter = 0
        invalid_frame = False
        for idx, keypoint in enumerate(self.ia_keypoints.keypoints) :
            points.append((float(keypoint.x), float(keypoint.y)))
            if keypoint.x == -1 and keypoint.y == -1 :
                invalid_frame = True
                
            if idx % 4 == 3 :
                if not invalid_frame :
                    frames.append(RotatedFrame(points, self.frames[counter].label))
                    
                points = []
                counter += 1
                invalid_frame = False

        return frames        
 
   
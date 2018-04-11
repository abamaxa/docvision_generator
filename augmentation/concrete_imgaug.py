import imgaug as ia
from imgaug import augmenters as iaa
from PIL import Image
import numpy as np
import cv2

from .base_augmentor import *
from graphics import Bounds, Frame

class ImgAugAugmentor(AbstractAugmentor) :
    def __init__(self, page, tiler, options) :
        super(ImgAugAugmentor, self).__init__(page, tiler, options)
        
        self.pipeline = None
        self.label_boxes = []
        self.image_np = None
        
        self.prepare_pipeline()
        
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
                        
    def convert_image_to_numpy(self) :
        (im_width, im_height) = self.image.size
        array_shape = (im_height, im_width, 3)
        array_data = self.image.getdata()
        self.image_np = np.array(array_data).reshape(array_shape).astype(np.uint8)    
    
    def prepare_frames(self) :
        self.label_boxes = self.convert_frames_to_boxes(self.frames)
        
    def convert_frames_to_boxes(self, frames) :
        boxes = []
        for frame in frames :
            box = ia.BoundingBox(x1=int(frame.x),  y1=int(frame.y),
                                 x2=int(frame.x2), y2=int(frame.y2))
            boxes.append(box)

        return ia.BoundingBoxesOnImage(boxes, shape=self.image_np.shape)

    def convert_boxes_to_frames(self, bbs) :
        frames = []   
        for box, frame in zip(bbs.bounding_boxes, self.frames) :
            bounds = Bounds(box.x1, box.y1, x2 = box.x2, y2 = box.y2)
            frames.append(Frame(bounds, frame.label))
            
        return frames
    
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

    def generate_augmented_image(self) : 
        self.convert_image_to_numpy()
        self.prepare_frames()
        
        seq_det = self.pipeline.to_deterministic()
        
        # Augment BBs and images.
        # As we only have one image and list of BBs, we use
        # [image] and [bbs] to turn both into lists (batches) for the
        # functions and then [0] to reverse that. In a real experiment, your
        # variables would likely already be lists.
        image_aug = seq_det.augment_images([self.image_np])[0]
        
        self.augmented_frames = []

        if self.frames :
            label_boxes_aug = seq_det.augment_bounding_boxes([self.label_boxes])[0]
            self.augmented_frames = self.convert_boxes_to_frames(label_boxes_aug)          
        
        self.augmented_image = Image.fromarray(image_aug)
                
    def prepare_pipeline_a(self) :
        # Define our sequence of augmentation steps that will be applied to every image.
        self.pipeline = iaa.Sequential(
            [
                #
                # Apply the following augmenters to most images.
                #
                iaa.Fliplr(0.5), # horizontally flip 50% of all images
                iaa.Flipud(0.2), # vertically flip 20% of all images
        
                # crop some of the images by 0-10% of their height/width
                self.sometimes(CROP, iaa.Crop(percent=(0, 0.1))),
        
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
                sometimes(iaa.Affine(
                    scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
                    translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
                    rotate=(-45, 45),
                    shear=(-16, 16),
                    order=[0, 1],
                    cval=(0, 255),
                    mode=ia.ALL
                )),
        
                #
                # Execute 0 to 5 of the following (less important) augmenters per
                # image. Don't execute all of them, as that would often be way too
                # strong.
                #
                iaa.SomeOf((0, 5),
                    [
                        # Convert some images into their superpixel representation,
                        # sample between 20 and 200 superpixels per image, but do
                        # not replace all superpixels with their average, only
                        # some of them (p_replace).
                        sometimes(
                            iaa.Superpixels(
                                p_replace=(0, 1.0),
                                n_segments=(20, 200)
                            )
                        ),
        
                        # Blur each image with varying strength using
                        # gaussian blur (sigma between 0 and 3.0),
                        # average/uniform blur (kernel size between 2x2 and 7x7)
                        # median blur (kernel size between 3x3 and 11x11).
                        iaa.OneOf([
                            iaa.GaussianBlur((0, 3.0)),
                            iaa.AverageBlur(k=(2, 7)),
                            iaa.MedianBlur(k=(3, 11)),
                        ]),
        
                        # Sharpen each image, overlay the result with the original
                        # image using an alpha between 0 (no sharpening) and 1
                        # (full sharpening effect).
                        iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),
        
                        # Same as sharpen, but for an embossing effect.
                        iaa.Emboss(alpha=(0, 1.0), strength=(0, 2.0)),
        
                        # Search in some images either for all edges or for
                        # directed edges. These edges are then marked in a black
                        # and white image and overlayed with the original image
                        # using an alpha of 0 to 0.7.
                        sometimes(iaa.OneOf([
                            iaa.EdgeDetect(alpha=(0, 0.7)),
                            iaa.DirectedEdgeDetect(
                                alpha=(0, 0.7), direction=(0.0, 1.0)
                            ),
                        ])),
        
                        # Add gaussian noise to some images.
                        # In 50% of these cases, the noise is randomly sampled per
                        # channel and pixel.
                        # In the other 50% of all cases it is sampled once per
                        # pixel (i.e. brightness change).
                        iaa.AdditiveGaussianNoise(
                            loc=0, scale=(0.0, 0.05*255), per_channel=0.5
                        ),
        
                        # Either drop randomly 1 to 10% of all pixels (i.e. set
                        # them to black) or drop them on an image with 2-5% percent
                        # of the original size, leading to large dropped
                        # rectangles.
                        iaa.OneOf([
                            iaa.Dropout((0.01, 0.1), per_channel=0.5),
                            iaa.CoarseDropout(
                                (0.03, 0.15), size_percent=(0.02, 0.05),
                                per_channel=0.2
                            ),
                        ]),
        
                        # Invert each image's chanell with 5% probability.
                        # This sets each pixel value v to 255-v.
                        iaa.Invert(0.05, per_channel=True), # invert color channels
        
                        # Add a value of -10 to 10 to each pixel.
                        iaa.Add((-10, 10), per_channel=0.5),
        
                        # Change brightness of images (50-150% of original value).
                        iaa.Multiply((0.5, 1.5), per_channel=0.5),
        
                        # Improve or worsen the contrast of images.
                        iaa.ContrastNormalization((0.5, 2.0), per_channel=0.5),
        
                        # Convert each image to grayscale and then overlay the
                        # result with the original with random alpha. I.e. remove
                        # colors with varying strengths.
                        iaa.Grayscale(alpha=(0.0, 1.0)),
        
                        # In some images move pixels locally around (with random
                        # strengths).
                        sometimes(
                            iaa.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)
                        ),
        
                        # In some images distort local areas with varying strength.
                        sometimes(iaa.PiecewiseAffine(scale=(0.01, 0.05)))
                    ],
                    # do all of the above augmentations in random order
                    random_order=True
                )
            ],
            # do all of the above augmentations in random order
            random_order=True
        )
        
        images_aug = seq.augment_images(images)        

   
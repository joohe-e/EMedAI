# import the necessary packages
import os
import numpy as np
import cv2
from PIL import Image

def create_circle(img, height, width):
    y = height//2
    x = width//2
    h = height//6
    w = width//6
    if width >= height:
        img = cv2.circle(img, (x, y), h, (0, 0, 0), -1)
    if width < height:
        img = cv2.circle(img, (x, y), w, (0, 0, 0), -1)

    return img

impath = "cropped"
outpath = "circled"

#Place black circle in the middle of image
#Attempt to get rid of random feature detection caused by vivid color of characters
for file in os.listdir(impath):
    if not os.path.isdir(os.path.join(impath, file)):
        img = cv2.imread(os.path.join(impath, file), cv2.IMREAD_COLOR)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #
        # mask = filter(hsv)
        # res1 = cv2.bitwise_and(img, img, mask=mask)
        im_height, im_width, channels = img.shape
        res1 = create_circle(img, im_height, im_width)
        # res2 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
        # ret,thresh = cv2.threshold(res2,40,255,cv2.THRESH_BINARY_INV)

        # filename = cl + '_' + file
        # filename = filename.replace("jpg", "tif")
        cv2.imwrite(os.path.join(outpath, file), res1)
# import the necessary packages
import os
import numpy as np
import cv2
from PIL import Image
import pytesseract

def filter(mode):
    lower_red = np.array([0, 40, 70])
    upper_red = np.array([5, 255, 255])
    mask1 = cv2.inRange(mode, lower_red, upper_red)

    lower_red = np.array([175, 40, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(mode, lower_red, upper_red)
    mask1 = mask1 + mask2

    lower_blue = np.array([90, 40, 110])
    upper_blue = np.array([130, 255, 255])
    mask2 = cv2.inRange(mode, lower_blue, upper_blue)
    mask1 = mask1 + mask2

    lower_green = np.array([35, 30, 80])
    upper_green = np.array([85, 255, 255])
    mask2 = cv2.inRange(mode, lower_green, upper_green)
    mask1 = mask1 + mask2

    # lower_yellow = np.array([15, 30, 60])
    # upper_yellow = np.array([30, 200, 255])
    # mask1 = cv2.inRange(mode, lower_yellow, upper_yellow)
    # mask2 = cv2.bitwise_not(mask1)

    mask2 = cv2.bitwise_not(mask1)

    return mask2

impath = "cropped"
outpath = "prepro"

#Pre-processing by removing the character from monitor
#This greatly improve image registration performance by reducing miss detection of image feature
for file in os.listdir(impath):
    if not os.path.isdir(os.path.join(impath, file)):
        img = cv2.imread(os.path.join(impath, file), cv2.IMREAD_COLOR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = filter(hsv)
        res1 = cv2.bitwise_and(img, img, mask=mask)
        # res2 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
        # ret,thresh = cv2.threshold(res2,40,255,cv2.THRESH_BINARY_INV)

        # filename = cl + '_' + file
        # filename = filename.replace("jpg", "tif")
        cv2.imwrite(os.path.join(outpath, file), res1)

# import the necessary packages
import os
import numpy as np
import cv2
from PIL import Image
import pytesseract

def filter(mode, color):
    if color == 'red':
        lower_red = np.array([0, 40, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(mode, lower_red, upper_red)

        lower_red = np.array([170, 40, 70])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(mode, lower_red, upper_red)
        mask1 = mask1 + mask2

    elif color == 'blue':
        lower_blue = np.array([85, 40, 110])
        upper_blue = np.array([130, 255, 255])
        mask1 = cv2.inRange(mode, lower_blue, upper_blue)

    elif color == 'green':
        lower_green = np.array([35, 30, 80])
        upper_green = np.array([85, 255, 255])
        mask1 = cv2.inRange(mode, lower_green, upper_green)

    elif color == 'yellow':
        lower_yellow = np.array([15, 30, 60])
        upper_yellow = np.array([30, 200, 255])
        mask1 = cv2.inRange(mode, lower_yellow, upper_yellow)

    return mask1


impath = "result"
outpath = "characters"
clist = ['red', 'blue', 'green', 'yellow']

#This code is to extract the characters by colors
#Will generate binary form of image with black letters
#You can change the range in filter function to enhance the color detection
for file in os.listdir(impath):
    if not os.path.isdir(os.path.join(impath, file)):
        img = cv2.imread(os.path.join(impath, file), cv2.IMREAD_COLOR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        for cl in clist:
            mask = filter(hsv, cl)
            res1 = cv2.bitwise_and(img, img, mask=mask)
            res2 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(res2,40,255,cv2.THRESH_BINARY_INV)

            filename = cl + '_' + file
            filename = filename.replace("jpg", "tif")
            cv2.imwrite(os.path.join(outpath, filename), thresh)

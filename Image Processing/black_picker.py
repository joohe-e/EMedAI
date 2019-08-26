# import the necessary packages
import os
import numpy as np
import cv2
from PIL import Image
import pytesseract

def filter(mode):
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([255, 255, 77])
    mask1 = cv2.inRange(mode, lower_black, upper_black)

    mask2 = cv2.bitwise_not(mask1)

    return mask2

impath = "result"
outpath = "binary"

for file in os.listdir(impath):
    if not os.path.isdir(os.path.join(impath, file)):
        img = cv2.imread(os.path.join(impath, file), cv2.IMREAD_COLOR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = filter(hsv)
        res1 = cv2.bitwise_and(img, img, mask=mask)
        res2 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(res2,40,255,cv2.THRESH_BINARY_INV)

        # filename = cl + '_' + file
        # file = file.replace("jpg", "tif")
        cv2.imwrite(os.path.join(outpath, file), thresh)
        # cv2.imshow('black', thresh)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

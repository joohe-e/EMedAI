#using orb, working with ref2 (top-down view)
from __future__ import print_function
import cv2
import numpy as np
import os

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15


def alignImages(im1, im2, original):
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    # matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMINGLUT)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    # imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    # cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(original, h, (width, height))

    return im1Reg, h


if __name__ == '__main__':

    inpath = 'prepro' #Any folder contains pre-processed images
    midpath = 'midpro'
    outpath = 'result'
    oripath = 'cropped'
    # refpath = path + '/ref/' + refFilename
    imReference = cv2.imread('ref.jpg', cv2.IMREAD_COLOR)
    im_height, im_width, channels = imReference.shape

    #Unsharp image
    #Can remove if you don't need
    for file in os.listdir(inpath):
        if not os.path.isdir(os.path.join(inpath, file)):
            im = cv2.imread(os.path.join(inpath, file), cv2.IMREAD_COLOR)
            src = cv2.resize(im, dsize=(im_width, im_height), interpolation=cv2.INTER_AREA)
            img = cv2.GaussianBlur(src, (0, 0), 3)
            dst2 = cv2.addWeighted(src, 1.5, img, -0.5, 0, src)
            cv2.imwrite(os.path.join(midpath, file), dst2)

    #Image Registration
    for imFilename in os.listdir(midpath):
        impath = midpath + '/' + imFilename
        tarpath = oripath + '/' + imFilename
        im = cv2.imread(impath, cv2.IMREAD_COLOR)
        target = cv2.imread(tarpath, cv2.IMREAD_COLOR)
        target = cv2.resize(target, dsize=(im_width, im_height), interpolation=cv2.INTER_AREA)
        imReg, h = alignImages(im, imReference, target)
        cv2.imwrite(os.path.join(outpath, imFilename), imReg)
#another
from ast import main
import numpy as np
import cv2 as cv
import glob
import imutils
import matplotlib.pyplot as plt
import os

def stitch_images(image_paths):

    images = []
    for image in image_paths:
        img=cv.imread(image)
        images.append(img)
    imageStitcher=cv.Stitcher_create()
    error, stitched_img=imageStitcher.stitch(images)
    stitched_img = cv.resize(stitched_img, (600, 500), interpolation=cv.INTER_AREA)
    if not error:
        return stitched_img

# main_image=cv.imread('StitchedOutput.jpg', cv.IMREAD_UNCHANGED)
# gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
# haar_cascade = cv.CascadeClassifier('cascade.xml')
# faces_rect = haar_cascade.detectMultiScale(gray_image, 1.1, 9, None)
# for (x,y,w,h) in faces_rect:
#     cv.rectangle(main_image, (x,y), (x+w, y+h), (0,255,0), 2)
    
# cv.imwrite('test.jpg', main_image)



# template =cv.imread('SeaStar.jpg',0)
# SeaStar=cv.imread('SeaStar.jpg', cv.IMREAD_UNCHANGED)
# result=cv.matchTemplate(grey_img, template, cv.TM_CCORR_NORMED)

# cv.imshow("res", result)

# threshold=0.99
# locations=np.where(result>=threshold)

# locations=list(zip(*locations[::-1]))

# print(locations)

# for loc in locations:
#     cv.rectangle(img, loc, (loc[0]+w, loc[1]+h),(0,0,255),2)
#     cv.imshow('all matches', main_image)
#     cv.waitKey()
#else:
#   print('not found')
#another
import numpy as np
import cv2
import glob
import imutils
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
image_paths = glob.glob('unstitched/*.jpg')
images=[]

for image in image_paths:
    img=cv2.imread(image)
    images.append(img)
    #cv2.imshow("Image", img)
    #cv2.waitKey(0)

imageStitcher=cv2.Stitcher_create()
error = cv2.Stitcher_create()

error, stitched_img=imageStitcher.stitch(images)

if not error:
    cv2.imwrite("StitchedOutput.png", stitched_img)
    cv2.imshow("StitchedImage", stitched_img)
    cv2.waitKey(0)



main_image=cv2.imread('StitchedOutput.jpg', cv2.IMREAD_UNCHANGED)
grey_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

template =cv2.imread('SeaStar.jpg',0)
SeaStar=cv2.imread('SeaStar.jpg', cv2.IMREAD_UNCHANGED)
result=cv2.matchTemplate(grey_img, template, cv2.TM_CCORR_NORMED)

cv2.imshow("res", result)

threshold=0.99
locations=np.where(result>=threshold)

locations=list(zip(*locations[::-1]))

print(locations)

for loc in locations:
    cv2.rectangle(img, loc, (loc[0]+w, loc[1]+h),(0,0,255),2)
    cv2.imshow('all matches', main_image)
    cv2.waitKey()
#else:
#   print('not found')
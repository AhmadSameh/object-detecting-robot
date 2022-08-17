import cv2
import numpy as np

im1=cv2.imread('im0.png')
im2=cv2.imread('im1.png')
img1=cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
img2=cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

orb=cv2.ORB_create(50)
kp1, des1= orb.detectAndCompute(img1, None)
kp2, des2=orb.detectAndCompute(img2, None)

#takes descriptor in first set and matches it with all other features in
#second set
matcher=cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

matches=matcher.match(des1,des2,None)

#i'm sorting the keypoints extracted
matches=sorted(matches,key=lambda x:x.distance )

#preprocessing homography by RANSAC
points1=np.zeros((len(matches),2),dtype=np.float32)
points2=np.zeros((len(matches),2),dtype=np.float32)

for i,match in enumerate(matches):
    points1[i,:]=kp1[match.queryIdx].pt
    points2[i,:]=kp2[match.trainIdx].pt

h,mask=cv2.findHomography(points1, points2, cv2.RANSAC)

#homography
height, width, channels=im2.shape
im1Reg=cv2.warpPerspective(im1, h, (width,height))

#img3=cv2.drawKeypoints(img1, kp1, None, flags=None)
img3=cv2.drawMatches(im2, kp1, im2, kp2, matches[:10], None)

cv2.imshow("keypoint matches",img3)
#cv2.imshow("Registered image", im1Reg)

cv2.waitKey(0)
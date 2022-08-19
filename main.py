import cv2
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from scipy.ndimage import shift
from matplotlib import pyplot as plt

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


#we could use FLANN to match
#FLANN_INDEX_KDTREE = 1
#index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
#search_params = dict(checks=50)   # or pass empty dictionary
#flann = cv.FlannBasedMatcher(index_params, search_params)
#matches = flann.knnMatch(des1, des2, k=2)

#preprocessing homography by RANSAC
points1=np.zeros((len(matches),2),dtype=np.float32)
points2=np.zeros((len(matches),2),dtype=np.float32)

for i,match in enumerate(matches):
    #we could use Lowe to pick best matches
    points1[i,:]=kp1[match.queryIdx].pt
    points2[i,:]=kp2[match.trainIdx].pt

h,mask=cv2.findHomography(points1, points2, cv2.RANSAC)

FM,inliers= cv2.findFundamentalMat(points1,points2,cv2.FM_LMEDS)

#img3=cv2.drawKeypoints(img1, kp1, None, flags=None)
img3=cv2.drawMatches(im2, kp1, im2, kp2, matches[:10], None)

cv2.imshow("keypoint matches",img3)
pts1 = points1[inliers.ravel() == 1]
pts2 = points2[inliers.ravel() == 1]

def drawlines(img1, img2, lines, pts1, pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r, c = img1.shape
    img1color = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2color = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    # Edit: use the same random seed so that two images are comparable!
    np.random.seed(0)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2]/r[1]])
        x1, y1 = map(int, [c, -(r[2]+r[0]*c)/r[1]])
        img1color = cv2.line(img1color, (x0, y0), (x1, y1), color, 1)
        #img1color = cv2.circle(img1color, tuple(pt1), 5, color, -1)
        #img2color = cv2.circle(img2color, tuple(pt2), 5, color, -1)
    return img1color, img2color

#find corresponding epilines
lines1 = cv2.computeCorrespondEpilines(
    pts2.reshape(-1, 1, 2), 2, FM)
lines1 = lines1.reshape(-1, 3)
img5, img6 = drawlines(img1, img2, lines1, pts1, pts2)



# Find epilines corresponding to points in left image (first image) and
# drawing its lines on right image
lines2 = cv2.computeCorrespondEpilines(
    pts1.reshape(-1, 1, 2), 1, FM)
lines2 = lines2.reshape(-1, 3)
img3, img4 = drawlines(img2, img1, lines2, pts2, pts1)

plt.subplot(121), plt.imshow(img5)
plt.subplot(122), plt.imshow(img3)
plt.suptitle("Epilines in both images")
plt.show()

#used to find homography matrix H1 and H2
h1, w1 = img1.shape
h2, w2 = img2.shape
_, H1, H2 = cv2.stereoRectifyUncalibrated(
    np.float32(pts1), np.float32(pts2), FM, imgSize=(w1, h1)
)

#homography
height, width, channels=im2.shape
im1Reg=cv2.warpPerspective(im1, H1, (width,height))
im2Reg=cv2.warpPerspective(im2, H2, (width,height))
cv2.imwrite("undistorted_L.png", im1Reg)
cv2.imwrite("undistorted_R.png", im2Reg)
#stereobm is based on SAD algorithm

cv2.imshow("Registered image1", im1Reg)
cv2.imshow("Registered image2", im2Reg)
cv2.waitKey(0)

i1=cv2.imread('undistorted_L.png', 0)
i2=cv2.imread("undistorted_R.png", 0)
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity_BM = stereo.compute(img1,img2)
plt.imshow(disparity_BM, "gray")
plt.colorbar()
plt.show()


block_size = 11
min_disp = -128
max_disp = 128
num_disp = max_disp - min_disp
uniquenessRatio = 5
speckleWindowSize = 200
speckleRange = 2
disp12MaxDiff = 0
stereo = cv2.StereoSGBM_create(
    minDisparity=min_disp,
    numDisparities=num_disp,
    blockSize=block_size,
    uniquenessRatio=uniquenessRatio,
    speckleWindowSize=speckleWindowSize,
    speckleRange=speckleRange,
    disp12MaxDiff=disp12MaxDiff,
    P1=8 * 1 * block_size * block_size,
    P2=32 * 1 * block_size * block_size,
)
disparity_SGBM = stereo.compute(img1, img2)

# Normalize the values to a range from 0..255 for a grayscale image
disparity_SGBM = cv2.normalize(disparity_SGBM, disparity_SGBM, alpha=255,
                              beta=0, norm_type=cv2.NORM_MINMAX)
disparity_SGBM = np.uint8(disparity_SGBM)
cv2.imshow("Disparity", disparity_SGBM)
cv2.imwrite("disparity_SGBM_norm.png", disparity_SGBM)
cv2.waitKey()
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

sift = cv2.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

imgSift = cv2.drawKeypoints(
    img1, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("SIFT Keypoints", imgSift)



FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Keep good matches: calculate distinctive image features
# Lowe, D.G. Distinctive Image Features from Scale-Invariant Keypoints. International Journal of Computer Vision 60, 91–110 (2004). https://doi.org/10.1023/B:VISI.0000029664.99615.94
# https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf
matchesMask = [[0, 0] for i in range(len(matches))]
good = []
pts1 = []
pts2 = []

for i, (m, n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        # Keep this keypoint pair
        matchesMask[i] = [1, 0]
        good.append(m)
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)
draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask[300:500],
                   flags=cv2.DrawMatchesFlags_DEFAULT)

keypoint_matches = cv2.drawMatchesKnn(
    img1, kp1, img2, kp2, matches[300:500], None, **draw_params)
cv2.imshow("Keypoint matches", keypoint_matches)
cv2.imwrite('matches.png',keypoint_matches)

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
FM, inliers = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)

# We select only inlier points
pts1 = pts1[inliers.ravel() == 1]
pts2 = pts2[inliers.ravel() == 1]

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
        img1color = cv2.circle(img1color, tuple(pt1), 5, color, -1)
        img2color = cv2.circle(img2color, tuple(pt2), 5, color, -1)
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
img1_rectified = cv2.warpPerspective(img1, H1, (w1, h1))
img2_rectified = cv2.warpPerspective(img2, H2, (w2, h2))
cv2.imwrite("rectified_1.png", img1_rectified)
cv2.imwrite("rectified_2.png", img2_rectified)
#stereobm is based on SAD algorithm

cv2.imshow("Registered image1", img1_rectified)
cv2.imshow("Registered image2", img2_rectified)
cv2.waitKey(0)

i1=cv2.imread('rectified_1.png', 0)
i2=cv2.imread("rectified_2.png", 0)
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity_BM = stereo.compute(i1,i2)
plt.imshow(disparity_BM, "gray")
plt.colorbar()
plt.show()
#im_color = cv2.applyColorMap(disparity_BM, cv2.COLORMAP_JET)



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
disparity_SGBM = stereo.compute(i1, i2)

# Normalize the values to a range from 0..255 for a grayscale image
disparity_SGBM = cv2.normalize(disparity_SGBM, disparity_SGBM, alpha=255,
                              beta=0, norm_type=cv2.NORM_MINMAX)
disparity_SGBM = np.uint8(disparity_SGBM)
cv2.imshow("Disparity", disparity_SGBM)
cv2.imwrite("disparity_SGBM_norm.png", disparity_SGBM)

image = cv2.imread('disparity_SGBM_norm.png', 0)
colormap = plt.get_cmap('inferno')
heatmap = (colormap(image) * 2**16).astype(np.uint16)[:,:,:3]
heatmap = cv2.cvtColor(heatmap, cv2.COLOR_RGB2BGR)

cv2.imshow('image', image)
cv2.imshow('heatmap', heatmap)
cv2.imwrite("heatmap.png", heatmap)
cv2.waitKey(0)
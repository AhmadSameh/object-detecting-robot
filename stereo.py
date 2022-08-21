import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from PIL import Image as im


def stereo_match(imgL, imgR):
    # disparity range is tuned for 'aloe' image pair
    window_size = 15
    min_disp = 16
    num_disp = 96 - min_disp
    stereo = cv.StereoSGBM_create(minDisparity=min_disp,
                                   numDisparities=num_disp,
                                   blockSize=16,
                                   P1=8 * 3 * window_size ** 2,
                                   P2=32 * 3 * window_size ** 2,
                                   disp12MaxDiff=1,
                                   uniquenessRatio=10,
                                   speckleWindowSize=150,
                                   speckleRange=32
                                   )

    # print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    # print('generating 3d point cloud...',)
    h, w = imgL.shape[:2]
    f = 0.8 * w  # guess for focal length
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h],  # turn points 180 deg around x-axis,
                    [0, 0, 0, -f],  # so that y-axis looks up
                    [0, 0, 1, 0]])
    points = cv.reprojectImageTo3D(disp, Q)
    colors = cv.cvtColor(imgL, cv.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    #append_ply_array(out_points, out_colors)

    disparity_scaled = (disp - min_disp) / num_disp
    disparity_scaled += abs(np.amin(disparity_scaled))
    disparity_scaled /= np.amax(disparity_scaled)
    disparity_scaled[disparity_scaled < 0] = 0
    return np.array(255 * disparity_scaled, np.uint8)

def drawlines(img1, img2, lines, pts1, pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r, c = img1.shape
    img1color = cv.cvtColor(img1, cv.COLOR_GRAY2BGR)
    img2color = cv.cvtColor(img2, cv.COLOR_GRAY2BGR)
    # Edit: use the same random seed so that two images are comparable!
    np.random.seed(0)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2]/r[1]])
        x1, y1 = map(int, [c, -(r[2]+r[0]*c)/r[1]])
        img1color = cv.line(img1color, (x0, y0), (x1, y1), color, 1)
        img1color = cv.circle(img1color, tuple(pt1), 5, color, -1)
        img2color = cv.circle(img2color, tuple(pt2), 5, color, -1)
    return img1color, img2color


def stereo_vision(locations):
    im1=cv.imread(locations[0])
    im2=cv.imread(locations[1])
    img1=cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
    img2=cv.cvtColor(im2, cv.COLOR_BGR2GRAY)

    sift = cv.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    imgSift = cv.drawKeypoints(
        img1, kp1, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv.imshow("SIFT Keypoints", imgSift)



    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params, search_params)
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
                    flags=cv.DrawMatchesFlags_DEFAULT)

    keypoint_matches = cv.drawMatchesKnn(
        img1, kp1, img2, kp2, matches[300:500], None, **draw_params)
    #cv.imshow("Keypoint matches", keypoint_matches)
    cv.imwrite('matches.png',keypoint_matches)

    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    FM, inliers = cv.findFundamentalMat(pts1, pts2, cv.FM_RANSAC)

    # We select only inlier points
    pts1 = pts1[inliers.ravel() == 1]
    pts2 = pts2[inliers.ravel() == 1]



    #find corresponding epilines
    lines1 = cv.computeCorrespondEpilines(
        pts2.reshape(-1, 1, 2), 2, FM)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = drawlines(img1, img2, lines1, pts1, pts2)



    # Find epilines corresponding to points in left image (first image) and
    # drawing its lines on right image
    lines2 = cv.computeCorrespondEpilines(
        pts1.reshape(-1, 1, 2), 1, FM)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = drawlines(img2, img1, lines2, pts2, pts1)

    #plt.subplot(121), plt.imshow(img5)
    #plt.subplot(122), plt.imshow(img3)
    #plt.suptitle("Epilines in both images")
    #plt.show()

    #used to find homography matrix H1 and H2
    h1, w1 = img1.shape
    h2, w2 = img2.shape
    _, H1, H2 = cv.stereoRectifyUncalibrated(
        np.float32(pts1), np.float32(pts2), FM, imgSize=(w1, h1)
    )

    #homography
    img1_rectified = cv.warpPerspective(img1, H1, (w1, h1))
    img2_rectified = cv.warpPerspective(img2, H2, (w2, h2))
    cv.imwrite("rectified_1.png", img1_rectified)
    cv.imwrite("rectified_2.png", img2_rectified)
    #stereobm is based on SAD algorithm

    #cv.imshow("Registered image1", img1_rectified)
    #cv.imshow("Registered image2", img2_rectified)
    #cv.waitKey(0)

    i1=cv.imread('rectified_1.png', 0)
    i2=cv.imread("rectified_2.png", 0)
    stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
    disparity_BM = stereo.compute(i1,i2)
    #plt.imshow(disparity_BM, "gray")
    #plt.colorbar()
    #plt.show()
    #im_color = cv.applyColorMap(disparity_BM, cv.COLORMAP_JET)



    block_size = 11
    min_disp = -128
    max_disp = 128
    num_disp = max_disp - min_disp
    uniquenessRatio = 5
    speckleWindowSize = 200
    speckleRange = 2
    disp12MaxDiff = 0
    stereo = cv.StereoSGBM_create(
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
    disparity_SGBM = cv.normalize(disparity_SGBM, disparity_SGBM, alpha=255,
                                beta=0, norm_type=cv.NORM_MINMAX)
    disparity_SGBM = np.uint8(disparity_SGBM)
    #cv.imshow("Disparity", disparity_SGBM)
    cv.imwrite("disparity_SGBM_norm.png", disparity_SGBM)

    image = cv.imread('disparity_SGBM_norm.png', 0)
    colormap = plt.get_cmap('inferno')
    heatmap = (colormap(image) * 2**16).astype(np.uint16)[:,:,:3]
    heatmap = cv.cvtColor(heatmap, cv.COLOR_RGB2BGR)



    array=stereo_match(i1,i2)
    np.set_printoptions(threshold=sys.maxsize)
    #print(array)
    #a 3d map
    data = im.fromarray(array)
    data.save('depthimage.png')
    #cv.imshow('disparityimage', image)
    #cv.imshow('heatmapdisparity', heatmap)
    final = cv.resize(heatmap, (600, 500), interpolation=cv.INTER_AREA)
    cv.imwrite("heatmapdisparity.png", heatmap)
    cv.imwrite("final.png", final)
    

    # image = cv.imread('depthimage.png', 0)
    # colormap = plt.get_cmap('inferno')
    # heatmapdepth = (colormap(image) * 2**16).astype(np.uint16)[:,:,:3]
    # heatmapdepth = cv.cvtColor(heatmap, cv.COLOR_RGB2BGR)
    # #cv.imshow("heatmapdepth", heatmapdepth)
    # cv.waitKey(0)
    
import numpy as np
import cv2 as cv

def detect(img):
    image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    lower = np.array([15, 150, 20])
    higher = np.array([35, 255, 255])
    mask = cv.inRange(image, lower, higher)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv.contourArea(contour) > 2500:
            x, y, w, h = cv.boundingRect(contour)
            cv.putText(img, "CORAL FRAGMENT", (x, y), cv.QT_FONT_NORMAL, 3, 0)
            cv.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 3)

    lower = np.array([110, 90, 20])
    higher = np.array([140, 255, 255])
    mask = cv.inRange(image, lower, higher)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv.contourArea(contour) > 4000:
            x, y, w, h = cv.boundingRect(contour)
            cv.putText(img, "SEA STAR", (x, y), cv.QT_FONT_NORMAL, 3, 0)
            cv.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 3)

    lower = np.array([150, 100, 20])
    higher = np.array([170, 255, 255])
    mask = cv.inRange(image, lower, higher)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv.contourArea(contour) > 3000:
            x, y, w, h = cv.boundingRect(contour)
            cv.putText(img, "CORAL COLONY", (x, y), cv.QT_FONT_NORMAL, 3, 0)
            cv.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 3)

    lower = np.array([100, 0, 20])
    higher = np.array([130, 50, 255])
    mask = cv.inRange(image, lower, higher)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv.contourArea(contour) > 3000:
            x, y, w, h = cv.boundingRect(contour)
            cv.putText(img, "SPONGE", (x, y), cv.QT_FONT_NORMAL, 3, 0)
            cv.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 3)
    
    return img

def stitch_images(image_paths):
    images = []
    for image in image_paths:
        img=cv.imread(image)
        images.append(img)
    imageStitcher=cv.Stitcher_create()
    error, stitched_img=imageStitcher.stitch(images)
    final = detect(stitched_img)
    final = cv.resize(final, (600, 500), interpolation=cv.INTER_AREA)
    if not error:
        return final

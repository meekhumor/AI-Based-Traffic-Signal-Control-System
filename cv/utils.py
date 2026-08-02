import cv2 as cv
import numpy as np

def contours_detector(img):
    """
    Detect contours in an image and return dilate mask with contour count.
    """
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blank = np.zeros(img.shape[:2], dtype='uint8')
    blurred_image = cv.GaussianBlur(gray, (5, 5), 0)

    edges = cv.Canny(blurred_image, 50, 150)

    contours, _ = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    count = len(contours)

    cv.drawContours(blank, contours, -1, (255), thickness=2)
    blank = cv.dilate(blank, (3, 3), iterations=1)

    return blank, count


def crop_image(image, top, left, right):
    """
    Crop an image based on trapezoidal lane landmark points top, left, right.
    """
    polygon = np.array([
        [0, image.shape[0]],
        [left[0], left[1]],
        [top[0], top[1]],
        [right[0], right[1]],
        [image.shape[1], image.shape[0]]
    ], np.int32)
    polygon = polygon.reshape((-1, 1, 2))

    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv.fillPoly(mask, [polygon], 255)

    masked_image = cv.bitwise_and(image, image, mask=mask)

    x, y, w, h = cv.boundingRect(polygon)
    cropped_image = masked_image[y:y+h, x:x+w]

    return cropped_image

import cv2 as cv
import numpy as np
from cv.utils import contours_detector, crop_image


def background_contour(video_path, top, left, right): 
    cap = cv.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return 0

    vehicle_counts = []
    last_10_counts = [] 
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
        frame = cv.resize(frame, (800, 600))

        if frame_count % 10 == 0:  
            cropped_image = crop_image(frame, top, left, right)
            _, count = contours_detector(cropped_image)

            last_10_counts.append(count)
            if len(last_10_counts) > 10:
                last_10_counts.pop(0)  

            avg_vehicle_count = int(np.mean(last_10_counts))
            vehicle_counts.append(avg_vehicle_count)

        frame_count += 1

    cap.release()

    if vehicle_counts:
        back_contours = np.min(vehicle_counts) - 20
    else:
        back_contours = 0

    return back_contours

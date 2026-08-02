import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from cv.lane_detector import detect_lane
from cv.background_contour import background_contour
from cv.utils import contours_detector, crop_image


def run_vehicle_counter(video_path='videos/road.mp4'):
    top, left, right = detect_lane(video_path)
    if top is None:
        print("Error: Could not detect lane landmarks.")
        return []

    back_contour = background_contour(video_path, top, left, right)

    cap = cv.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return []

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
            cv.line(frame, (top[0], top[1]), (left[0], left[1]), (255, 0, 0), 2)
            cv.line(frame, (top[0], top[1]), (right[0], right[1]), (0, 255, 0), 2)
            cv.circle(frame, (top[0], top[1]), 5, (255, 255, 255), -1)

            cropped_image = crop_image(frame, top, left, right)
            _, count = contours_detector(cropped_image)

            last_10_counts.append(count)
            if len(last_10_counts) > 10:
                last_10_counts.pop(0)  

            avg_vehicle_count = int(np.mean(last_10_counts))
            real_count = max(0, int((avg_vehicle_count - back_contour) / 8))

            cv.putText(frame, f'Vehicle Count: {real_count}', (20, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            vehicle_counts.append(real_count)

            cv.imshow("Vehicle Count", frame)

        frame_count += 1

        if cv.waitKey(1) & 0xFF == ord('q'):
            break  

    cap.release()
    cv.destroyAllWindows()

    if vehicle_counts:
        plt.figure(figsize=(10, 5))
        plt.plot(vehicle_counts, marker='o')
        plt.xlabel('Frame Count (per 10 frames)')
        plt.ylabel('Vehicle Count (Moving Average)')
        plt.title('Vehicle Count Over Time')
        plt.show()

    return vehicle_counts


if __name__ == '__main__':
    run_vehicle_counter()

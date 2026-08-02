import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from ultralytics import YOLO
from cv.utils import contours_detector, crop_image


def run_yolo_counter(video_path='videos/road.mp4'):
    cap = cv.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30
    frame_interval = max(1, int(fps * 0.1))  

    vehicle_counts = []
    timestamps = []

    model = YOLO('yolov8n.pt') 

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)  

        if frame_count % frame_interval == 0:
            yolo_vehicle_count = 0
            results = model(frame)
        
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls) 
                    label = result.names[cls_id]
                    if label in ['car', 'truck', 'bus', 'motorbike']:
                        yolo_vehicle_count += 1

            current_time = datetime.now().strftime('%H:%M:%S')
            timestamps.append(current_time)

            top = (538, 891)
            right = (1079, 1491)
            left = (0, 1727)

            cropped_image = crop_image(frame, top, left, right)
            blank, count = contours_detector(cropped_image)
            blank = cv.resize(blank, (500, 700))
            frame = cv.resize(frame, (500, 700))

            calculated_count = max(0, int((count - 400) / 20))
            cv.putText(blank, f'Vehicle Count: {calculated_count}', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            vehicle_counts.append(calculated_count)

            yolo_crop = cv.resize(cropped_image, (500, 700))
            cv.putText(yolo_crop, f'Vehicle Count: {yolo_vehicle_count}', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv.imshow('yolo', yolo_crop)
            cv.imshow("main", frame)
            cv.imshow("edge", blank)

        frame_count += 1

        if cv.waitKey(1) & 0xFF == ord('q'):
            break  

    cap.release()
    cv.destroyAllWindows()

    if timestamps:
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps[::10], vehicle_counts[::10], marker='o')
        plt.xlabel('Time')
        plt.ylabel('Vehicle Count')
        plt.title('Vehicle Count Over Time')
        plt.show()


if __name__ == '__main__':
    run_yolo_counter()

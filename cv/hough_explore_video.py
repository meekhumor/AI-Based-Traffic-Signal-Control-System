import cv2
import numpy as np

video_path = 'videos/road.mp4' 
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  
    frame = cv2.resize(frame, (800, 600))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    left_lane_lines = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6)  

            if -0.7 < slope < -0.4:  
                left_lane_lines.append((x1, y1, x2, y2))
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue for left lane

    cv2.imshow('Edges', edges)
    cv2.imshow('Lane Detection', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

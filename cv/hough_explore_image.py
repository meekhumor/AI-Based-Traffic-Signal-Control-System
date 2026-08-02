import cv2
import numpy as np

img = cv2.imread('Images/03/9.jpg')
if img is not None:
    img = cv2.resize(img, (800, 600))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    edges_resized = cv2.resize(edges, (800, 600))
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    left_lane_lines = []
    right_lane_lines = []
    red_lane_lines = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6) 
            
            slope_text = f"{slope:.2f}"
            cv2.putText(img, slope_text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            if slope < -0.4:  
                left_lane_lines.append((x1, y1, x2, y2))
                cv2.putText(img, slope_text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            if slope > 0.3:  
                right_lane_lines.append((x1, y1, x2, y2))
                cv2.putText(img, slope_text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            if -0.1 < slope < 0.1:
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)  
                cv2.putText(img, slope_text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    print("Left lines:", left_lane_lines)
    print("Right lines:", right_lane_lines)
    print("Red lines:", red_lane_lines)

    for x1, y1, x2, y2 in left_lane_lines:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue for left lane

    for x1, y1, x2, y2 in right_lane_lines:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green for right lane

    cv2.imshow('Edges', edges_resized)  
    cv2.imshow('Lane Detection', img)   

    cv2.waitKey(0)
    cv2.destroyAllWindows()

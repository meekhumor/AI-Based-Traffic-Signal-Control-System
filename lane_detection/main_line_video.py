import cv2
import numpy as np

cap = cv2.VideoCapture('videos/rush.mp4')  

frame_count = 0
stored_lines = {'blue': None, 'red': None, 'green': None}

def extend_line(x1, y1, x2, y2, width, height):
    if x1 == x2:
        return (x1, 0, x1, height)
    
    m = (y2 - y1) / (x2 - x1 + 1e-6)
    c = y1 - m * x1

    points = []
    y_left = round(c)
    if 0 <= y_left <= height:
        points.append((0, y_left))

    y_right = round(m * width + c)
    if 0 <= y_right <= height:
        points.append((width, y_right))

    x_top = round(-c / m) if m != 0 else None
    if x_top is not None and 0 <= x_top <= width:
        points.append((x_top, 0))

    x_bottom = round((height - c) / m) if m != 0 else None
    if x_bottom is not None and 0 <= x_bottom <= width:
        points.append((x_bottom, height))

    if len(points) >= 2:
        return points[0] + points[1]
    return None  

def get_line_intersection(bx1, by1, bx2, by2, rx1, ry1, rx2, ry2):
    A1, B1, C1 = by2 - by1, bx1 - bx2, (by2 - by1) * bx1 + (bx1 - bx2) * by1
    A2, B2, C2 = ry2 - ry1, rx1 - rx2, (ry2 - ry1) * rx1 + (rx1 - rx2) * ry1
    det = A1 * B2 - A2 * B1

    if det == 0:
        return None  

    ix, iy = int((C1 * B2 - C2 * B1) / det), int((A1 * C2 - A2 * C1) / det)

    if (min(bx1, bx2) <= ix <= max(bx1, bx2) and min(by1, by2) <= iy <= max(by1, by2) and
        min(rx1, rx2) <= ix <= max(rx1, rx2) and min(ry1, ry2) <= iy <= max(ry1, ry2)):
        return (ix, iy)
    return None  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  
    
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  
    frame = cv2.resize(frame, (800, 600))
    height, width = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    if frame_count % 10 == 0:
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        left_lane_lines, right_lane_lines, red_lane_lines = [], [], []

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1 + 1e-6)  

                if slope < -0.4:
                    left_lane_lines.append((x1, y1, x2, y2))
                elif slope > 0.3:
                    right_lane_lines.append((x1, y1, x2, y2))
                elif -0.1 <= slope <= 0.1:
                    red_lane_lines.append((x1, y1, x2, y2))

        stored_lines['blue'] = min(left_lane_lines, key=lambda line: min(line[0], line[2]), default=None)
        stored_lines['red'] = min(red_lane_lines, key=lambda line: min(line[1], line[3]), default=None)
        stored_lines['green'] = max(right_lane_lines, key=lambda line: max(line[0], line[2]), default=None)
    
    blue_line = stored_lines['blue']
    red_line = stored_lines['red']
    green_line = stored_lines['green']

    if red_line:
        x1, y1, x2, y2 = red_line
        rx1, ry1, rx2, ry2 = extend_line(x1, y1, x2, y2, width, height)  
        cv2.line(frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 3)  
        rmx, rmy = int((rx1 + rx2) / 2), int((ry1 + ry2) / 2)

    if blue_line:
        x1, y1, x2, y2 = blue_line
        bx1, by1, bx2, by2 = extend_line(x1, y1, x2, y2, width, height)  
        intersection = get_line_intersection(bx1, by1, bx2, by2, rx1, ry1, rx2, ry2)
        if intersection:
            ix, iy = intersection
            px, py = int((ix + rmx) / 2), int((iy + rmy) / 2)
            if bx1 < bx2:
                left = (bx1, by1)
            else:
                left = (bx2, by2)
            
            cv2.line(frame, left, (px, py), (255, 0, 0), 3) 
            cv2.circle(frame, (px, py), 6, (255, 255, 255), -1)

    if green_line:
        x1, y1, x2, y2 = green_line
        gx1, gy1, gx2, gy2 = extend_line(x1, y1, x2, y2, width, height)  
        if gx1 > gx2:
            right = (gx1, gy1)
        else:
            right = (gx2, gy2)
        
        cv2.line(frame, right, (px, py), (0, 255, 0), 3)

    cv2.imshow('Lane Detection', frame)
    frame_count += 1

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()

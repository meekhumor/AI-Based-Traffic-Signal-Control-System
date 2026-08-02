import cv2
import numpy as np


def detect_lane(video_path):
    cap = cv2.VideoCapture(video_path)  

    frame_count = 0
    all_lines = {'blue': [], 'red': [], 'green': []}

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

    def compute_average_lane_lines(all_lines):
        final_lines = {}
        
        for color in ['blue', 'red', 'green']:
            if all_lines[color]:
                avg_x1 = int(np.mean([line[0] for line in all_lines[color]]))
                avg_y1 = int(np.mean([line[1] for line in all_lines[color]]))
                avg_x2 = int(np.mean([line[2] for line in all_lines[color]]))
                avg_y2 = int(np.mean([line[3] for line in all_lines[color]]))
                final_lines[color] = (avg_x1, avg_y1, avg_x2, avg_y2)
        
        return final_lines

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

            if left_lane_lines:
                all_lines['blue'].append(min(left_lane_lines, key=lambda line: min(line[0], line[2])))
            if red_lane_lines:
                all_lines['red'].append(min(red_lane_lines, key=lambda line: min(line[1], line[3])))
            if right_lane_lines:
                all_lines['green'].append(max(right_lane_lines, key=lambda line: max(line[0], line[2])))
        
        frame_count += 1

    final_lines = compute_average_lane_lines(all_lines)

    def get_line_intersection(bx1, by1, bx2, by2, rx1, ry1, rx2, ry2):
        A1 = by2 - by1
        B1 = bx1 - bx2
        C1 = A1 * bx1 + B1 * by1

        A2 = ry2 - ry1
        B2 = rx1 - rx2
        C2 = A2 * rx1 + B2 * ry1

        det = A1 * B2 - A2 * B1

        if det == 0:
            return None  

        ix = int((C1 * B2 - C2 * B1) / det)
        iy = int((A1 * C2 - A2 * C1) / det)

        if (min(bx1, bx2) <= ix <= max(bx1, bx2) and min(by1, by2) <= iy <= max(by1, by2) and
            min(rx1, rx2) <= ix <= max(rx1, rx2) and min(ry1, ry2) <= iy <= max(ry1, ry2)):
            return (ix, iy)
        else:
            return None  

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return None, None, None

    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  
    frame = cv2.resize(frame, (800, 600))
    height, width = frame.shape[:2]

    bx1, by1, bx2, by2 = 0, 0, 0, 0
    rx1, ry1, rx2, ry2 = 0, 0, 0, 0
    gx1, gy1, gx2, gy2 = 0, 0, 0, 0

    for color, line in final_lines.items():
        ext = extend_line(*line, width, height)
        if ext is None:
            continue
        x1, y1, x2, y2 = ext
        if color == 'blue':
            bx1, by1, bx2, by2 = x1, y1, x2, y2
        elif color == 'red':
            rx1, ry1, rx2, ry2 = x1, y1, x2, y2
        elif color == 'green':
            gx1, gy1, gx2, gy2 = x1, y1, x2, y2

    cap.release()

    rmx, rmy = int((rx1 + rx2) / 2), int((ry1 + ry2) / 2)
    intersection = get_line_intersection(bx1, by1, bx2, by2, rx1, ry1, rx2, ry2)
    if intersection is not None:
        ix, iy = intersection
        px, py = int((ix + rmx) / 2), int((iy + rmy) / 2)
    else:
        px, py = rmx, rmy

    left = (bx1, by1) if bx1 < bx2 else (bx2, by2)
    right = (gx1, gy1) if gx1 > gx2 else (gx2, gy2)
    top = (px, py)

    return top, left, right

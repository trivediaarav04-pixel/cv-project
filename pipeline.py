import cv2
import numpy as np

def make_coordinates(image, line_parameters):
    if line_parameters is None:
        return None
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * 0.6)
    if abs(slope) < 1e-3:
        return None
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit, right_fit = [], []
    
    # Check if no lines were detected at all
    if lines is None:
        return None

    for line in lines:
        # Reshape or flatten line safely
        line = np.array(line).reshape(-1)
        if len(line) != 4:
            continue
        x1, y1, x2, y2 = line
        
        if x1 == x2:
            continue
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope, intercept = parameters[0], parameters[1]
        
        if abs(slope) < 0.3:  # Filter out near-horizontal lines
            continue
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_avg = np.average(left_fit, axis=0) if len(left_fit) > 0 else None
    right_avg = np.average(right_fit, axis=0) if len(right_fit) > 0 else None

    left_line = make_coordinates(image, left_avg)
    right_line = make_coordinates(image, right_avg)
    
    output_lines = [l for l in [left_line, right_line] if l is not None]
    return np.array(output_lines) if output_lines else None

def region_of_interest(image):
    height, width = image.shape[:2]
    polygons = np.array([
        [(int(width * 0.1), height), 
         (int(width * 0.45), int(height * 0.6)), 
         (int(width * 0.55), int(height * 0.6)), 
         (int(width * 0.9), height)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    return cv2.bitwise_and(image, mask)

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(line_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 10)
    return line_image

def process_frame(frame):
    if frame is None:
        return None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    cropped_canny = region_of_interest(canny)
    lines = cv2.HoughLinesP(
        cropped_canny, 2, np.pi / 180, 100, 
        np.array([]), minLineLength=40, maxLineGap=5
    )
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    return cv2.addWeighted(frame, 0.8, line_image, 1.0, 1)
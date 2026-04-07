import cv2
import math
import numpy as np
from PIL import Image
from src.utils import dump_img

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def is_square(cnt):
    area = cv2.contourArea(cnt)
    if not (area > 5000 and area < 15000):
        return False
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

    x, y, w, h = cv2.boundingRect(approx)

    aspect_ratio = float(w) / h

    if 0.9 <= aspect_ratio <= 1.1:
        rect_area = w*h
        extent = float(area) / rect_area
        if extent > 0.9:
            return True
    
    return False

def get_midpoint(square):
    x, y, w, h = cv2.boundingRect(square)
    center = (x + w // 2, y + h // 2)
    return center

def find_one_square(img, small_crop):
    avg_color = cv2.mean(small_crop)
    green, blue, red, alpha = avg_color
    is_candidate_tile = not (red > 230 or green < 180)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh_method = cv2.THRESH_BINARY_INV if is_candidate_tile else cv2.THRESH_BINARY
    a, thresh = cv2.threshold(gray, 230, 255, thresh_method)
    dump_img(thresh, "thresh.png")
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx == 4):
            x, y, w, h = cv2.boundingRect(approx)
            area = w * h
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2 and w*h > 300:
                if is_candidate_tile:
                    ret = (x+7, y+7, w-14, h-14)
                else:
                    ret = (x+2, y+2, w-4, h-4)
                return ret
    
    raise ValueError


def refine_tiles(img, curr_tiles):
    pass
    refined = []
    for tile in curr_tiles:
        (x, y, w, h) = tile
        p = 10
        h_img, w_img = img.shape[:2]
        y1 = max(0, y - p)
        y2 = min(h_img, y + h + p)
        x1 = max(0, x - p)
        x2 = min(w_img, x + w + p)
        small_crop = img[y:y+h, x:x+w]
        large_crop = img[y1:y2, x1:x2]
        dump_img(small_crop, "small_crop.png")
        dump_img(large_crop, "large_crop.png")
        sub_box = find_one_square(large_crop, small_crop)
        (lx, ly, lw, lh) = sub_box
        refined_crop = large_crop[lx:lx+lw, ly:ly+lh]
        dump_img(refined_crop, "refined_crop.png")
        global_x = x1 + lx
        global_y = y1 + ly
        refined.append((global_x, global_y, lw, lh))

    return refined#curr_tiles

def get_tiles(img, debug=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    blurred = cv2.GaussianBlur(gray, (3,3), 0)
    kernel = np.ones((5,5), np.uint8)
    eroded = cv2.erode(blurred, kernel, iterations=1)
    edges1 = cv2.Canny(blurred, 20, 100)
    edges2 = cv2.Canny(eroded, 20, 100)
    contours1, _ = cv2.findContours(edges1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(edges2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours1 = list(contours1)
    contours2 = list(contours2)
    contours1.extend(contours2)
    contours = tuple(contours1)
    squares = {get_midpoint(cnt): cnt for cnt in contours if is_square(cnt)}

    unique_squares = {}
    pixel_tolerance = 20
    for mid, sq in squares.items():
        is_duplicate = False
        for existing_mid in unique_squares.keys():
            if distance(mid, existing_mid) < pixel_tolerance:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_squares[mid] = sq

    unique_squares = list(unique_squares.values())
    final_squares = []
    for square in unique_squares:
        midpoint = get_midpoint(square)
        roi = img[midpoint[1]-2 : midpoint[1]+2, midpoint[0]-2:midpoint[0]+2]
        avg_color = cv2.mean(roi)[:3]
        if not all(c > 245 for c in avg_color):
            final_squares.append(cv2.boundingRect(square))

    if debug:
        output_img = img.copy()
        for square in final_squares:
            x, y, w, h = cv2.boundingRect(square)
            cv2.rectangle(output_img, (x, y), (x+w, y+h), (0, 0, 255), 2)

        img_rgb = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
        
        pil_img = Image.fromarray(img_rgb)
        pil_img.save("output_file.png")

    refined_squares = refine_tiles(img, final_squares)
    return refined_squares
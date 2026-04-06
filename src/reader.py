import cv2
import math
import numpy as np
import easyocr
import os
from PIL import Image, ImageOps
import pytesseract

img = None
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def shrink_img(img):
    return cv2.resize(img, (0,0), fx=0.3, fy=0.3)

def display_img(img, shrink=False):
    if shrink:
        cv2.imshow("Preview", shrink_img(img))
    else:
        cv2.imshow("Preview", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def is_square(cnt):
    area = cv2.contourArea(cnt)
    if area > 5000 and area < 15000:
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

def get_tiles(img, debug=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    blurred = cv2.GaussianBlur(gray, (3,3), 0)
    kernel = np.ones((5,5), np.uint8)
    eroded = cv2.erode(blurred, kernel, iterations=1)
    edges1 = cv2.Canny(eroded, 20, 100)
    edges2 = cv2.Canny(blurred, 20, 100)
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
            final_squares.append(square)

    if debug:
        output_img = img.copy()
        for square in final_squares:
            x, y, w, h = cv2.boundingRect(square)
            cv2.rectangle(output_img, (x, y), (x+w, y+h), (0, 0, 255), 2)

        img_rgb = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
        
        pil_img = Image.fromarray(img_rgb)
        pil_img.save("output_file.png")

    return final_squares

def prepare_for_ocr(crop, inset=6):
    crop = crop[inset: -inset, inset: -inset]    
    gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    resized_crop = cv2.resize(gray_crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    blurred_crop = cv2.medianBlur(resized_crop, 7)
    _, op_crop = cv2.threshold(blurred_crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blurred_num_crop = cv2.medianBlur(resized_crop, 3)
    _, num_crop = cv2.threshold(blurred_num_crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return (op_crop, num_crop)

reader = easyocr.Reader(['en'])
image_idx = 0
def do_ocr(img, can_be_operator=True, debug_nums=False):
    op_crop, num_crop = img
    global image_idx
    op_crop = Image.fromarray(op_crop)
    op_crop = ImageOps.expand(op_crop, border=(0, 10, 0, 10), fill='white')
    if debug_nums:
        debug_num = Image.fromarray(num_crop)
        debug_num.save(f"test_images/n{image_idx}.png")
        image_idx += 1

    if can_be_operator:
        result = pytesseract.image_to_string(op_crop, config=r'--oem 3 --psm 10 -c tessedit_char_whitelist=')
        result = result.strip()
        if result == '/':
            return result
        result = pytesseract.image_to_string(op_crop, config=r'--oem 3 --psm 13 -c tessedit_char_whitelist=+-x=')
        result = result.strip()
        if result in ['+', '-', 'x', '=']:
            if result == 'x':
                return '*'
            return result
    results = reader.readtext(num_crop, detail=0, paragraph=False, rotation_info=[0], allowlist='0123456789 ')
    if len(results) > 0:
        return results[0]
    return ''
    

def get_values(bounding_boxes):
    values = []
    for box in bounding_boxes:
        x, y, w, h = box
        can_be_operator = not (y > 1350)
        cell_crop = img[y:y+h, x:x+w]
        avg_cell_color = np.mean(cell_crop, axis=(0, 1))
        if avg_cell_color[0] > 180 and can_be_operator:
            values.append('')
            continue
        ocr_ready = prepare_for_ocr(cell_crop)
        cell_contents = do_ocr(ocr_ready, can_be_operator=can_be_operator)
        values.append(cell_contents)
        #print(avg_cell_color, cell_contents)
    return values

def print_grid(np_grid, max_len=4):
    for row in np_grid:
        print(" ".join(f"{str(item):^{max_len}}" for item in row))

def read_img(image):
    global img
    img = image
    tiles = get_tiles(img)
    bounding_boxes = [cv2.boundingRect(tile) for tile in tiles]
    values = get_values(bounding_boxes)

    # Grid reconstruction
    coords = {(box[0], box[1]):values[idx] for idx,box in enumerate(bounding_boxes)}

    sol_tiles = {coord:v for coord,v in coords.items() if coord[1] > 1350}
    grid_tiles = {coord:v for coord,v in coords.items() if not coord in sol_tiles}
    min_x = min([t[0] for t in grid_tiles.keys()])
    min_y = min([t[1] for t in grid_tiles.keys()])

    new_grid_tiles = {}
    for idx, tile in enumerate(grid_tiles.keys()):
        new_grid_tiles[(tile[0]-min_x, tile[1]-min_y)] = grid_tiles[tile]

    grid_tiles = new_grid_tiles

    y_diff = min([t[1] for t in grid_tiles if t[1] > 5])
    x_diff = min([t[0] for t in grid_tiles if t[0] > 5])

    new_grid_tiles = {}
    for tile in grid_tiles.keys():
        tile_x = round(tile[0] / x_diff)
        tile_y = round(tile[1] / y_diff)
        new_grid_tiles[(tile_x, tile_y)] = grid_tiles[tile]

    grid_tiles = new_grid_tiles
    available_nums = [int(x) for x in sol_tiles.values()]
    n = 1
    for k,v in grid_tiles.items():
        if v == '':
            grid_tiles[k] = f'n{n}'
            n += 1
    cols = max(c[0]+1 for c in grid_tiles.keys())
    rows = max(c[1]+1 for c in grid_tiles.keys())
    grid = np.full((rows, cols), "", dtype='U10')
    for k,v in grid_tiles.items():
        x = k[1]
        y = k[0]
        grid[x,y] = np.str_(v)
    return available_nums, grid

if __name__ == "__main__":
    img = cv2.imread("puzzle1.png")
    available_nums, grid = read_img(img)
    print_grid(grid)
    print("Available nums", available_nums)
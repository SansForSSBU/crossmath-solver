import cv2
import math
import numpy as np
import easyocr
import os
from PIL import Image, ImageOps
import pytesseract
import sys
from src.tile_detector import get_tiles
from src.optical_character_recognition import ocr
from src.game_board import GameBoard

MAX_TILE_NUM_DIGITS = 3
VALID_OPERATORS = ["+", "-", "/", "x", "="]

img = None

def get_values(bounding_boxes, generate_ocr_golden_records=False):
    values = []
    for box in bounding_boxes:
        x, y, w, h = box
        can_be_operator = not (y > 1350)
        cell_crop = img[y:y+h, x:x+w]
        avg_cell_color = np.mean(cell_crop, axis=(0, 1))
        if avg_cell_color[0] > 180 and can_be_operator:
            values.append('')
            continue
        cell_contents = ocr(cell_crop, can_be_operator=can_be_operator, generate_golden_records=generate_ocr_golden_records)
        values.append(cell_contents)
    return values

def reconstruct_grid(grid_tiles):
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
    return GameBoard(grid)

def parse_tile_text(tile_text, can_be_operator=True):
    if str.isdigit(tile_text) and len(tile_text) <= MAX_TILE_NUM_DIGITS:
        return int(tile_text)
    elif can_be_operator and tile_text in VALID_OPERATORS:
        return tile_text
    else:
        raise ValueError(f"Invalid tile: {tile_text}")

def read_img(path, generate_ocr_golden_records=False):
    global img
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Could not find image at {path}")
    if image.shape != (2160, 1080, 3):
        raise ValueError("Provided image was not 1080x2160")
    img = image
    tiles = get_tiles(img)
    bounding_boxes = [cv2.boundingRect(tile) for tile in tiles]
    values = get_values(bounding_boxes, generate_ocr_golden_records=generate_ocr_golden_records)

    # Grid reconstruction
    coords = {(box[0], box[1]):values[idx] for idx,box in enumerate(bounding_boxes)}

    candidate_nums = [v for coord,v in coords.items() if coord[1] > 1350]
    candidate_nums = [parse_tile_text(x, can_be_operator=False) for x in candidate_nums]
    grid_tiles = {coord:v for coord,v in coords.items() if coord[1] <= 1350}
    grid = reconstruct_grid(grid_tiles)
    
    return candidate_nums, grid
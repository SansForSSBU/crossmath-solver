from src.main import solve_img
from src.optical_character_recognition import ocr
import numpy as np
from pathlib import Path
import os
import json
import cv2
import easyocr

def test_golden_records_img2solution():
    puzzles_dir = Path("test/puzzles")
    for img_path in puzzles_dir.iterdir():
        print(f"Solving image {img_path.name}")
        solved_board = solve_img(img_path)
        solution_path = f"./test/solutions/{img_path.stem}.npy"
        
        old_ans = np.load(solution_path)
        assert np.array_equal(solved_board.np_grid, old_ans)
        print(f"{img_path.name} passed match test")

def test_ocr_golden_records():
    image_folder_path = "test/ocr_golden_records/images"
    key_path = "test/ocr_golden_records/key.json"
    with open(key_path, "r") as f:
        key = json.load(f)
    for image_path in Path.iterdir(Path(image_folder_path)):
        reader = easyocr.Reader(['en'])
        name = image_path.stem.split(".")[0]
        can_be_operator, answer = key[name]
        img = cv2.imread(image_path)
        assert ocr(img, reader, can_be_operator=can_be_operator) == answer
    pass
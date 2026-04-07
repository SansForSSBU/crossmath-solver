from pathlib import Path
from src.main import solve_img
import numpy as np
import os

def generate_golden_records(overwrite_img2solution=False, generate_ocr_golden_records=False):
    puzzles_dir = Path("test/puzzles")
    for img_path in puzzles_dir.iterdir():
        solution_path = f"./test/solutions/{img_path.stem}.npy"
        solved_board = solve_img(img_path, generate_ocr_golden_records=generate_ocr_golden_records)
        if overwrite_img2solution or not os.path.exists(solution_path):
            print(f"Solving image {img_path.name}")
            np.save(solution_path, solved_board.np_grid)

if __name__ == "__main__":
    # TODO: These should be command-line arguments
    overwrite_img2solution = False
    generate_ocr_golden_records=True
    generate_golden_records(overwrite_img2solution=overwrite_img2solution, generate_ocr_golden_records=generate_ocr_golden_records)

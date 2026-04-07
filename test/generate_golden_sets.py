from pathlib import Path
from src.main import solve_img
import numpy as np
import os

def generate_golden_records(overwrite_img2solution=False, generate_ocr_golden_records=False):
    puzzles_dir = Path("test/puzzles")
    for img_path in puzzles_dir.iterdir():
        solution_path = f"./test/solutions/{img_path.stem}.npy"
        # If there's no reason to calculate the solution here, skip it to save some time
        if (not overwrite_img2solution and not generate_ocr_golden_records) and os.path.exists(solution_path):
            continue
        print(f"Solving image {img_path.name}")
        solved_board = solve_img(img_path, generate_ocr_golden_records=generate_ocr_golden_records)
        if overwrite_img2solution or not os.path.exists(solution_path):
            np.save(solution_path, solved_board.np_grid)

if __name__ == "__main__":
    # TODO: These should be command-line arguments
    overwrite_img2solution = False
    generate_ocr_golden_records=False
    generate_golden_records(overwrite_img2solution=overwrite_img2solution, generate_ocr_golden_records=generate_ocr_golden_records)

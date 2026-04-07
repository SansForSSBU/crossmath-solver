from pathlib import Path
from src.main import solve_img
import numpy as np
import os

def generate_golden_records_img2solution(overwrite=False):
    puzzles_dir = Path("test/puzzles")
    for img_path in puzzles_dir.iterdir():
        solution_path = f"./test/solutions/{img_path.stem}.npy"
        if overwrite or not os.path.exists(solution_path):
            print(f"Solving image {img_path.name}")
            solved_board = solve_img(img_path)
            np.save(solution_path, solved_board.np_grid)

if __name__ == "__main__":
    overwrite_img2solution = False # TODO: These should be command-line arguments
    generate_golden_records_img2solution(overwrite=overwrite_img2solution)
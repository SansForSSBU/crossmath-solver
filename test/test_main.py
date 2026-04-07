from src.main import solve_img
import numpy as np
from pathlib import Path
import os

def test_puzzles():
    puzzles_dir = Path("test/puzzles")
    for img_path in puzzles_dir.iterdir():
        print(f"Solving image {img_path.name}")
        solved_board = solve_img(img_path)
        solution_path = f"./test/solutions/{img_path.stem}.npy"
        if os.path.exists(Path(solution_path)):
            old_ans = np.load(solution_path)
            assert np.array_equal(solved_board.np_grid, old_ans)
            print(f"{img_path.name} passed match test")
        else:
            np.save(solution_path, solved_board.np_grid)
            print(f"Saved new solution for {img_path.name}")
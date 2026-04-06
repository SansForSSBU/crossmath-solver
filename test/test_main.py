from src.main import solve_img
import numpy as np
from pathlib import Path
import os

def test_puzzles():
    puzzles_dir = Path("test/puzzles")
    for img_path in puzzles_dir.iterdir():
        ans = solve_img(img_path)
        solution_path = f"./test/solutions/{img_path.stem}.npy"
        if os.path.exists(Path(solution_path)):
            old_ans = np.load(solution_path)
            assert np.array_equal(ans, old_ans)
            print(f"{img_path.name} passed match test")
        else:
            np.save(solution_path, ans)
            print(f"Saved new solution for {img_path.name}")
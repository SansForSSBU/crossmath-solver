from src.main import solve_img
import numpy as np
from pathlib import Path
import os

def test_puzzles():
    img_path = "./test/puzzles/1.png"
    ans = solve_img(img_path)
    solution_path = "./test/solutions/1.npy"
    if os.path.exists(Path("./test/solutions/1.npy")):
        old_ans = np.load(solution_path)
        assert np.array_equal(ans, old_ans)
    else:
        np.save(solution_path, ans)
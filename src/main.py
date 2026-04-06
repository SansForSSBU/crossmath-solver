from src.reader import read_img, print_grid
from src.solver import solve
import cv2
import sys
import argparse

def solve_img(path):
    img = cv2.imread(path)
    available_nums, grid = read_img(img)
    if img is None:
        print(f"Could not find or open image at {path}")
        sys.exit(1)
    ans = solve(available_nums, grid)
    for k,v in ans.items():
        mask = (grid == k)
        grid[mask] = v
    return grid

def main():
    parser = argparse.ArgumentParser(description="Crossmath solver")
    parser.add_argument("path", help="Path to puzzle image")
    args = parser.parse_args()
    result = solve_img(args.path)
    print_grid(result)

if __name__ == "__main__":
    main()
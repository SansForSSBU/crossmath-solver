from src.reader import read_img
from src.solver import solve
import cv2
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Crossmath solver")
    parser.add_argument("path", help="Path to puzzle image")
    return parser.parse_args()

def solve_img(path, generate_ocr_golden_records=False):
    available_nums, game_board = read_img(path, generate_ocr_golden_records=generate_ocr_golden_records)
    answers = solve(available_nums, game_board)
    game_board.substitute_answers(answers)
    return game_board

def main():
    args = parse_args()
    solved_board = solve_img(args.path)
    solved_board.print()

if __name__ == "__main__":
    main()
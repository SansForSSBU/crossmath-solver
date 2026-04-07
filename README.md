# crossmath-solver

Solver for the mobile crossword/math game crossmath.

This solver has been tested on 20 puzzles from the game.

It uses computer vision to read the puzzles from the image then solves it and prints out the solution.

# Demo Video

[![Watch the demo](https://img.youtube.com/vi/lENMmO1ahg0/0.jpg)](https://www.youtube.com/watch?v=lENMmO1ahg0)

# Setup

You must be running Linux for these instructions to work

From root of repository:

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

`sudo apt install tesseract-ocr`

# Usage

Input images must be of the game in fullscreen and at the resolution 1080x2160

From root of repository and whilst inside venv:

`python3 -m src.main <puzzle_image_path>`


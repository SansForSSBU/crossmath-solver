# Demo Video

https://github.com/user-attachments/assets/5dcad881-6ea0-4573-bb15-2b2796b1949c

# Explanation

Solver for the mobile crossword/math game crossmath using computer vision and optical character recognition

This solver has been tested on 20 puzzles from the game.

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


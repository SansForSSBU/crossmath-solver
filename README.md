# crossmath-solver

> **Note:** This project is currently a **Work in Progress**. 
> It is designed specifically for **Linux** environments.
> Input images must be screenshots of the game in 1080x2160 resolution
> Even on these input images, the program will still sometimes fail.

# Setup

From root of repository:

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

`sudo apt install tesseract-ocr`

# Usage

From root of repository and whilst inside venv:

`python3 -m src.main <puzzle_image_path>`

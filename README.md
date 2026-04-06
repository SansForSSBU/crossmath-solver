# crossmath-solver

> **Note:** This project is currently a **Work in Progress**. 
> It is designed specifically for **Linux** environments and has only been 
> verified using the sample image provided in this repository.

# Setup

From root of repository:

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

`sudo apt install tesseract-ocr`

# Usage

From root of repository and whilst inside venv:

`python3 -m src.main <puzzle_image_path>`

# Testing

python3 -m pytest -s
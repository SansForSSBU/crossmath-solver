import cv2
from reader import read_img, print_grid

img = cv2.imread("puzzle1.png")
available_nums, grid = read_img(img)
print_grid(grid)
print("Available nums", available_nums)
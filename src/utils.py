import cv2
import os
from PIL import Image
from pathlib import Path

def dump_img(cv2_img, name="output_file.png"):
    output_dir = Path("debug_images")
    output_dir.mkdir(parents=True, exist_ok=True)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    pil_img.save(f"debug_images/{name}")
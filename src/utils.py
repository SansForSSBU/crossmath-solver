import cv2
from PIL import Image

def dump_img(cv2_img, name="output_file.png"):
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    pil_img.save(name)
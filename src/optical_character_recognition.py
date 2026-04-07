import easyocr
from PIL import Image, ImageOps
import pytesseract
import cv2
import json
from src.utils import dump_img
import numpy as np
from scipy.ndimage import label

reader = easyocr.Reader(['en'])

image_idx = 0
ocr_key = {}
def ocr(crop, can_be_operator=True, generate_golden_records=False):
    global image_idx
    global ocr_key
    dump_img(crop, "ocr_before.png")
    ocr_ready = prepare_for_ocr(crop)
    dump_img(ocr_ready[0], "ocr_preprocessed_0.png")
    dump_img(ocr_ready[1], "ocr_preprocessed_1.png")
    cell_contents = do_ocr(ocr_ready, can_be_operator=can_be_operator)
    print(cell_contents)
    if generate_golden_records:
        image_folder_path = "test/ocr_golden_records/images"
        key_path = "test/ocr_golden_records/key.json"
        rgb_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_crop)
        pil_image.save(f"{image_folder_path}/{image_idx}.png")
        ocr_key[image_idx] = (can_be_operator, cell_contents)
        with open(key_path, "w") as f:
            json.dump(ocr_key, f, indent=4)
        image_idx += 1

    return cell_contents

def shave_whitespace(img, padding=5):
    coords = np.argwhere(img < 200)

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    h, w = img.shape[:2]
    y0 = max(0, y0 - padding)
    y1 = min(h, y1 + padding)
    x0 = max(0, x0 - padding)
    x1 = min(w, x1 + padding)

    return img[y0:y1, x0:x1]
    pass

def prepare_for_ocr(crop, inset=6):
    #crop = crop[inset: -inset, inset: -inset]
    gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    resized_crop = cv2.resize(gray_crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    blurred_crop = cv2.medianBlur(resized_crop, 7)
    _, op_crop = cv2.threshold(blurred_crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blurred_num_crop = cv2.medianBlur(resized_crop, 3)
    _, num_crop = cv2.threshold(blurred_num_crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    num_crop = shave_whitespace(num_crop)
    op_crop = shave_whitespace(op_crop, padding=70)
    return (op_crop, num_crop)   

def only_one_island_of_black(pil_black_and_white):
    arr = np.array(pil_black_and_white.convert('L'))
    black_mask = (arr == 0)
    _, num_features = label(black_mask)
    return num_features == 1

def do_ocr(img, can_be_operator=True):
    op_crop, num_crop = img
    global image_idx
    pil_op_crop = Image.fromarray(op_crop)
    #op_crop = ImageOps.expand(op_crop, border=(0, 10, 0, 10), fill='white')

    if can_be_operator:
        result = pytesseract.image_to_string(pil_op_crop, config=r'--oem 3 --psm 10 -c tessedit_char_whitelist=')
        result = result.strip()
        if result == '/':
            return result
        result = pytesseract.image_to_string(pil_op_crop, config=r'--oem 3 --psm 13 -c tessedit_char_whitelist=+-x=')
        result = result.strip()
        if result in ['+', '-', 'x', '=']:
            if result == "=" and only_one_island_of_black(pil_op_crop): # Hack to deal with the OCR confusing - for =
                return "-"
            if result == 'x':
                return '*'
            return result
    results = reader.readtext(num_crop, detail=0, paragraph=False, rotation_info=[0], allowlist='0123456789')
    if len(results) > 0:
        return results[0]
    results = reader.readtext(op_crop, detail=0, paragraph=False, rotation_info=[0], allowlist='0123456789')
    if len(results) > 0:
        return results[0]
    pass
    raise ValueError("OCR was provided with an image it could not find any characters in")
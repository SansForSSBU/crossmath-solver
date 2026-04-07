import easyocr
from PIL import Image, ImageOps
import pytesseract
import cv2

reader = easyocr.Reader(['en'])
image_idx = 0

def ocr(crop, can_be_operator=True):
    ocr_ready = prepare_for_ocr(crop)
    cell_contents = do_ocr(ocr_ready, can_be_operator=can_be_operator)
    return cell_contents

def prepare_for_ocr(crop, inset=6):
    crop = crop[inset: -inset, inset: -inset]    
    gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    resized_crop = cv2.resize(gray_crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    blurred_crop = cv2.medianBlur(resized_crop, 7)
    _, op_crop = cv2.threshold(blurred_crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blurred_num_crop = cv2.medianBlur(resized_crop, 3)
    _, num_crop = cv2.threshold(blurred_num_crop, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return (op_crop, num_crop)   

def do_ocr(img, can_be_operator=True, debug_nums=False):
    op_crop, num_crop = img
    global image_idx
    op_crop = Image.fromarray(op_crop)
    op_crop = ImageOps.expand(op_crop, border=(0, 10, 0, 10), fill='white')
    if debug_nums:
        debug_num = Image.fromarray(num_crop)
        debug_num.save(f"test_images/n{image_idx}.png")
        image_idx += 1

    if can_be_operator:
        result = pytesseract.image_to_string(op_crop, config=r'--oem 3 --psm 10 -c tessedit_char_whitelist=')
        result = result.strip()
        if result == '/':
            return result
        result = pytesseract.image_to_string(op_crop, config=r'--oem 3 --psm 13 -c tessedit_char_whitelist=+-x=')
        result = result.strip()
        if result in ['+', '-', 'x', '=']:
            if result == 'x':
                return '*'
            return result
    results = reader.readtext(num_crop, detail=0, paragraph=False, rotation_info=[0], allowlist='0123456789 ')
    if len(results) > 0:
        return results[0]
    return ''
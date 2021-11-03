import cv2
import os
from pathlib import Path
from PIL import Image, ImageOps
import pytesseract

BASE_DIR = Path(__file__).resolve().parent
tesseract_location = os.path.join(
    BASE_DIR, "support", "tesseract_install", "tesseract.exe"
)
pytesseract.pytesseract.tesseract_cmd = (
    tesseract_location  # Location of tesseract.eve file
)


def match_template(template, window_key):
    SOURCE_DIR = os.path.join(BASE_DIR, "static", f"source_{window_key}.jpg")
    TEMPLATE_DIR = template
    match_exist = False
    source_img = cv2.imread(SOURCE_DIR, 0)
    template_img = cv2.imread(TEMPLATE_DIR, 0)
    result = cv2.matchTemplate(source_img, template_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f"max loc: {max_loc}")
    print(f"max_val: {max_val}")
    if max_val > 0.95:
        match_exist = True
    template_h, template_w = template_img.shape
    location = [max_loc[0] + template_w / 2, (max_loc[1] + template_h / 2)]
    context = {"exist": match_exist, "loc": location, "max_val": max_val}
    return context


def read_text(image):
    custom_config = r"--oem 3 kor+chi_sim+eng+jpn+vie --psm 6"
    text = pytesseract.image_to_string(image, lang="eng")
    return text


def text_recognition(cropping, window_key):
    x0, y0, x1, y1 = cropping["x0"], cropping["y0"], cropping["x1"], cropping["y1"]

    SOURCE_DIR = os.path.join(BASE_DIR, "static", f"source_{window_key}.jpg")
    print(window_key)
    TEMPLATE_DIR = os.path.join(BASE_DIR, "static", f"template_{window_key}.jpg")
    image = Image.open(SOURCE_DIR)
    image_cropped = image.crop((x0, y0, x1, y1))
    image_cropped.save(TEMPLATE_DIR)

    image = cv2.imread(TEMPLATE_DIR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if x0 == 1356 and y0 == 282 and x1 == 1514 and y1 == 321:
        print("here")
        custom_config = r"--oem 3 eng --psm 6"
        ret, thresh_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    else:
        ret, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)
    text = read_text(thresh_image)
    print(text)

    return text

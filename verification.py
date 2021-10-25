from windows_operations import *
from obj_detection import match_template
from screen_loc import locations as loc

import cv2
import os
from pathlib import Path
import time
from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent

def check_verification(func):
    def wrapper(action, window, window_key):
        detect_end_script(window_key)
        
        take_screenshot(window_key)
        TEMPLATE_DIR = os.path.join(BASE_DIR, "assets", "verify.jpg")
        verify_button_match = match_template(TEMPLATE_DIR, window_key)
        if verify_button_match["exist"]:
            click(verify_button_match["loc"][0],verify_button_match["loc"][1], window)
            time.sleep(5)
            complete_verification(window, window_key)
        TEMPLATE_DIR = os.path.join(BASE_DIR, "assets", "submit_verification.jpg")
        submit_button_match = match_template(TEMPLATE_DIR, window_key)
        if submit_button_match["exist"]:
            while True:
                if complete_verification(window, window_key):
                    click(submit_button_match["loc"][0], submit_button_match["loc"][1], window)
                    time.sleep(10)
                    take_screenshot(window_key)
                    TEMPLATE_DIR = os.path.join(BASE_DIR, "assets", "submit_verification.jpg")
                    submit_button_match = match_template(TEMPLATE_DIR, window_key)
                    if not submit_button_match["exist"]:
                        break
        func(action, window, window_key)
                
        
    return wrapper

def complete_verification(window, window_key):
    detect_end_script(window_key)

    take_screenshot(window_key)
    SOURCE_DIR = os.path.join(BASE_DIR, "static", f"source_{window_key}.jpg")
    TEMPLATE_LIST_DIR = os.path.join(BASE_DIR, "static", f"verification_template_list_{window_key}.jpg")
    TEMPLATE_DIR = os.path.join(BASE_DIR, "static", f"template_{window_key}.jpg")
    TEMPLATE_ROTATED_DIR = os.path.join(BASE_DIR, "static", f"template_rotate_{window_key}.jpg")
    image = Image.open(SOURCE_DIR)
    source = image.crop((loc["verification_source"]["x0"], loc["verification_source"]["y0"], loc["verification_source"]["x1"], loc["verification_source"]["y1"]))
    source.save(SOURCE_DIR)
    template_list = image.crop((loc["verification_temp"]["x0"], loc["verification_temp"]["y0"], loc["verification_temp"]["x1"], loc["verification_temp"]["y1"]))
    template_list.save(TEMPLATE_LIST_DIR)
    source = cv2.imread(SOURCE_DIR, 0)
    # source = cv2.GaussianBlur(source,(5,5),1)
    ret, thresh_source = cv2.threshold(source,230,255, cv2.THRESH_BINARY)
    cv2.imwrite(SOURCE_DIR, thresh_source)
    best_match = ""
    match_list = []
    for x in range(5):
        template_cropped = template_list.crop((0+45*x, 1, 45+45*x, 50))
        # template_cropped = template_list.crop((10, 12, 35, 37))
        template_cropped.save(TEMPLATE_DIR)
        template_image = cv2.imread(TEMPLATE_DIR, 0)
        ret, thresh_template = cv2.threshold(template_image,127,255, cv2.THRESH_BINARY_INV)
        cv2.imwrite(TEMPLATE_DIR, thresh_template)
        best_val = 0
        for n in range(360):
            template_cropped = Image.open(TEMPLATE_DIR)
            template_rotate = template_cropped.rotate(n)
            template_rotate.save(TEMPLATE_ROTATED_DIR)
            current_match = match_template(TEMPLATE_ROTATED_DIR, window_key)
            if current_match["max_val"] > best_val:
                best_match = current_match
        click(best_match["loc"][0]+23+730, best_match["loc"][1]+23+542, window)
    return True

    # TO DO: COMPLETE LATER
    # TEMPLATE_DIR = os.path.join(BASE_DIR, "assets", "submit_verification.jpg")
    # submit_button_match = match_template(TEMPLATE_DIR)
    # click(match["loc"][0], match["loc"][1], target_window)
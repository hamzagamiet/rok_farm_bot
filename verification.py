from windows_operations import *
from obj_detection import match_template
from bot_settings import target_window

import cv2
import os
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent

def check_verification(func):
    def wrapper(*args, **kwargs):
        take_screenshot()
        TEMPLATE_DIR = os.path.join(BASE_DIR, "assets", "verify.jpg")
        verify_button_match = match_template(TEMPLATE_DIR)
        if verify_button_match["exists"]:
            click(verify_button_match["loc"][0],verify_button_match["loc"][1])
            time.sleep(5)
        TEMPLATE_DIR = os.path.join(BASE_DIR, "assets", "submit_verification.jpg")
        submit_button_match = match_template(TEMPLATE_DIR)
        if submit_button_match["exists"]:
            while True:
                if complete_verification():
                    break
    return wrapper

def complete_verification():
    return True
    # TO DO: COMPLETE LATER
    # TEMPLATE_DIR = os.path.join(BASE_DIR, "assets", "submit_verification.jpg")
    # submit_button_match = match_template(TEMPLATE_DIR)
    # click(match["loc"][0], match["loc"][1], target_window)
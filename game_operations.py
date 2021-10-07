from bot_settings import target_window, requested_actions
from windows_operations import *
from screen_loc import locations as loc
from obj_detection import *
from template_files import template_paths as TEMPLATE

import os
from PIL import Image, ImageOps
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent

def main():
    for action in requested_actions:
        execute_action(action)

def return_to_game(func):
    def wrapper(*args, **kwargs):
        take_screenshot(target_window)
        exit_button = match_template(os.path.join(BASE_DIR, "assets", f"exit_button.jpg"))
        if exit_button["exist"]:
            click(exit_button["loc"][0], exit_button["loc"][1], target_window)
            time.sleep(3)
            func(*args, **kwargs)
        else:
            build_button = match_template(os.path.join(BASE_DIR, "assets", f"build.jpg"))
            search_button = match_template(os.path.join(BASE_DIR, "assets", f"search.jpg"))
            exit_button = match_template(os.path.join(BASE_DIR, "assets", f"exit_button.jpg"))
            if build_button["exist"]:
                print("zoom out")
                map_button = match_template(os.path.join(BASE_DIR, "assets", f"map.jpg"))
                click(map_button["loc"][0], map_button["loc"][1], target_window)
                time.sleep(3)
                func(*args, **kwargs)
            elif search_button["exist"]:
                func(*args, **kwargs)
            elif exit_button["exist"] :
                print ("click exit")
                click(exit_button["loc"][0], exit_button["loc"][1], target_window)
                time.sleep(3)
                func(*args, **kwargs)
            else:
                print ("could not return to game")
    return wrapper


def troops_available(func):
    def wrapper(*args, **kwargs):
        take_screenshot(target_window)
        troop_dispatch_text = text_recognition(loc["no_gatherers"])
        try:
            troops_dispatched = troop_dispatch_text.split("/")[0]
            tot_troop_slots = troop_dispatch_text.split("/")[1]
        except:
            troops_dispatched = 0
            tot_troop_slots = 1
        print (troops_dispatched, tot_troop_slots)
        if int(troops_dispatched) != int(tot_troop_slots):
            func(*args, **kwargs)
        else:
            print("no marches available")
    return wrapper

# @check_verification
@return_to_game
@troops_available
def execute_action(action):
    for step in action:
        click_center = False
        if step == TEMPLATE["search_loc"]:
            click_center = True
        time.sleep(1)       
        execute_step(step, click_center)

def execute_step(template, click_center):
    take_screenshot(target_window)
    match = match_template(template)
    if match["exist"]:
        print("clicking match")
        click(match["loc"][0], match["loc"][1], target_window)
        if click_center == True:
            time.sleep(3)
            click(1920 / 2, 1080 / 2, target_window)
    else:
        print("no match found")

main()
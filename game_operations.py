from windows_operations import *
from screen_loc import locations as loc
from obj_detection import *
from template_files import template_paths as TEMPLATE
import os
from PIL import Image, ImageOps
from pathlib import Path
import time
BASE_DIR = Path(__file__).resolve().parent
action = []
no_actions = 0
window = ""

def main(action, no_actions, window):
    time.sleep(1)
    if within_limit(no_actions, window):
        execute_action(action, window)
    else:
        print(f"already have {no_actions} marches dispatched")

def return_to_game(func):
    def wrapper(action, window):
        take_screenshot(window)
        exit_button = match_template(os.path.join(BASE_DIR, "assets", f"exit_button.jpg"), window)
        if exit_button["exist"]:
            click(exit_button["loc"][0], exit_button["loc"][1], window)
            time.sleep(3)

            func(action, window)
        else:
            build_button = match_template(os.path.join(BASE_DIR, "assets", f"build.jpg"), window)
            search_button = match_template(os.path.join(BASE_DIR, "assets", f"search.jpg"), window)
            exit_button = match_template(os.path.join(BASE_DIR, "assets", f"exit_button.jpg"), window)

            if build_button["exist"]:
                print("zoom out")
                map_button = match_template(os.path.join(BASE_DIR, "assets", f"map.jpg"), window)
                click(map_button["loc"][0], map_button["loc"][1], window)
                time.sleep(3)
    
                func(action, window)
            elif search_button["exist"]:
                func(action, window)
            elif exit_button["exist"] :
                print ("click exit")
                click(exit_button["loc"][0], exit_button["loc"][1], window)
                time.sleep(3)
    
                func(action, window)
            else:
                print ("could not return to game")
    return wrapper


def troops_available(func):
    def wrapper(action, window):
        take_screenshot(window)
        troop_dispatch_text = text_recognition(loc["no_gatherers"],window)
        try:
            troops_dispatched = troop_dispatch_text.split("/")[0]
            tot_troop_slots = troop_dispatch_text.split("/")[1].split[0]
        except:
            troops_dispatched = 0
            tot_troop_slots = 1
        print (troops_dispatched, tot_troop_slots)
        if tot_troop_slots == "s":
            tot_troop_slots = 5
            print("YOUR TROOPS")
        print (troops_dispatched)
        if int(troops_dispatched) != int(tot_troop_slots):
            func(action, window)
        else:
            print("no marches available")
    return wrapper

def within_limit(no_actions, window):
    take_screenshot(window)
    troop_dispatch_text = text_recognition(loc["no_gatherers"],window)
    try:
        troops_dispatched = troop_dispatch_text.split("/")[0]
        if troops_dispatched == "s":
            troops_dispatched = 5
        if no_actions <= int(troops_dispatched):
            print("troop limit reached")
            return False
        else:
            print ("sending troops")            
    except:
        print("cannot read troop info")
    return True
    

# @check_verification
@return_to_game
@troops_available
def execute_action(action, window):
    for step in action:
        click_center = False
        if step == TEMPLATE["search_loc"]:
            click_center = True
        time.sleep(1)       
        execute_step(step, click_center, window)

def execute_step(template, click_center, window):
    take_screenshot(window)
    match = match_template(template, window)
    if match["exist"]:
        print("clicking match")
        click(match["loc"][0], match["loc"][1], window)
        if click_center == True:
            time.sleep(3)
            click(1920 / 2, 1080 / 2, window)
    else:
        print("no match found")
        
if __name__ == "__main__":
   main(action, no_actions, window)

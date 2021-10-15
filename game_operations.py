from verification import check_verification
from windows_operations import *
from screen_loc import locations as loc
from obj_detection import *
from template_files import template_paths as TEMPLATE
import os
from PIL import Image, ImageOps
from pathlib import Path
from bot_settings import get_action_list
import time
import json
import sys

BASE_DIR = Path(__file__).resolve().parent

def main():
    with open("data.json", "r") as file:
        data = json.load(file)[0]
    for key in data:
        window = key
    window_key = window
    window = win32gui.FindWindow(None, window_key)
    resource_list = [data[window_key][n]["resource"] for n in data[window_key]]
    requested_actions = get_action_list(resource_list)
    while True:
        for action in requested_actions:
            time.sleep(1)
            if within_limit(len(requested_actions), window, window_key):
                execute_action(action, window, window_key)
            else:
                print(f"already have {len(requested_actions)} marches dispatched")
                keep_running(window_key)

def return_to_game(func):
    def wrapper(action, window, window_key):
        take_screenshot(window_key)
        
        search_button = match_template(os.path.join(BASE_DIR, "assets", f"search.jpg"), window_key)

        while not search_button["exist"]:
            exit_button = match_template(os.path.join(BASE_DIR, "assets", f"exit_button.jpg"), window_key)
            chat_exit_button = match_template(os.path.join(BASE_DIR, "assets", f"chat_exit.jpg"), window_key)
            confirm_button = match_template(os.path.join(BASE_DIR, "assets", f"confirm_button.jpg"), window_key)
            game_launch_button = match_template(os.path.join(BASE_DIR, "assets", f"game_launch_icon.jpg"), window_key)
            build_button = match_template(os.path.join(BASE_DIR, "assets", f"build.jpg"), window_key)
            search_button = match_template(os.path.join(BASE_DIR, "assets", f"search.jpg"), window_key)
            exit_button = match_template(os.path.join(BASE_DIR, "assets", f"exit_button.jpg"), window_key)
            map_button = match_template(os.path.join(BASE_DIR, "assets", f"map.jpg"), window_key)
            
            if exit_button["exist"]:
                print ("exit_button")
                click(exit_button["loc"][0], exit_button["loc"][1], window)
                time.sleep(3)

            if chat_exit_button["exist"]:
                print ("exit_button")
                click(chat_exit_button["loc"][0], chat_exit_button["loc"][1], window)
                time.sleep(3)

            if confirm_button["exist"]:
                print ("exit_button")
                click(confirm_button["loc"][0], confirm_button["loc"][1], window)

            if game_launch_button["exist"]:
                print ("exit_button")   
                click(game_launch_button["loc"][0], game_launch_button["loc"][1], window)

            if build_button["exist"]:
                click(map_button["loc"][0], map_button["loc"][1], window)

            if exit_button["exist"]:
                print ("exit_button")
                click(exit_button["loc"][0], exit_button["loc"][1], window)

            time.sleep(1)
            print ("attempting to return to game")
            take_screenshot(window_key)

        func(action, window, window_key)        
    return wrapper


def troops_available(func):
    def wrapper(action, window, window_key):
        take_screenshot(window_key)
        troop_dispatch_text = text_recognition(loc["no_gatherers"],window_key)
        try:
            troops_dispatched = troop_dispatch_text.split("/")[0]
            tot_troop_slots = troop_dispatch_text.split("/")[1].split[0]
        except:
            troops_dispatched = 0
            tot_troop_slots = 1
        print (troops_dispatched, tot_troop_slots)
        if tot_troop_slots == "s" or "S":
            tot_troop_slots = 5
        print (troops_dispatched)
        if int(troops_dispatched) != int(tot_troop_slots):
            func(action, window, window_key)
        else:
            print("no marches available")
    return wrapper

def within_limit(no_actions, window, window_key):
    take_screenshot(window_key)
    troop_dispatch_text = text_recognition(loc["no_gatherers"],window_key)
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
    
def keep_running(window_key):
    match = False
    with open("data.json", "r") as file:
        data_list = json.load(file)
        for data in data_list:
            print(data)
            for key in data:
                print(key)
                if key == window_key:
                    match = True
                    break
            if match:
                break
        if match == False:
            print("ending")
            sys.exit()

@check_verification
@return_to_game
@troops_available
def execute_action(action, window, window_key):
    for step in action:
        click_center = False
        if step == TEMPLATE["search_loc"]:
            click_center = True
        time.sleep(1)       
        execute_step(step, click_center, window, window_key)

def execute_step(template, click_center, window, window_key):
    keep_running(window_key)
    take_screenshot(window_key)
    match = match_template(template, window_key)
    if match["exist"]:
        print("clicking match")
        click(match["loc"][0], match["loc"][1], window)
        if click_center == True:
            time.sleep(3)
            click(1920 / 2, 1080 / 2, window)
    else:
        print("no match found")
        
if __name__ == "__main__":
   main()

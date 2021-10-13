import numpy as np
from pathlib import Path
from template_files import template_paths as TEMPLATE
import win32gui
import os

BASE_DIR = Path(__file__).resolve().parent
    
wood_action = [
    TEMPLATE["search"],
    TEMPLATE["wood"],
    TEMPLATE["search_loc"],
    TEMPLATE["gather"],
    TEMPLATE["new_troops"],
    TEMPLATE["march"],
]
food_action = [
    TEMPLATE["search"],
    TEMPLATE["food"],
    TEMPLATE["search_loc"],
    TEMPLATE["gather"],
    TEMPLATE["new_troops"],
    TEMPLATE["march"],
]
gold_action = [
    TEMPLATE["search"],
    TEMPLATE["gold"],
    TEMPLATE["search_loc"],
    TEMPLATE["gather"],
    TEMPLATE["new_troops"],
    TEMPLATE["march"],
]
stone_action = [
    TEMPLATE["search"],
    TEMPLATE["stone"],
    TEMPLATE["search_loc"],
    TEMPLATE["gather"],
    TEMPLATE["new_troops"],
    TEMPLATE["march"],
]

def get_action_list(resource_list):
    action_list = []
    for resource in resource_list:
        if resource == "wood":
            action_list.append(wood_action)
        elif resource == "food":
            action_list.append(food_action)
        elif resource == "stone":
            action_list.append(stone_action)
        elif resource == "gold":
            action_list.append(gold_action)
    return action_list
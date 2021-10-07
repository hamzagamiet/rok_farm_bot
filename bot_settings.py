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

#TEST DATA - WILL BE TAKEN FROM interface.py
requested_actions = [
    stone_action,
    food_action,
    wood_action,
    gold_action,
    wood_action,
]

target_window = win32gui.FindWindow(None, "BlueStacks")

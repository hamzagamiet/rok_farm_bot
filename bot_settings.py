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


def get_action_list(resource):
    action_list = []
    if resource.lower() == "wood":
        action_list = wood_action
    elif resource.lower() == "food":
        action_list = food_action
    elif resource.lower() == "stone":
        action_list = stone_action
    elif resource.lower() == "gold":
        action_list = gold_action
    return action_list


def march_info(self):
    march_list = [
        self.int_val1.get(),
        self.int_val2.get(),
        self.int_val3.get(),
        self.int_val4.get(),
        self.int_val5.get(),
    ]
    node_list = [
        self.node1.get(),
        self.node2.get(),
        self.node3.get(),
        self.node4.get(),
        self.node5.get(),
    ]

    active_node_list = []
    for n in range(len(march_list)):
        if march_list[n] == 1:
            for option in self.rss_options:
                if node_list[n].lower() == option.lower():
                    active_node_list.append(option.lower())

    requested_actions = []
    for node in active_node_list:
        if node == "wood":
            requested_actions.append("wood")
        elif node == "food":
            requested_actions.append("food")
        elif node == "stone":
            requested_actions.append("stone")
        elif node == "gold":
            requested_actions.append("gold")

    return requested_actions

from verification import check_verification
from windows_operations import *
from screen_loc import locations as loc
from obj_detection import *
from template_files import template_paths as TEMPLATE
import os
import json
from pathlib import Path
from bot_settings import get_action_list
import time

BASE_DIR = Path(__file__).resolve().parent


class FarmingInformation:
    def __init__(self):
        self.start()

    def start(self):
        with open("data.json", "r") as file:
            self.data = json.load(file)[0]
        for key in self.data:
            self.window_key = key
        march_list = [
            [self.data[self.window_key][n]["resource"], self.window_key]
            for n in self.data[self.window_key]
        ]
        self.march_list = march_list
        self.march_count = len(march_list)

        while True:
            print (self.march_list)
            print (type(self.march_list))
            march = FarmMarch(
                resource = march_list[0][0], window_key = march_list[0][1], march_count = self.march_count
            )
            print (
                f"{march.is_running}\n\n"
                f"{march.resource}\n\n"
                f"{march.action_list}\n\n"
                f"{march.coordinates}\n\n"
                f"{march.window_key}\n\n"
                f"{march.window}\n\n"
            )
            time.sleep(1)
            if GameCheck.check_dispatched_army(self.march_count, march.window_key):
                if march.start():
                    self.march_list = self.queue(march_list)
            else:
                detect_end_script(self.window_key)

    def queue(self, march_list):
        march_list.append(march_list[0])
        del march_list[0]
        return march_list


class FarmMarch:

    def __init__(
        self, is_running=False, resource=None, coordinates=None, window_key=None, march_count = 0
    ):
        self.is_running = is_running
        self.resource = resource
        self.action_list = get_action_list(self.resource)
        self.coordinates = coordinates
        self.window_key = window_key
        self.march_count = march_count
        self.window = win32gui.FindWindow(None, self.window_key)

        print ("instantiating...")
        print (self.action_list)
        time.sleep(1)

    def start(self):
        for self.action_index in range(len(self.action_list)):
            while True:
                if self.execute_action():
                    break
        return True

    def execute_action(self):
        print("executing action")
        check_verification(self.window_key, self.window)
        GameCheck.return_to_game(self.window_key, self.window)
        if GameCheck.check_troops_avilable(self.window_key):
            print("you have troops available")
            self.click_center = False
            if GameCheck.check_dispatched_army(
                self.march_count, self.window_key
            ):
                self.step = self.action_list[self.action_index]
                print (self.step)
            if self.step == TEMPLATE["search_loc"]:
                self.click_center = True
            self.execute_step()
            print ("true")
            time.sleep(2)
            # take_screenshot(self.window_key)
            # if (
            #     not match_template(self.step, self.window_key)["exist"]
            #     and self.action_index != 1
            #     or self.action_index == 1
            # ):
            #     return False
            print ("here")
            return True
        print("nothing")
        return False

    def execute_step(self):
        print(self.step)
        detect_end_script(self.window_key)
        take_screenshot(self.window_key)
        match = match_template(self.step, self.window_key)
        if self.step == TEMPLATE["gather"]:
            take_screenshot(self.window_key)
            co_ordinates_text = text_recognition(loc["co_ordinates"], self.window_key)
            co_ordinates_text = co_ordinates_text.split(" ")
        if match["exist"]:
            click(match["loc"][0], match["loc"][1], self.window)
            if self.click_center == True:
                time.sleep(3)
                click(1920 / 2, 1080 / 2, self.window)
        print ("done")


class GameCheck:
    def return_to_game(window_key, window):
        take_screenshot(window_key)

        button_exceptions_files = [
            "search.jpg",
            "search_loc.jpg",
            "new_troops.jpg",
            "march.jpg"
        ]
        button_exceptions = [
            match_template(os.path.join(BASE_DIR, "assets", button_file), window_key)
            for button_file in button_exceptions_files
        ]   

        while True:

            button_exist = False
            for button in button_exceptions:
                if button["exist"]:
                    button_exist = True
                    break
            if button_exist:
                break

            exit_button = match_template(
                os.path.join(BASE_DIR, "assets", f"exit_button.jpg"), window_key
            )
            chat_exit_button = match_template(
                os.path.join(BASE_DIR, "assets", f"chat_exit.jpg"), window_key
            )
            confirm_button = match_template(
                os.path.join(BASE_DIR, "assets", f"confirm_button.jpg"), window_key
            )
            game_launch_button = match_template(
                os.path.join(BASE_DIR, "assets", f"game_launch_icon.jpg"), window_key
            )
            build_button = match_template(
                os.path.join(BASE_DIR, "assets", f"build.jpg"), window_key
            )
            search_button = match_template(
                os.path.join(BASE_DIR, "assets", f"search.jpg"), window_key
            )
            exit_button = match_template(
                os.path.join(BASE_DIR, "assets", f"exit_button.jpg"), window_key
            )
            map_button = match_template(
                os.path.join(BASE_DIR, "assets", f"map.jpg"), window_key
            )

            if exit_button["exist"]:
                click(exit_button["loc"][0], exit_button["loc"][1], window)
                time.sleep(3)

            if chat_exit_button["exist"]:
                click(chat_exit_button["loc"][0], chat_exit_button["loc"][1], window)
                time.sleep(3)

            if confirm_button["exist"]:
                click(confirm_button["loc"][0], confirm_button["loc"][1], window)

            if game_launch_button["exist"]:
                click(
                    game_launch_button["loc"][0], game_launch_button["loc"][1], window
                )

            if build_button["exist"]:
                click(map_button["loc"][0], map_button["loc"][1], window)

            if exit_button["exist"]:
                click(exit_button["loc"][0], exit_button["loc"][1], window)

            time.sleep(1)
            take_screenshot(window_key)

    def check_troops_avilable(window_key):
        take_screenshot(window_key)
        troop_dispatch_text = text_recognition(loc["no_gatherers"], window_key)
        try:
            troops_dispatched = troop_dispatch_text.split("/")[0]
            tot_troop_slots = troop_dispatch_text.split("/")[1].split[0]
        except:
            troops_dispatched = 0
            tot_troop_slots = 1
        if tot_troop_slots == "s" or "S":
            tot_troop_slots = 5
        if int(troops_dispatched) != int(tot_troop_slots):
            return True
        else:
            return False

    def check_dispatched_army(no_marches, window_key):
        take_screenshot(window_key)
        troop_dispatch_text = text_recognition(loc["no_gatherers"], window_key)
        try:
            troops_dispatched = troop_dispatch_text.split("/")[0]
            if troops_dispatched == "s":
                troops_dispatched = 5
            if no_marches <= int(troops_dispatched):
                return False
            else:
                return True
        except:
            return True


if __name__ == "__main__":
    FarmingInformation()

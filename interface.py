from tkinter import *
from tkinter import ttk
from pathlib import Path
import os
import threading
import json
from subprocess import Popen
import requests

#INITIAL DECLARATIONS
BASE_DIR = Path(__file__).resolve().parent
root = Tk()

def create_combobox(root, rss_options, current_val = None):
    print (current_val)
    node = ttk.Combobox(root, value = rss_options, width=10)
    node.current(current_val)
    return node

def combobox_value_index(rss_options, value):
    for index in range(len(rss_options)):
        if rss_options[index] == value:
            return index
    return None

def change_window(frame):
    frame.tkraise()


root.title("ROKBot")

root.geometry("500x500")
root.minsize(500,500)
root.maxsize(500,500)
my_menu = Menu(root)
root.config(menu=my_menu)
style = ttk.Style(root)
style.theme_use("vista")

#CREATE ITEMS
account = Menu(my_menu)
my_menu.add_cascade(label="Bot",menu=account)
activate = Menu(my_menu)
my_menu.add_cascade(label="Activate", menu=activate)
activate.add_command(label="Enter Key")
activate.add_separator()
activate.add_command(label="Buy Key")
discord = Menu(my_menu)
my_menu.add_cascade(label="Discord", menu=discord)

def show_frame(frame):
    '''Show a frame for the given page name'''
    frame.tkraise()

class Home(Frame):

    def __init__(self, root):
        Frame.__init__(self)
        # self.scollbar = Scrollbar(Home, orient= VERTICAL)
        self.root = root
        with open('license.txt', "a+") as file_data:
            file_data.seek(0)
            text = file_data.read()
            print(text)
            key_activated = False
            if len(text) > 0:
                response = requests.get(f"https://www.therokhub.com/secretaccess/farm/check_license/{text}")
                print(response)
                response_json = response.json()
                if response_json["status"] == "active":
                    key_activated = True


        if not key_activated:
            self.key_entry = Entry(root, width=50)
            self.key_entry.grid(row = 1, column = 1, padx =40, pady = 2, sticky="nsew")                                   
            self.submit_key = Button(root, text= "SUBMIT", command=self.key_submission)
            self.submit_key.grid(row = 2, column = 1, padx =40, pady = 2, sticky="nsew") 
        
        if key_activated:
            self.instance_treeview = ttk.Treeview(root)
            self.instance_treeview["columns"] = ("Instance", "Running", "State")
            self.instance_treeview.column("#0", width=60)
            self.instance_treeview.column("Instance", anchor =W, width=130)
            self.instance_treeview.column("Running", anchor =W, width=130)
            self.instance_treeview.column("State", anchor =W, width=130)
            self.instance_treeview.heading("#0", text = "Label", anchor= W)
            self.instance_treeview.heading("Instance", text = "Instance", anchor= W)
            self.instance_treeview.heading("Running", text = "Running", anchor= W)
            self.instance_treeview.heading("State", text = "State", anchor= W)
            self.instance_treeview.insert(parent="",index="end", iid=0, text="", values=("Bluestacks", 0, 0))
            self.instance_treeview.insert(parent="",index="end", iid=1, text="", values=("Bluestacks 1", 0, 0))
            self.instance_treeview.grid(row = 1, column = 1, columnspan = 8, padx =25, pady = 2, sticky="nsew")
            self.instance_treeview.bind("<Double-1>", self.OnDoubleClick)

    def key_submission(self):
        key_submit = self.key_entry.get()
        response = requests.get(f"https://www.therokhub.com/secretaccess/farm/check_license/{key_submit}")
        response_json = response.json()
        if response_json["status"] == "active":
            print ("ACTIVATED")
            with open('license.txt', 'w+') as file:
                file.write(key_submit)
        else:
            print ("NOT ACTIVATED")
        show_frame(Home(root))


    def OnDoubleClick(self, event):
        item = self.instance_treeview.selection()
        for i in item:
            instance = self.instance_treeview.item(i, "values")[0]
        show_frame(FarmingWindow(self.root, instance))

class FarmingWindow(Frame):
    def __init__(self, root, window):
        Frame.__init__(self)
        n = 100
        #CREATION
        self.page_title = Label(root, text = window)
        self.window = window
        self.rss_options = ["Wood", "Food", "Stone","Gold"]
        self.level_options = [1,2,3,4,5,6,7,8,9]
        self.int_val1 = IntVar()
        self.int_val2 = IntVar()
        self.int_val3 = IntVar()
        self.int_val4 = IntVar()
        self.int_val5 = IntVar()
        #INSTANTION
        self.is_active1 = Checkbutton(root,variable=self.int_val1, onvalue=1, offvalue=0, text= "March 1")
        self.is_active2 = Checkbutton(root,variable=self.int_val2, onvalue=1, offvalue=0, text= "March 2")
        self.is_active3 = Checkbutton(root,variable=self.int_val3, onvalue=1, offvalue=0, text= "March 3")
        self.is_active4 = Checkbutton(root,variable=self.int_val4, onvalue=1, offvalue=0, text= "March 4")
        self.is_active5 = Checkbutton(root,variable=self.int_val5, onvalue=1, offvalue=0, text= "March 5")
        self.node1 = create_combobox(root, self.rss_options)        
        self.node2 = create_combobox(root, self.rss_options)       
        self.node3 = create_combobox(root, self.rss_options)      
        self.node4 = create_combobox(root, self.rss_options) 
        self.node5 = create_combobox(root, self.rss_options)
        self.march_1_level = create_combobox(root, self.level_options, 0)        
        self.march_2_level = create_combobox(root, self.level_options, 0)        
        self.march_3_level = create_combobox(root, self.level_options, 0)        
        self.march_4_level = create_combobox(root, self.level_options, 0)   
        self.march_5_level = create_combobox(root, self.level_options, 0)   
        self.start_stop = Button(root, text= "START", command=self.start_bot_thread)
        #PLACEMENT
        self.page_title.grid(row = 2, column = 1, pady = 2, sticky="nsew")
        self.is_active1.grid(row = 3, column = 1, pady = 2, sticky="nsew")
        self.is_active2.grid(row = 4, column = 1, pady = 2, sticky="nsew")
        self.is_active3.grid(row = 5, column = 1, pady = 2, sticky="nsew")
        self.is_active4.grid(row = 6, column = 1, pady = 2, sticky="nsew")
        self.is_active5.grid(row = 7, column = 1, pady = 2, sticky="nsew")
        self.node1.grid(row = 3, column = 3, pady = 2, sticky="nsew")
        self.node2.grid(row = 4, column = 3, pady = 2, sticky="nsew")
        self.node3.grid(row = 5, column = 3, pady = 2, sticky="nsew")
        self.node4.grid(row = 6, column = 3, pady = 2, sticky="nsew")
        self.node5.grid(row = 7, column = 3, pady = 2, sticky="nsew")
        self.march_1_level.grid(row = 3, column = 4, pady = 2, sticky="nsew", padx =5)
        self.march_2_level.grid(row = 4, column = 4, pady = 2, sticky="nsew", padx =5)
        self.march_3_level.grid(row = 5, column = 4, pady = 2, sticky="nsew", padx =5)
        self.march_4_level.grid(row = 6, column = 4, pady = 2, sticky="nsew", padx =5)
        self.march_5_level.grid(row = 7, column = 4, pady = 2, sticky="nsew", padx =5)
        self.start_stop.grid(row = 8, column = 1, padx=25, pady = 2, sticky="nsew")
        
        try:
            with open("gui_data.json", "r") as file:
                data = json.load(file)
                for n in range(len(data)):
                    for key in data[n]:
                        if key == self.window:
                            if data[n][key]["int_val1"] == 1:
                                self.is_active1.select()
                            if data[n][key]["int_val2"] == 1:
                                self.is_active2.select()
                            if data[n][key]["int_val3"] == 1:
                                self.is_active3.select()
                            if data[n][key]["int_val4"] == 1:
                                self.is_active4.select()
                            if data[n][key]["int_val5"] == 1:
                                self.is_active5.select()
                            if data[n][key]["start_stop"] == "STOP":
                                self.start_stop.config(text="STOP")
                            self.node1.current(combobox_value_index(self.rss_options, data[n][key]["node1"]))
                            self.node2.current(combobox_value_index(self.rss_options, data[n][key]["node2"]))
                            self.node3.current(combobox_value_index(self.rss_options, data[n][key]["node3"]))
                            self.node4.current(combobox_value_index(self.rss_options, data[n][key]["node4"]))
                            self.node5.current(combobox_value_index(self.rss_options, data[n][key]["node5"]))
        except:
            print("this file is not currently running")

    def start_bot_thread(self):
        threading.Thread(target=self.start_bot()).start()

    def start_bot(self):
        requested_actions = self.march_info()
        if self.start_stop.cget("text") == "START":
            self.start_stop.config(text="STOP")
            with open('license.txt', "a+") as file:
                file.seek(0)
                license_key = file.read()             
            submit_data = {
                "license_key": license_key,
                "window": self.window,
                "window_active": True,
                "march_1_selected": True if self.int_val1.get() == 1 else False,
                "march_2_selected": True if self.int_val2.get() == 1 else False,
                "march_3_selected": True if self.int_val3.get() == 1 else False,
                "march_4_selected": True if self.int_val4.get() == 1 else False,
                "march_5_selected": True if self.int_val5.get() == 1 else False,
                "march_1_running": False,
                "march_2_running": False,
                "march_3_running": False,
                "march_4_running": False,
                "march_5_running": False,
                "march_1_target": self.node1.get(),
                "march_2_target": self.node2.get(),
                "march_3_target": self.node3.get(),
                "march_4_target": self.node4.get(),
                "march_5_target": self.node5.get(),
                "march_1_level": int(self.march_1_level.get()),
                "march_2_level": int(self.march_2_level.get()),
                "march_3_level": int(self.march_3_level.get()),
                "march_4_level": int(self.march_4_level.get()),
                "march_5_level": int(self.march_5_level.get()),
            }
            if len(license_key) > 0:
                requests.post(f"https://www.therokhub.com/secretaccess/farm/data", data= submit_data)
            Popen("python game_operations.py")
        
        elif self.start_stop.cget("text") == "STOP":
            self.start_stop.config(text="START")
            with open('license.txt', "a+") as file:
                file.seek(0)
                license_key = file.read()
            submit_data = {
                "license_key": license_key,
                "window": self.window,
            }
            print(submit_data)       
            if len(license_key) > 0:
                requests.post("https://www.therokhub.com/secretaccess/farm/data/delete", data= submit_data)

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

show_frame(Home(root))

def delete_on_exit():
    with open('license.txt', "r+") as file:
        file.seek(0)
        license_key = file.read()
    submit_data = {
        "license_key": license_key,
    }     
    if len(license_key) > 0:
        requests.post("https://www.therokhub.com/secretaccess/farm/data/delete/all", data= submit_data)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", delete_on_exit)

if __name__ == "__main__":
    root.mainloop()

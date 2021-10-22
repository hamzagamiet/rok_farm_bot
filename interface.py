from tkinter import *
from tkinter import ttk
from pathlib import Path
import os
from game_operations import main
from multiprocessing import Process
import threading
import json
from subprocess import Popen
import requests
import random

#INITIAL DECLARATIONS
BASE_DIR = Path(__file__).resolve().parent
root = Tk()

def create_combobox(root, options, current_val = None):
    print (current_val)
    node = ttk.Combobox(root, value = options)
    node.current(current_val)
    return node

def combobox_value_index(options, value):
    for index in range(len(options)):
        if options[index] == value:
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
                response = requests.get(f"https://www.therokhub.com/secretaccess/farm/check_license/{text}/{random(1000)}")
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
        url = f"https://www.therokhub.com/secretaccess/farm/check_license/{key_submit}"
        response = requests.get(url)
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
        self.page_title = Label(root, text = window)
        self.window = window
        self.options = ["Wood", "Food", "Stone","Gold"]
        self.int_val1 = IntVar()
        self.int_val2 = IntVar()
        self.int_val3 = IntVar()
        self.int_val4 = IntVar()
        self.int_val5 = IntVar()
        self.is_active1 = Checkbutton(root,variable=self.int_val1, onvalue=1, offvalue=0, text= "March 1")
        self.node1 = create_combobox(root, self.options)
        self.is_active2 = Checkbutton(root,variable=self.int_val2, onvalue=1, offvalue=0, text= "March 2")
        self.node2 = create_combobox(root, self.options)
        self.is_active3 = Checkbutton(root,variable=self.int_val3, onvalue=1, offvalue=0, text= "March 3")
        self.node3 = create_combobox(root, self.options)
        self.is_active4 = Checkbutton(root,variable=self.int_val4, onvalue=1, offvalue=0, text= "March 4")
        self.node4 = create_combobox(root, self.options)
        self.is_active5 = Checkbutton(root,variable=self.int_val5, onvalue=1, offvalue=0, text= "March 5")
        self.node5 = create_combobox(root, self.options)
        self.start_stop = Button(root, text= "START", command=self.start_bot_thread)
        self.page_title.grid(row = 2, column = 1, pady = 2, sticky="nsew")
        self.is_active1.grid(row = 3, column = 1, pady = 2, sticky="nsew")
        self.node1.grid(row = 3, column = 3, pady = 2, sticky="nsew")
        self.is_active2.grid(row = 4, column = 1, pady = 2, sticky="nsew")
        self.node2.grid(row = 4, column = 3, pady = 2, sticky="nsew")
        self.is_active3.grid(row = 5, column = 1, pady = 2, sticky="nsew")
        self.node3.grid(row = 5, column = 3, pady = 2, sticky="nsew")
        self.is_active4.grid(row = 6, column = 1, pady = 2, sticky="nsew")
        self.node4.grid(row = 6, column = 3, pady = 2, sticky="nsew")
        self.is_active5.grid(row = 7, column = 1, pady = 2, sticky="nsew")
        self.node5.grid(row = 7, column = 3, pady = 2, sticky="nsew")
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
                            self.node1.current(combobox_value_index(self.options, data[n][key]["node1"]))
                            self.node2.current(combobox_value_index(self.options, data[n][key]["node2"]))
                            self.node3.current(combobox_value_index(self.options, data[n][key]["node3"]))
                            self.node4.current(combobox_value_index(self.options, data[n][key]["node4"]))
                            self.node5.current(combobox_value_index(self.options, data[n][key]["node5"]))
        except:
            print("this file is not currently running")

    def start_bot_thread(self):
        threading.Thread(target=self.start_bot()).start()

    def start_bot(self):
        requested_actions = self.march_info()
        if self.start_stop.cget("text") == "START":
            self.start_stop.config(text="STOP")
            if requested_actions != []:
                current_data_dict = {
                    self.window: {
                        n: {
                            "resource": requested_actions[n],
                            "status": "waiting",
                            "co-ords": [],
                            "commander": "none"
                        } for n in range(len(requested_actions))
                    }
                }
                current_data = [current_data_dict]
                try:
                    with open("data.json", "r") as file:
                        data = json.load(file)
                        data.insert(0,current_data_dict)
                except:
                    print("couldn't load data")
                with open("data.json", "w+") as file:
                    try:
                        print("existing data")
                        json.dump(data, file, indent=4, separators=(',', ': '))
                    except:
                        print("broken data")
                        json.dump(current_data, file, indent=4, separators=(',', ': '))
                
                current_gui_data_dict = {
                    self.window:{
                        "int_val1": self.int_val1.get(),
                        "int_val2": self.int_val2.get(),
                        "int_val3": self.int_val3.get(),
                        "int_val4": self.int_val4.get(),
                        "int_val5": self.int_val5.get(),
                        "node1": self.node1.get(),
                        "node2": self.node2.get(),
                        "node3": self.node3.get(),
                        "node4": self.node4.get(),
                        "node5": self.node5.get(),
                        "start_stop": self.start_stop.cget("text")
                    }
                }
                current_gui_data = [current_gui_data_dict]
                try:
                    with open("gui_data.json", "r") as file:
                        gui_data = json.load(file)
                        gui_data.insert(0,current_gui_data_dict)
                except:
                    print("couldn't load gui data")
                file.close()
                with open("gui_data.json", "w+") as file:
                    try:
                        #work if existing file
                        json.dump(gui_data, file, indent=4, separators=(',', ': '))
                        print("existing gui data")
                    except:
                        #work if creating from scratch
                        json.dump(current_gui_data, file, indent=4, separators=(',', ': '))
                        print("broken gui data")
                file.close()
                Popen("python game_operations.py")
        
        elif self.start_stop.cget("text") == "STOP":
            self.start_stop.config(text="START")
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
                    for n in range(len(data)):
                        for key in data[n]:
                            if key == self.window:
                                del data[n]
                                file.close()
                                with open("data.json", "w+") as file:
                                    try:
                                        json.dump(data, file, indent=4, separators=(',', ': '))
                                    finally:
                                        file.close()
            except:
                pass
            try:
                with open("gui_data.json", "r") as file:
                    print ("try")
                    gui_data = json.load(file)
                    print ("here")
                    for n in range(len(gui_data)):
                        for key in gui_data[n]:
                            if key == self.window:
                                print("deleting")
                                del gui_data[n]
                                file.close()
                                with open("gui_data.json", "w+") as file:
                                    try:
                                        json.dump(gui_data, file, indent=4, separators=(',', ': '))
                                    except:
                                        pass
            except:
                pass

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
                for option in self.options:
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
# Button(f2, text="window1", command=f1).pack()
# Button(f1, text="window2", command=f2).pack()

class FarmingInfo:
    def __init__(self):
        self.coordinates = []
        self.is_active = False
        self.resource =  "None"
        self.commander = "None"

def delete_on_exit():
    try:
        os.remove("data.json")
    except:
        print("cannot find")
    try:
        os.remove("gui_data.json")
    except:
        print("cannot find")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", delete_on_exit)

if __name__ == "__main__":
    root.mainloop()
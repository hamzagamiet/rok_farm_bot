from tkinter import *
from tkinter import ttk
from pathlib import Path
import os
from game_operations import main
from bot_settings import wood_action, stone_action, gold_action, food_action
from multiprocessing import Process
import threading
import time
import win32gui

#INITIAL DECLARATIONS
BASE_DIR = Path(__file__).resolve().parent
ICON_DIR = os.path.join(BASE_DIR, "icons", "rokbot_logo.png")
root = Tk()

def create_combobox(root, options):
    node = ttk.Combobox(root, value = options)
    node.current()
    return node

def change_window(frame):
    frame.tkraise()


root.title("ROKBot")
root.call('wm', 'iconphoto', root._w, PhotoImage(file=ICON_DIR))

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
        self.instance_treeview.grid(row = 1, column = 1, columnspan = 4, padx =25, pady = 2, sticky="nsew")
        self.instance_treeview.bind("<Double-1>", self.OnDoubleClick)

    def OnDoubleClick(self, event):
        item = self.instance_treeview.selection()
        for i in item:
            instance = self.instance_treeview.item(i, "values")[0]
        show_frame(FarmingWindow(self.root, instance))

class FarmingWindow(Frame):
    def __init__(self, root, window):
        Frame.__init__(self)
        n = 100
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
        self.page_title = Label(root, text = window)
        self.window = window
        self.page_title.grid(row = n+1, column = 1, pady = 2, sticky="nsew")
        self.is_active1.grid(row = n+3, column = 1, pady = 2, sticky="nsew")
        self.node1.grid(row = n+3, column = 3, pady = 2, sticky="nsew")
        self.is_active2.grid(row = n+4, column = 1, pady = 2, sticky="nsew")
        self.node2.grid(row = n+4, column = 3, pady = 2, sticky="nsew")
        self.is_active3.grid(row = n+5, column = 1, pady = 2, sticky="nsew")
        self.node3.grid(row = n+5, column = 3, pady = 2, sticky="nsew")
        self.is_active4.grid(row = n+6, column = 1, pady = 2, sticky="nsew")
        self.node4.grid(row = n+6, column = 3, pady = 2, sticky="nsew")
        self.is_active5.grid(row = n+7, column = 1, pady = 2, sticky="nsew")
        self.node5.grid(row = n+7, column = 3, pady = 2, sticky="nsew")
        self.start_stop.grid(row = n+8, column = 1, padx=25, pady = 2, sticky="nsew")
    
    def start_bot_thread(self):
        threading.Thread(target=self.start_bot()).start()

    def start_bot(self):
        requested_actions = self.march_info()
        print ("attempt")
        if self.start_stop.cget("text") == "START":
            self.start_stop.config(text="STOP")
        elif self.start_stop.cget("text") == "STOP":
            self.start_stop.config(text="START")
        break_loop = False
        while self.start_stop.cget("text") == "STOP":
            root.update()
            for action in requested_actions:
                if self.start_stop.cget("text") == "STOP":
                    root.update()
                    print ("me too")
                    main(action, len(requested_actions), self.window)
                if self.start_stop.cget("text") == "START":
                    print ("breaking loop")
                    break_loop = True
                    break
            if break_loop:
                print ("broken loop")
                break

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
                requested_actions.append(wood_action)
            elif node == "food":
                requested_actions.append(food_action)
            elif node == "stone":
                requested_actions.append(stone_action)
            elif node == "gold":
                requested_actions.append(gold_action)

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

if __name__ == "__main__":
    root.mainloop()

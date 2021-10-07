from tkinter import *
from tkinter import ttk
from pathlib import Path
import os

#INITIAL DECLARATIONS
BASE_DIR = Path(__file__).resolve().parent
ICON_DIR = os.path.join(BASE_DIR, "icons", "rokbot_logo.png")

root = Tk()
root.title("ROKBot")
root.call('wm', 'iconphoto', root._w, PhotoImage(file=ICON_DIR))

root.geometry("500x500")
root.minsize(500,500)
root.maxsize(500,500)
my_menu = Menu(root)
root.config(menu=my_menu)

style = ttk.Style(root)
print(f"THEME NAMES:\n{style.theme_names()}")
style.theme_use("classic")

#FUNCTIONS
def our_command():
    pass

#CREATE ITEMS
account = Menu(my_menu)
my_menu.add_cascade(label="Bot",menu=account)
activate = Menu(my_menu)
my_menu.add_cascade(label="Activate", menu=activate)
activate.add_command(label="Enter Key", command=our_command)
activate.add_separator()
activate.add_command(label="Buy Key", command=our_command)
discord = Menu(my_menu)
my_menu.add_cascade(label="Discord", menu=discord)

my_label1 = Label(root, text="Hello World 1!")
my_label2 = Label(root, text="Hello World 2!")
my_label3 = Label(root, text="Hello World 3!")
my_button1 = Button(root, text="Click Me!")
my_button2 = Button(root, text="Click Me!")
my_button3 = Button(root, text="Click Me!")



#DISPLAY ITEMS
my_label1.grid(row=0, column = 0)
my_label2.grid(row=0, column = 1)
my_label3.grid(row=0, column = 2)
my_button1.grid(row=1, column = 1)
my_button2.grid(row=2, column = 1)
my_button3.grid(row=3, column = 1)

root.mainloop()
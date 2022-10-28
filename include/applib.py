import  tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory

def erase_text(textbox):
    textbox.delete(0,"end")
def filePathQuery():
    global path_button_text
    path_button_text = askdirectory(title='Please enter a file path')
def switchButtonState(button):
    if (button['state'] == tk.NORMAL):
        button['state'] = tk.DISABLED
    else:
        button['state'] = tk.NORMAL
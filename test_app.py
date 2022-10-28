#!/usr/bin/env python
import  tkinter as tk
#from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askdirectory


app = tk.Tk()
filename_label = Label(app, text="Please enter a file path:", font=("Times 22 bold"))
filepath = ""
filename = Entry(app, width = 40)

def switchButtonState():
    if (button1['state'] == tk.NORMAL):
        button1['state'] = tk.DISABLED
    else:
        button1['state'] = tk.NORMAL
def connectBluetooth():
   button2['text'] = "Disconnect Bluetooth"
   print("test") 
   switchButtonState()
def filePathQuery():
    global path_button_text
    path_button_text = askdirectory(title='Please enter a file path')
app.title("Test Application")
app.geometry("1000x1000")
filename_label.pack()
button1 = tk.Button(app, text="Please choose file path", command=filePathQuery)
button1.pack()
filename_label.pack()
filename.focus_set()
filename.pack()
button1 = tk.Button(app, text="Begin Testing",state=tk.DISABLED)
button2 = tk.Button(app, text="Connect to Module",command = connectBluetooth)
button1.pack()
button2.pack()
app.mainloop()
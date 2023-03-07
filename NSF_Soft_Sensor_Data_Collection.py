#!/usr/bin/env python
import  tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import bluetooth as BLE
from datetime import datetime
from queue import Queue
import serial.tools.list_ports

#automatically create the filename for if the use would like to keep it as is
#filename = str('arduino_mocap' + datetime.now().strftime("%m_%d_%Y-%H_%M"))

#initializes the window
app = tk.Tk()
app.title("NSF Soft Sensor Data Collection")
#app.iconphoto()
app.resizable()
icon = PhotoImage(file="uml-logo.png")
app.iconphoto(False, icon)

width = app.winfo_screenwidth()
height = app.winfo_screenwidth()

app.geometry(f"{width}x{height}")

#Initialize all existing variables

path_button_text = tk.StringVar(master=app, value="")

tk_mocap_bool = tk.IntVar()

tk_mocap_bool.set(1)

connect_button = tk.Button(app, text="Connect Bluetooth", command= lambda : bluetooth_obj.connectBluetooth(name="FlexibleSensorBLE"))

begin_button = tk.Button(app, text="Begin Testing",state=tk.DISABLED, command= lambda : bluetooth_obj.bluetoothRetData(name=path_button_text.get() + filename_entry.get() + datetime.now().strftime("%m_%d_%Y-%H_%M"), bool=tk_mocap_bool, serial_obj=com_choice))

t_frame = Frame(app)
hor = Scrollbar(t_frame, orient="horizontal")
hor.pack(side=BOTTOM, fill=X)
vert = Scrollbar(t_frame)
vert.pack(side=RIGHT, fill=Y)
term = Text(t_frame, state=DISABLED, background="light gray", width = int(width/16), height= int(height/35), wrap=NONE, undo=True, xscrollcommand=hor.set, yscrollcommand=vert.set)

queue = Queue(maxsize=1)

bluetooth_obj = BLE.bluetooth(queue, term, connect_button, begin_button)

#create entry and label for filename

filename_label = Label(app, text="File Name of Saved Data:", font=("Arial 12 bold"))
filename_entry = Entry(app, width= 50)
filename_entry.delete(0,"end")
filename_entry.insert(0, str('qtpy_mocap'))

filepath_label = Label(app, text="Please enter a file path:", font=("Arial 12 bold"))
filepath_button = tk.Button(app, text="Please choose file path", command= lambda : filePathQuery())

def filePathQuery():
        temp_name = askdirectory(title='Please enter a file path')
        temp_name = temp_name[2:]
        if(temp_name == None):
                path_button_text.set(temp_name)
        else:
                path_button_text.set(temp_name + "/")
        term['state'] = tk.NORMAL
        term.insert(END, "Path Changed To: "+ path_button_text.get() + "\n")
        term.see(END)
        term['state'] = tk.DISABLED

#Create the text at the top and put in to the left
header_label = Label(app, text="To Begin Collecting Data, Please enter the following information", font=("Arial 18 bold"))
#Changes the file name when the checkbox for mocap is changed
def mocap_entry(): 
        if tk_mocap_bool.get() == 1:
                filename_entry.delete(0,"end")
                filename_entry.insert(0, str('qtpy_mocap'))
                term['state'] = tk.NORMAL
                term.insert(END,"MOCAP Enabled\n")
                term.insert(END, "Name Changed To: " + filename_entry.get()+"\n")
                term.see(END)
                term['state'] = tk.DISABLED
        else:
                filename_entry.delete(0,"end")
                filename_entry.insert(0, str('qtpy'))
                term['state'] = tk.NORMAL
                term.insert(END,"MOCAP Disabled\n")
                term.insert(END, "Name Changed To: " + filename_entry.get()+"\n")
                term.see(END)
                term['state'] = tk.DISABLED

#Create the checkbox
mocap_box = Checkbutton(app, text="Are you Syncing with MOCAP?", variable=tk_mocap_bool, onvalue=1, offvalue=0, command= lambda : mocap_entry())

com_options = []
com_choice = StringVar(app)

com_text = Label(app, text="Select COM Port for Mocap (Ignore if not needed):", font="Arial 11 bold")
com_drop = ttk.OptionMenu(app, com_choice, *com_options)

def com_list():
        com_choice.set('')
        com_drop.set_menu(None)
        for p in serial.tools.list_ports.comports():
                com_options.append(p)
        for option in com_options:
                com_drop['menu'].add_command(label=option, command=tk._setit(com_choice, option))
com_list()

tags_label = Label(app, text="Data Collection Labels", font=("Arial 12 bold"))
walking_button = tk.Button(app, text="Walking (1)", command= lambda : bluetooth_obj.change_state(1))
jogging_button = tk.Button(app, text="Jogging (2)", command= lambda : bluetooth_obj.change_state(2))
sitting_button = tk.Button(app, text="Sitting (3)", command= lambda : bluetooth_obj.change_state(3))
standing_button = tk.Button(app, text="Standing (4)", command= lambda : bluetooth_obj.change_state(4))
idle_button = tk.Button(app, text="Idle (0)", command= lambda : bluetooth_obj.change_state(0))

info_text = Label(app, text="This Application is to be used in the NSF Soft Sensor Project run by UMass Lowell.", font="Arial 11 bold")
filepath_label.place(relx=0.01, rely=0.1, anchor='nw')
filepath_button.place(relx=0.15, rely=0.1, anchor='nw')
info_text.place(relx=0.0, rely= 0.90)
header_label.place(relx=0.01, rely=0.002, anchor='nw')
filename_label.place(relx=0.01, rely=0.15, anchor='nw')
filename_entry.place(relx=0.12, rely=0.15, anchor='nw')
mocap_box.place(relx=0.01, rely=0.05, anchor='nw')
connect_button.place(relx=0.18, rely=0.20, anchor='nw')
begin_button.place(relx=0.188, rely=0.25, anchor='nw')

tags_label.place(relx=0.17, rely=0.35, anchor='nw')
walking_button.place(relx=0.1, rely=0.38, anchor='nw')
jogging_button.place(relx=0.15, rely=0.38, anchor='nw')
sitting_button.place(relx=0.2, rely=0.38, anchor='nw')
standing_button.place(relx=0.25, rely=0.38, anchor='nw')
idle_button.place(relx=0.30, rely=0.38, anchor='nw')

com_drop.place(relx=0.23, rely=0.30, anchor='nw')
com_text.place(relx=0.01, rely=0.305, anchor='nw')

term.pack()
hor.config(command=term.xview)
vert.config(command=term.yview)
t_frame.place(relx=0.45, rely=0.05, anchor='nw')

#filename_entry.bind("<FocusIn>", applib.erase_text(filename_entry))
#app.after(5000, com_list)
app.mainloop()
s = Scrollbar()
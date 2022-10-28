import  tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from include import applib

def connectBluetooth(button):
   button['text'] = "Disconnect Bluetooth"
   print("test") 
   applib.switchButtonState(button)
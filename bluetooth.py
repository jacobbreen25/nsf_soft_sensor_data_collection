"""
Description: A class for starting and
"""

import asyncio
from bleak import BleakScanner, BleakClient, backends 
import sys
import platform
import struct
import threading
from tkinter import *
import  tkinter as tk
import csv
import queue as queue
import time
import serial

state = 0

class bluetooth:  
    """
     Name: __init__
     Params: self
     Description: Initialize the object and create private data variables
     Date Last Changed: 11/18/22
     Author: Jacob Breen
    """
    def __init__(self, q : queue, term, connect, begin):
        self.client = 0
        self.arduino_ble = backends.device.BLEDevice(0)

        #self.Thread = threading.Thread(target= self.dataRetrieve())
        self.terminal = term
        self.conn_button = connect
        self.begin_button = begin

        self.outfileWritable = 0
        self.outfile = 0

        self.queue = q

        self.data = queue.Queue()
        
        self.int_1 = "eb523251-6513-11ed-9c9d-0800200c9a66".format(0xFFE1)
        

    """
    Name: callback
    Params: self, characteristic (of type BleakGATTCharacteristic), data (of type bytearray) 
    Description: Initialize the object and create private data variables
    Date Last Changed: 11/18/22
    Author: Jacob Breen
    """
    def __callback(self, characteristic, d : bytearray):
        data_array = d.decode().rstrip().split('\t')
        #threading.Thread(self.__print__(data_array))
        threading.Thread(self.__write_to_file__(self.outfileWritable, self.outfile, data_array)).start() 
        threading.Thread(self.__print__(data_array))     

    """
    Name: __print
    Params: self
    Description: print the data inside the data dictionary
    Date Last Changed: 11/18/22
    Author: Jacob Breen
    """
    def __print__(self, list : list):
        self.terminal['state'] = tk.NORMAL
        self.terminal.delete('end -1 l','end')
        self.terminal.insert('end', str(list[0]) +': '+'\t')
        self.terminal.insert('end', str(list[1]) +'\t')
        self.terminal.insert('end', str(list[2])+'\t')
        self.terminal.insert('end', str(list[3])+'\t')
        self.terminal.insert('end', str(list[4])+'\t')
        self.terminal.insert('end', str(list[5])+'\t')
        self.terminal.insert('end', str(list[6])+'\t')
        self.terminal.insert('end', str(list[7])+'\t')
        self.terminal.insert('end', str(list[8]) + '\t')
        self.terminal.insert('end', str(state))
        self.terminal.see(END)
        self.terminal['state'] = tk.DISABLED

    """
    Name: __write_to_file__
    Params: self,oFileWriter,oFile,list
    Description: writes data to specified file
    Date Last Changed: 11/18/22
    Author: Jacob Breen
    """
    def __write_to_file__(self, oFileWriter, oFile, list : list):
        list[0] = float(list[0])/1000
        list.append(state)
        oFileWriter.writerow(list)
        oFile.flush() 
    
    """
    Name: __connectBLE
    Params: self, name (of type string)
    Description: connect to the bluetooth signal named {name}
    Date Last Changed: 11/18/22
    Author: Jacob Breen
    """
    async def __connectBLE(self, name : str):
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name == name:
                self.arduino_ble = d
    
    
    """
    Name: __retrieve
    Params: self
    Description: begin retrieving data from the bluetooth signal
    Date Last Changed: 12/22/22
    Author: Jacob Breen
    """

    async def __retrieve__(self, filename : str):
        with open(filename + ".csv", 'w+',newline='') as self.outfile:
            self.outfileWritable = csv.writer(self.outfile)
            self.terminal['state'] = tk.NORMAL
            self.terminal.insert(END, "Preparing to Collect...\n")
            self.terminal['state'] = tk.DISABLED

            def disconnect(client):
                if (self.queue.empty()):
                    self.queue.put(1)
                self.conn_button['text'] = "Connect Bluetooth"
                if(self.begin_button['text'] == "Stop Testing"):
                    self.begin_button['text'] = "Begin Testing"
                    self.switchButtonState(self.begin_button)
                else:
                    self.switchButtonState(self.begin_button)
            
            async with BleakClient(self.arduino_ble, disconnect_callback= lambda : disconnect, timeout=5.0) as self.client:
                try:
                    self.terminal['state'] = tk.NORMAL
                    self.terminal.insert(END, "Collecting Data...\n")
                    self.terminal.edit_separator()
                    self.terminal['state'] = tk.DISABLED
                    await self.client.start_notify(self.int_1, self.__callback)
                    await asyncio.sleep(0.02)
                    while self.queue.empty():
                        await asyncio.sleep(0.1)
                    await self.client.stop_notify(self.int_1)
                except Exception as e:
                    self.arduino_ble = 0
                    self.conn_button['text'] = "Connect Bluetooth"
                    self.conn_button['state'] = tk.NORMAL
                    self.begin_button['text'] = "Begin Testing"
                    self.begin_button['state'] = tk.DISABLED
                    self.terminal['state'] = tk.NORMAL
                    self.terminal.insert(END, "Hit exception \"")
                    self.terminal.insert(END, e)
                    self.terminal.see(END)
                    self.terminal.insert(END, "\" when collecting data\n")
                    self.terminal['state'] = tk.DISABLED
                    self.queue.put(0)
                    return
                self.queue.get()
                self.outfile.close()
                self.terminal['state'] = tk.NORMAL
                self.terminal.insert(END, "\nEnding Data Collection...\n")
                self.terminal.insert(END,"Disconnecting From QT Py...\n\n")
                self.terminal.see(END)
                self.terminal['state'] = tk.DISABLED

    """
    Name: dataRetrieve
    Params: self, filename
    Description: runs the asyncio coroutine for retrieving data
    Date Last Changed: 1/26/23
    Author: Jacob Breen
    """    
    def dataRetrieve(self, filename : str):
        t = asyncio.run(self.__retrieve__(filename))

    """
    Name: switchButtonState
    Params: self
    Description: switches button state
    Date Last Changed: 1/24/23
    Author: Jacob Breen
    """
    def switchButtonState(self, button):
        if (button['state'] == tk.NORMAL):
            button['state'] = tk.DISABLED
        else:
            button['state'] = tk.NORMAL

    """
    Name: connectBluetooth
    Params: self, name
    Description: starts the connection process for the bluetooth signal
    Date Last Changed: 11/18/22
    Author: Jacob Breen
    """
    def connectBluetooth(self, name : str):
        if name != "NULL":
            t = threading.Thread(target=self.connect, args=[name])
        if self.conn_button['text'] == "Connect Bluetooth":
            def wait_and_switch():
                while(t.is_alive()):
                    time.sleep(1)
                if self.arduino_ble.address != 0:
                    self.conn_button['text'] = "Disconnect Bluetooth"
                    self.conn_button['state'] = tk.NORMAL
                    self.begin_button['state'] = tk.NORMAL
                    self.terminal['state'] = tk.NORMAL
                    self.terminal.insert(END,"Found Bluetooth Device...\n")
                    self.terminal.see(END)
                    self.terminal['state'] = tk.DISABLED
                else:
                    self.conn_button['text'] = "Connect Bluetooth"
                    self.conn_button['state'] = tk.NORMAL
                    self.begin_button['state'] = tk.DISABLED
                    self.terminal['state'] = tk.NORMAL
                    self.terminal.insert(END,"Could Not Find Bluetooth Device\n")
                    self.terminal.see(END)
                    self.terminal['state'] = tk.DISABLED
            self.conn_button['state'] = tk.DISABLED
            t.start()
            threading.Thread(target=wait_and_switch).start()
        else:
            if (self.queue.empty()):
                self.queue.put(1)
            self.terminal['state'] = tk.NORMAL
            self.terminal.insert(END,"Disconnecting From Arduino...\n")
            self.terminal['state'] = tk.DISABLED
            self.conn_button['text'] = "Connect Bluetooth"
            if(self.begin_button['text'] == "Stop Testing"):
                self.begin_button['text'] = "Begin Testing"
                self.switchButtonState(self.begin_button)
            else:
                self.switchButtonState(self.begin_button)

    """
    Name: bluetoothRetData
    Params: self, name, bool, serial_obj
    Description: starts bluetooth data returning and (if mocap is enabled) begins mocap system
    Date Last Changed: 1/26/23
    Author: Jacob Breen
    """    
    def bluetoothRetData(self, name : str, bool : bool, serial_obj):
        if self.arduino_ble.address == 0: 
            self.terminal['state'] = tk.NORMAL
            self.terminal.insert(END, "No Arduino Found")
            self.terminal['state'] = tk.DISABLED
            return
        if self.begin_button['text'] == "Begin Testing":
            if name.find('/') == -1:
                self.terminal['state'] = tk.NORMAL
                self.terminal.insert(END, "\nPlease Insert File Path\n")
                self.terminal.see(END)
                self.terminal['state'] = tk.DISABLED
                return
            t = threading.Thread(target= self.dataRetrieve, args=[name])
            t.start()
            if(bool.get() == 1):
                threading.Thread(target=self.mocap_start, args=[serial_obj]).start()
            def wait_for_end():
                while(t.is_alive()):
                    if not self.queue.empty():
                        self.begin_button['state'] = tk.DISABLED
                    time.sleep(1)
                self.begin_button['state'] = tk.NORMAL
            threading.Thread(target=wait_for_end).start()
            self.begin_button['text'] = "Stop Testing"
            #self.switchButtonState()
        else:
            self.queue.put(1)
            #threading.Thread(target=ble.dataHault).start()
            self.begin_button['text'] = "Begin Testing"
            #self.switchButtonState(self.begin_button)

    """
    Name: connect
    Params: self, iName
    Description: runs the asyncio coroutine for connecting the BLE
    Date Last Changed: 1/26/23
    Author: Jacob Breen
    """
    def connect(self, iName : str):
        asyncio.run(self.__connectBLE(name=iName))

    """
    Name: mocap_start
    Params: self, serial_obj
    Description: begins the mocap system
    Date Last Changed: 1/26/23
    Author: Jacob Breen
    """
    def mocap_start(self, serial_obj):
        port_name = serial_obj.get()
        port_name  = port_name[:port_name.find('-') - 1]
        if port_name == '':
            return
        mocap = serial.Serial(port=port_name, baudrate=300)
        mocap.write(1)
        mocap.close()
    """
    Name: change_state
    Params: self, chng_state
    Description: changes the state of the user by taking in a value 
    Date Last Changed: 1/26/23
    Author: Jacob Breen
    """
    def change_state(self, chng_state : int):
        global state
        state = chng_state


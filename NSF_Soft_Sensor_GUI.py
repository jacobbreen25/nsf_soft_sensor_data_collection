import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from threading import Thread
from datetime import datetime
from tkinter.filedialog import askdirectory
import time
import serial
import serial.tools.list_ports
import asyncio
from bleak import BleakScanner, BleakClient, backends 
import csv
import queue

class NSF_Gui(tk.Tk):
    """
    
    """
    def __init__(self, *args, **kwargs):
        self.experimentName = "qtpy"
        self.experimentPath = ""
        self.samplerate = 120
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        self.mocapList = []

        self.startTime = float
        self.endTesting = queue.Queue()
        self.bluetooth_command = queue.Queue()

        self.dataChar = "eb523251-6513-11ed-9c9d-0800200c9a66".format(0xFFE1)

        self.bluetooth_active = queue.Queue()

        #Thread(target=lambda : asyncio.run(self.__bluetooth_daemon()).start(), daemon=True).run()

        self.construct_gui()

    async def bluetooth_daemon(self):
        while self.bluetooth_active.empty():
            if(self.bluetooth_command):
                command = self.bluetooth_command.get()
                if(command == "connect"):
                    await self.connect_bluetooth()
                elif(command == "capture"):
                    await self.capture_bluetooth()
            asyncio.sleep(2)
    """
        Construct GUI

        Variables are denoted by the naming convention below:

        [Variable Type]VariableName ex. lFilePath

        l = Label
        e = Entry
        b = Button
        f = Frame
        d = Dropdown Menu
        c = Checkbox
    """
    def construct_gui(self):
        self.title("NSF Soft Sensor Data Collection")
        self.resizable()

        f = [tk.Frame(master=self)]
        lHeader = tk.Label(master=f[-1], text="NSF Soft Sensor Data Collection", font=self.title_font)
        lHeader.pack(side=tk.LEFT, pady=5)

        f.append(tk.Frame(master=self))
        lFilePath = tk.Label(master=f[-1], text="Log File Path ")
        self.bFilePath = tk.Button(master=f[-1], text="Select File Path", 
            command=lambda: self.filePathQuery(), width=50)
        lFilePath.pack(side=tk.LEFT, pady=5)
        self.bFilePath.pack(side=tk.LEFT, pady=5)

        f.append(tk.Frame(master=self))
        lFileName = tk.Label(master=f[-1], text="Log File Name ")
        self.eFileName = tk.Entry(master=f[-1], width=100)
        self.eFileName.insert(0, self.experimentName)
        lFileName.pack(side=tk.LEFT, pady=5)
        self.eFileName.pack(side=tk.LEFT, pady=5)

        f.append(tk.Frame(master=self))
        self.mocapBool = tk.IntVar(master=f[-1], value=0)
        lMocapCheck = tk.Label(master=f[-1], text="Check for Smart MOCAP Enabling ")
        cMocapCheck = tk.Checkbutton(master=f[-1], variable=self.mocapBool, command=self.mocapChecked)
        lMocapCheck.pack(side=tk.LEFT, pady=5)
        cMocapCheck.pack(side=tk.LEFT, pady=5)

        f.append(tk.Frame(master=self))
        self.mocapCOM = tk.StringVar(master=f[-1])
        def acquireCOMList():
            self.mocapList = ['None']
            self.mocapCOM.set('None')
            for p in serial.tools.list_ports.comports():
                self.mocapList.append(p)
            self.print("COM Options Reset\n")
        lMocapList = tk.Label(master=f[-1], text="Choose COM Port if using MOCAP ")
        dMocapList = ttk.OptionMenu(f[-1], self.mocapCOM, 'None', *self.mocapList)
        bMocapReset = tk.Button(master=f[-1], text="Reset COM Options", command=lambda: acquireCOMList(), width=20)
        lMocapList.pack(side=tk.LEFT, pady=5)
        dMocapList.pack(side=tk.LEFT, pady=5)
        bMocapReset.pack(side=tk.LEFT, pady=5)

        # tk.Slider widget for hz here

        f.append(tk.Frame(master=self))
        self.bBluetooth = tk.Button(master=f[-1], text="Connect Bluetooth", 
            command=lambda: Thread(target=lambda : self.bluetooth_command.put("connect")).run(), 
                                   width=50)
        self.bTesting = tk.Button(master=f[-1], text="Begin Testing", 
         command=lambda: Thread(target=lambda : self.bluetooth_command.put("capture")).run(), 
                                width=50, state=tk.DISABLED)
        self.bBluetooth.pack(side=tk.LEFT, pady=5, padx=5)
        self.bTesting.pack(side=tk.LEFT, pady=5, padx=5)
        
        f.append(tk.Frame(master=self))
        hor = tk.Scrollbar(f[-1], orient="horizontal")
        hor.pack(side=tk.BOTTOM, fill=tk.X)
        vert = tk.Scrollbar(f[-1])
        vert.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal = tk.Text(f[-1], state=tk.DISABLED, background="light gray", wrap=tk.NONE, undo=True, xscrollcommand=hor.set, yscrollcommand=vert.set)
        self.terminal.pack(side=tk.LEFT, pady=5)
        
        acquireCOMList()
        for frame in f:
             frame.pack()

    def filePathQuery(self):
        temp_name = askdirectory(title='Please enter a file path')
        temp_name = temp_name[2:]
        if(temp_name == None):
                self.experimentPath = temp_name
        else:
                self.experimentPath = (temp_name + "/")

    def mocapChecked(self):
        if(self.mocapBool.get()):
            self.mocapBool.set(1)
            self.print("Smart MOCAP Enabled\n")
        else:
            self.print("Smart MOCAP Disabled\n")
            self.mocapBool.set(0)

    """

    """
    async def connect_bluetooth(self, name : str):
        #self.bleDevice = backends.device.BLEDevice(0)
        self.bleClient = None
        self.bBluetooth['state'] = tk.DISABLED
        if(self.bBluetooth['text'] != "Disconnect Bluetooth"):
            devices = await BleakScanner.discover()
            for d in devices:
                #self.print(str(d) + "\n")
                if d.name == name:
                    self.bleClient = BleakClient(d, disconnected_callback= lambda : self.disconnect_callback(), timeout=5.0)
                    await self.bleClient.connect()
                    self.bBluetooth['text'] = "Disconnect Bluetooth"
                    self.bTesting['state'] = tk.NORMAL
                    self.print("Connected to " + name + "\n")
        else:
            if (self.bleClient.is_connected):  
                await self.bleClient.disconnect()
                self.bBluetooth['text'] = "Connect Bluetooth"
                self.fprint("Successfully disconnected from " + name + "\n")
            else:
                self.print("Wasn't connected at first!\n")
        if(self.bleClient is None):
            self.print("Could not find " + name + "\n")
        self.bBluetooth['state'] = tk.NORMAL

    """
    
    """
    async def callback(self, characteristic, d : bytearray):
        if (self.can_take):
            data_array = d.decode().rstrip().split('\t')
            self.clearln()
            self.print(data_array)
            self.write(data_array)

    """
    
    """    
    async def capture_bluetooth(self):
        self.bTesting['state'] = tk.DISABLED
        if(self.bTesting['text'] == "Begin Testing"):
            self.print("Beginning Test...\n")
            if (self.bleClient.is_connected()):
                with open(self.experimentPath + self.eFileName.get() + datetime.now().strftime("%m_%d_%Y-%H_%M") + ".csv",
                'w+',newline='') as self.outfile:
                    self.outfileWritable = csv.writer(self.outfile)
                    try:
                        self.bTesting['text'] = "Stop Testing"
                        self.bTesting['state'] = tk.NORMAL
                        if(self.mocapBool.get()):
                            port_name = self.mocapCOM.get()
                            port_name  = port_name[:port_name.find('-') - 1]
                            if port_name != '':
                                serial = serial.Serial(port=port_name, baudrate=300)
                                serial.write(1)
                                serial.close()
                        await self.bleClient.start_notify(self.dataChar, callback=lambda : self.callback)
                        await asyncio.sleep(0.02)
                        while self.endTesting.empty():
                            await asyncio.sleep(0.05)
                        await self.bleClient.stop_notify()
                    except Exception as e:
                        self.print(str(e) + "\n")
                    self.endTesting.get()
                    self.outfile.close()
            else:
                self.print("Bluetooth disconnected unexpectedly. Please try connecting again...\n")
                self.bTesting['state'] = tk.DISABLED
                self.bBluetooth['text'] = "Connect Bluetooth"
        else:
            self.endTesting.put(1)
            self.bTesting['text'] = "Begin Testing"
    
    """
    
    """
    def disconnect_callback(self, client):
        print("disconnected")
        return

    def clearln(self):
        self.terminal['state'] = tk.NORMAL
        self.terminal.replace()
        self.terminal.delete("end-1l", tk.END)
        self.terminal['state'] = tk.DISABLED

    def print(self, printable : str, index = tk.END):
        self.terminal['state'] = tk.NORMAL
        self.terminal.insert(index, printable)
        self.terminal['state'] = tk.DISABLED

    def write(self, writable : list):
        #writable.insert(0, datetime.time.microseconds())
        self.outfileWritable.writerow(writable)
        
if __name__ == "__main__":
    app = NSF_Gui()
    #asyncio.run(app.bluetooth_daemon()).start()
    app.mainloop()
        
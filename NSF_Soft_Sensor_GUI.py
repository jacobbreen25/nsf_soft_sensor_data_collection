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
from functools import wraps
import math
from ratelimit import limits, sleep_and_retry

glb_command = str

class FlexSense_Gui(tk.Tk):
    
    """
    __init__

    Initializes the object and sets everything up for use
    """

    def __init__(self, *args, **kwargs):
        self.experimentName = "qtpy"
        self.experimentPath = ""
        self.samplerate = 60
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.label = "Idle"
        self.mocapList = []
        self.can_take = bool
        self.startTime = float
        self.endTesting = queue.Queue()
        self.bluetooth_command = queue.Queue()
        self.bleClient = None
        self.dataChar = "eb523251-6513-11ed-9c9d-0800200c9a66".format(0xFFE1)

        self.isActive = True      

    """
        Construct GUI

        Construst the GUI and sets up all buttons and functionality

        Variables are denoted by the naming convention below:

        Variable Type]VariableName ex. lFilePath

        l = Label
        e = Entry
        b = Button
        f = Frame
        d = Dropdown Menu
        c = Checkbox
        s = Slider
        sp = Spinbox
    """

    async def construct_gui(self):
        self.title("NSF Soft Sensor Data Collection")
        self.resizable()
        self.tasks = []
        icon = tk.PhotoImage(file="uml-logo.png")
        self.iconphoto(False, icon)

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
            self.dMocapList['menu'].delete(0,'end')
            self.mocapList = ['None']
            self.mocapCOM.set('None')
            for p in serial.tools.list_ports.comports():
                self.mocapList.append(p)
            for option in self.mocapList:
                self.dMocapList['menu'].add_command(label=option, command=tk._setit(self.mocapList, option))
            self.print("COM Options Reset\n")
        lMocapList = tk.Label(master=f[-1], text="Choose COM Port if using MOCAP ")
        self.dMocapList = ttk.OptionMenu(f[-1], self.mocapCOM, 'None', *self.mocapList)
        bMocapReset = tk.Button(master=f[-1], text="Update COM Options", command=lambda: acquireCOMList(), width=20)
        lMocapList.pack(side=tk.LEFT, pady=5)
        self.dMocapList.pack(side=tk.LEFT, pady=5)
        bMocapReset.pack(side=tk.LEFT, pady=5)

        # tk.Slider widget for hz here

        f.append(tk.Frame(master=self))
        lHz = tk.Label(master=f[-1], text="Slide to Desired Sample Rate (Hz):")
        def sliderCommand(event):
            self.samplerate = self.sHz.get()
            self.print("Sample Rate set to " + str(self.samplerate) + "Hz\n")
        self.sHz = tk.Scale(master=f[-1], from_= 60, to_=120, resolution=20, tickinterval=20, length=200, orient="horizontal", command=sliderCommand)
        lHz.pack(side=tk.LEFT, pady=5)
        self.sHz.pack(side=tk.LEFT, pady=5)

        f.append(tk.Frame(master=self))
        def connect():
            global glb_command
            glb_command = "connect"
            return
        
        def capture():
            global glb_command
            glb_command = "capture"
            if(self.bTesting['text'] == "Stop Testing"):
                self.endTesting.put(1)
            #print("Test")
            return

        self.bBluetooth = tk.Button(master=f[-1], text="Connect Bluetooth", command= lambda: Thread(connect()), width=50)
        self.bTesting = tk.Button(master=f[-1], text="Begin Testing", command=lambda: Thread(capture()), width=50, state=tk.DISABLED)
        self.bBluetooth.pack(side=tk.LEFT, pady=5, padx=5)
        self.bTesting.pack(side=tk.LEFT, pady=5, padx=5)
        
        f.append(tk.Frame(master=self))
        self.bIdle = tk.Button(master=f[-1], text="Idle/Transition", command= lambda: Thread(setLabel(self.bIdle, "Idle")), state=tk.DISABLED)
        self.disabledButton = self.bIdle
        bWalking = tk.Button(master=f[-1], text="Walking", command= lambda: Thread(setLabel(bWalking, "Walking")))
        bJogging = tk.Button(master=f[-1], text="Jogging", command= lambda: Thread(setLabel(bJogging, "Jogging")))
        bSitToStand = tk.Button(master=f[-1], text="Sitting to Standing", command= lambda: Thread(setLabel(bSitToStand, "SitToStand")))
        bWalkInc = tk.Button(master=f[-1], text="Walking Incline", command= lambda: Thread(setLabel(bWalkInc, "WalkingIncline")))
        bWalkDec = tk.Button(master=f[-1], text="Walking Decline", command= lambda: Thread(setLabel(bWalkDec, "WalkingDecline")))
        bSquating = tk.Button(master=f[-1], text="Squating", command= lambda: Thread(setLabel(bSquating, "Squating")))
        bStepUp = tk.Button(master=f[-1], text="Step Up", command= lambda: Thread(setLabel(bStepUp, "StepUp")))
        bStepDown = tk.Button(master=f[-1], text="Step Down", command= lambda: Thread(setLabel(bStepDown, "StepDown")))
        def setLabel(button, label):
            self.disabledButton['state'] = tk.NORMAL
            self.disabledButton = button
            self.label = label
            self.disabledButton['state'] = tk.DISABLED
            return
        self.bIdle.pack(side=tk.LEFT, pady=5, padx=5)
        bWalking.pack(side=tk.LEFT, pady=5, padx=5)
        bJogging.pack(side=tk.LEFT, pady=5, padx=5)
        bSitToStand.pack(side=tk.LEFT, pady=5, padx=5)
        bWalkInc.pack(side=tk.LEFT, pady=5, padx=5)
        bWalkDec.pack(side=tk.LEFT, pady=5, padx=5)
        bSquating.pack(side=tk.LEFT, pady=5, padx=5)
        bStepUp.pack(side=tk.LEFT, pady=5, padx=5)
        bStepDown.pack(side=tk.LEFT, pady=5, padx=5)

        f.append(tk.Frame(master=self))
        lTimer = tk.Label(master=f[-1], text="Set how long you want the label to run for:")
        lTimer.pack(side=tk.LEFT, pady=5, padx=5)

        f.append(tk.Frame(master=self))
        self.spHours = ttk.Spinbox(master=f[-1], from_= 0, to=1000, increment=1, width=5)
        self.spMinutes = ttk.Spinbox(master=f[-1], from_= 0, to=1000, increment=1, width=5)
        self.spSeconds = ttk.Spinbox(master=f[-1], from_= 0, to=1000, increment=1, width=5)
        self.spHours.set(0)
        self.spMinutes.set(0)
        self.spSeconds.set(0)
        self.spHours.pack(side=tk.LEFT, pady=5, padx=5)
        self.spMinutes.pack(side=tk.LEFT, pady=5, padx=5)
        self.spSeconds.pack(side=tk.LEFT, pady=5, padx=5)

        f.append(tk.Frame(master=self))
        lHours = tk.Label(master=f[-1], text="Hours")
        lMinutes = tk.Label(master=f[-1], text="Minutes")
        lSeconds = tk.Label(master=f[-1], text="Seconds")
        lHours.pack(side=tk.LEFT, pady=5, padx=5)
        lMinutes.pack(side=tk.LEFT, pady=5, padx=5)
        lSeconds.pack(side=tk.LEFT, pady=5, padx=5)


        f.append(tk.Frame(master=self))
        hor = tk.Scrollbar(f[-1], orient="horizontal")
        hor.pack(side=tk.BOTTOM, fill=tk.X)
        vert = tk.Scrollbar(f[-1])
        vert.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal = tk.Text(f[-1], state=tk.DISABLED, background="light gray", wrap=tk.NONE, undo=True, xscrollcommand=hor.set, yscrollcommand=vert.set)
        self.terminal.pack(side=tk.LEFT, pady=5)
        hor.config(command=self.terminal.xview)
        vert.config(command=self.terminal.yview)
        
        grip = ttk.Sizegrip(self)
        grip.pack(side="right", anchor="se")

        acquireCOMList()

        for task in self.tasks:
            await task
        for frame in f:
             frame.pack()
    
    """
    filePathQuery

    Queries the user for what file path they would like
    """

    def filePathQuery(self):
        temp_name = askdirectory(title='Please enter a file path')
        temp_name = temp_name[2:]
        if(temp_name == None):
                self.experimentPath = temp_name
        else:
                self.experimentPath = (temp_name + "/")

    """
    mocapChecked

    Event that happens when the MOCAP checkbox is checked 
    """

    def mocapChecked(self):
        if(self.mocapBool.get()):
            self.mocapBool.set(1)
            self.print("Smart MOCAP Enabled\n")
        else:
            self.print("Smart MOCAP Disabled\n")
            self.mocapBool.set(0)

    """
    connect_bluetooth

    Takes a name and connects to a bluetooth device given that name.
    """

    async def connect_bluetooth(self, name : str):
        #self.bleDevice = backends.device.BLEDevice(0)
        #self.bleClient = None
        
        self.bBluetooth['state'] = tk.DISABLED
        self.update()
        if(self.bBluetooth['text'] != "Disconnect Bluetooth"):
            self.print("Connection processing...\n")
            devices = await BleakScanner.discover()
            for d in devices:
                #self.print(str(d) + "\n")
                if d.name == name:
                    try:
                        self.bleClient = BleakClient(d, disconnected_callback= self.disconnect_callback, timeout=3.0)
                        await self.bleClient.connect()
                        self.bBluetooth['text'] = "Disconnect Bluetooth"
                        self.bTesting['state'] = tk.NORMAL
                        self.print("Connected to " + name + "\n")
                        break
                    except Exception as e:
                        self.bBluetooth['state'] = tk.NORMAL
                        self.print("ERR: " + str(e) + "\n")
                else:
                    self.bleClient = None
        else:
            self.print("Disconnection processing...\n")
            if (self.bleClient.is_connected):  
                await self.bleClient.disconnect()
                #self.bBluetooth['text'] = "Connect Bluetooth"
                #self.bTesting['state'] = tk.DISABLED
                self.print(" " + name +" successfully!", "end-2c")
            else:
                self.print("Wasn't connected at first!\n")
        if(self.bleClient is None):
            self.print("Could not find " + name + "\n")
        self.bBluetooth['state'] = tk.NORMAL
        self.update()

    """
    callback

    A callback ran after every packet is received
    """
    
    async def callback(self, characteristic, d : bytearray):
        #if (self.can_take):
        #print(self.lastPacketTime) - pow(10,9)/60
        #if((self.lastPacketTime + pow(10,9)/30 >= time.time_ns()) and (self.lastPacketTime + pow(10,9)/120 <= time.time_ns())):
        #if((self.lastPacketTime + pow(10,9)/120 <= time.time_ns())):
        #print(self.lastPacketTime)
        #print("Start Time:" + str(time.time()))
        data_array = d.decode().rstrip().split('\t')
        currenttime = int(data_array[0])
        if (self.lastPacketTime is None or currenttime - self.lastPacketTime >= (1000 - 130)/int(self.samplerate)):
            data_array.append(self.label)
            self.clearln()
            self.print("\n")
            self.print(data_array)
            self.write(data_array)
            self.lastPacketTime = currenttime
            #print("Final Time:" + str(time.time()))

    """
    capture_bluetooth

    Begins capturing data from the bluetooth device connected
    """  

    async def capture_bluetooth(self):
        self.bTesting['state'] = tk.DISABLED
        self.sHz['state'] = tk.DISABLED
        self.bBluetooth['state'] = tk.DISABLED
        self.update()
        if(self.bTesting['text'] == "Begin Testing"):
            self.print("Beginning Test...\n")
            if (self.bleClient.is_connected):
                with open(self.experimentPath + self.eFileName.get() + datetime.now().strftime("%m_%d_%Y-%H_%M") + ".csv",
                'w+',newline='') as self.outfile:
                    self.outfileWritable = csv.writer(self.outfile)
                    try:
                        self.bTesting['text'] = "Stop Testing"
                        self.bTesting['state'] = tk.NORMAL
                        self.update()
                        if(self.mocapBool.get()):
                            port_name = self.mocapCOM.get()
                            port_name  = port_name[:port_name.find('-') - 1]
                            if port_name != '':
                                serial = serial.Serial(port=port_name, baudrate=300)
                                serial.write(1)
                                serial.close()
                        self.lastPacketTime = None
                        await self.bleClient.start_notify(self.dataChar, callback= self.callback)
                        await asyncio.sleep(0)
                        while self.endTesting.empty():
                            self.update()
                            await asyncio.sleep(0)
                        await self.bleClient.stop_notify(self.dataChar)
                        await asyncio.sleep(0)
                    except Exception as e:
                        await asyncio.sleep(0)
                        self.outfile.close()
                        self.print(str(e) + "\n")
                    self.print("\n")
                    self.endTesting.get()
                    await asyncio.sleep(0)
                    self.outfile.close()
            else:
                self.sHz['state'] = tk.NORMAL
                self.bTesting['state'] = tk.DISABLED
                self.bBluetooth['text'] = "Connect Bluetooth"
                self.bBluetooth['state'] = tk.NORMAL
                self.print("Bluetooth disconnected unexpectedly. Please try connecting again...\n")
        else:
            self.print("Ending Test...\n")
            self.sHz['state'] = tk.NORMAL
            self.bBluetooth['state'] = tk.NORMAL
            self.bTesting['text'] = "Begin Testing"
            self.bTesting['state'] = tk.NORMAL
    
    """
    disconnect_callback

    Runs after device disconnects and puts app into disconnected state
    """

    def disconnect_callback(self, client):
        self.bBluetooth['text'] = "Connect Bluetooth"
        self.bBluetooth['state'] = tk.NORMAL
        self.bTesting['text'] = "Begin Testing"
        self.bTesting['state'] = tk.DISABLED
        self.print("Disconnected from device\n")
        return
    
    """
    clearln

    Clears the line on the terminal
    """

    def clearln(self):
        self.terminal['state'] = tk.NORMAL
        #self.terminal.replace()
        self.terminal.delete("end-1l", tk.END)
        self.terminal['state'] = tk.DISABLED
    
    """
    print 

    Prints whatever is given as printable at the given index
    """

    def print(self, printable : str, index = tk.END):
        self.terminal['state'] = tk.NORMAL
        self.terminal.insert(index, printable)
        self.terminal['state'] = tk.DISABLED
        self.terminal.see(tk.END)
        self.update()
    
    """
    write

    Writes whatever was given as writable into a csv file
    """

    def write(self, writable : list):
        #writable.insert(0, datetime.time.microseconds())
        self.outfileWritable.writerow(writable)
    
    """
    bluetoothDaemon

    Runs a daemon that looks for a command and runs a certain function given the command
    """

    async def bluetoothDaemon(self):
        global glb_command
        while(self.isActive):
            #time.sleep(0.01)
            self.update()
            if (glb_command == "connect"):
                glb_command = str
                task = asyncio.create_task(self.connect_bluetooth("FlexibleSensorBLE"))
                await task
            elif (glb_command == "capture"):
                glb_command = str
                task = asyncio.create_task(self.capture_bluetooth())
                await task
            await asyncio.sleep(0)

    """
    timeDaemon

    Daemon for the built in timer for labels
    """

    async def timeDaemon(self):
        self.timeStarted = False
        while(self.isActive):
            if(self.disabledButton != self.bIdle):
                if(self.spSeconds.get() == "0" and self.spMinutes.get() == "0" and self.spHours.get() == "0"):
                    self.spHours['state'] = tk.NORMAL
                    self.spMinutes['state'] = tk.NORMAL
                    self.spSeconds['state'] = tk.NORMAL
                    self.disabledButton['state'] = tk.NORMAL
                    self.disabledButton = self.bIdle
                    self.label = "Idle"
                    self.disabledButton['state'] = tk.DISABLED
                    self.timeStarted = False
                    self.print("Label time has finished\n")
                    i = 3
                    while(i != 0):
                        self.terminal.config(background= "red")
                        await asyncio.sleep(.5)
                        self.terminal.config(background="light gray")
                        await asyncio.sleep(0.25)
                        i = i - 1
                else:
                    if(not self.timeStarted):
                        self.print("Label time has Started\n")
                        self.timeStarted = True
                    self.spHours['state'] = tk.DISABLED
                    self.spMinutes['state'] = tk.DISABLED
                    self.spSeconds['state'] = tk.DISABLED
                    if(self.spHours.get() == ""):
                        self.spHours.set(0)
                    if(self.spMinutes.get() == ""):
                        self.spMinutes.set(0)
                    if(self.spSeconds.get() == ""):
                        self.spSeconds.set(0)
                    
                    temp = int(self.spHours.get())*3600 + int(self.spMinutes.get()) * 60 + int(self.spSeconds.get())
                    if(temp != 0):
                        await asyncio.sleep(1)
                        temp = temp - 1
                        hours = int(temp/3600)
                        minutes = int((temp - hours*3600)/60)
                        seconds = int(temp - minutes*60 - hours*3600)
                        self.spHours.set(hours)
                        self.spMinutes.set(minutes)
                        self.spSeconds.set(seconds)
                    
            else:
                self.timeStarted = False
                self.spHours['state'] = tk.NORMAL
                self.spMinutes['state'] = tk.NORMAL
                self.spSeconds['state'] = tk.NORMAL
            await asyncio.sleep(0)
    """
    destroy

    Deletes the object and closes all daemons
    """

    def destroy(self):
        self.isActive = False
        if(self.bleClient is not None and self.bleClient.is_connected):
            self.bleClient.disconnect()
        tk.Tk.destroy(self)

if __name__ == "__main__":
    async def asyncio_main():
        app = FlexSense_Gui()
        await app.construct_gui()
        task1 = asyncio.create_task(app.bluetoothDaemon())
        #task2 = asyncio.create_task(app.clockDaemon())
        task3 = asyncio.create_task(app.timeDaemon())
        def endProg():
            app.destroy()
        app.protocol('WM_DELETE_WINDOW', endProg)
        await task1
        #await task2
        await task3
        


    
    asyncio.run(asyncio_main())
        
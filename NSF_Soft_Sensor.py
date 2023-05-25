import asyncio
from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic
import csv
import queue
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    overload,
)
#from threading import Thread
#import serial
#import serial.tools.list_ports
#from functools import wraps


class FlexSense_Bluetooth():
    
    def __init__(self):
        """
        Initializes the object and sets everything up for use
        """
        self.endTesting = queue.Queue()
        self._connected = False   

    async def connect(self, name : str, disconnect_callback = None):
        """
        Takes a name and connects to a bluetooth device given that name.
            Params:
                name:
                    Name of the bluetooth device
                disconnect_callback:
                    A callback ran when the the bluetooth device disconnects. default is None
        """
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name == name:
                try:
                    self.bleClient = BleakClient(d, disconnected_callback=disconnect_callback, timeout=3.0)
                    await self.bleClient.connect()
                    self._connected = True
                    break
                except:
                    raise
            else:
                self.bleClient = BleakClient(None)
        if(not self.bleClient.is_connected):
            raise ValueError("Could not find " + name)
    async def capture(self, characterstic, callback: Callable[
            [BleakGATTCharacteristic, bytearray], Union[None, Awaitable[None]]
        ]):
            """
            Begins capturing data from the bluetooth device connected 
                Params:
                    characteristic: 
                        The characteristic you are collecting data from. 
                    callback: 
                        Callback for the bluetooth device, should have 2 params, a characteristic param and a bytearray param
            """
            self.char = characterstic
            if (self._connected and self.bleClient.is_connected):
                try:
                    await self.bleClient.start_notify(characterstic, callback= callback)
                except:
                    raise
            #self.endTesting.get()
  
    def is_connected(self):
        """
        Returns true if the bluetooth device is connected and false otherwise 
        """     
        return (self._connected and self.bleClient.is_connected)

    async def endCapture(self):
        """
        Ends the data collection
        """
        await self.bleClient.stop_notify(self.char)
        #self.endTesting.put(1)

    async def disconnect(self):
        """
        Disconnects the bluetooth device
        """
        if (self._connected and self.bleClient.is_connected):
            try:
                await self.bleClient.disconnect()
            except:
                raise
    
    def destroy(self):
        """
        Deletes the object and closes all daemons
        """
        self.isActive = False

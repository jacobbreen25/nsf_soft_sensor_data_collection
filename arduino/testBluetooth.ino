#include <ArduinoBLE.h>

/*
* Purpose: The purpose of this program is to controll a peripheral device(Flexible Sensor Board) and send that data to a Server(PC)
* Author: Jacob Breen
* Date Started: 11/10/22
* Date Last Worked on: 11/10/22
*
* Version: 00.00.01
*/

// Server UUID is eb523250-6513-11ed-9c9d-0800200c9a66

// Client UUID is eb523257-6513-11ed-9c9d-0800200c9a66

BLEService MessageService("eb523250-6513-11ed-9c9d-0800200c9a66"); 

BLEFloatCharacteristic float_1("eb523251-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEFloatCharacteristic float_2("eb523252-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEFloatCharacteristic float_3("eb523253-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEFloatCharacteristic float_4("eb523254-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEFloatCharacteristic float_5("eb523255-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEFloatCharacteristic float_6("eb523256-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
void setup() {
  // put your setup code here, to run once:
  SerialUSB.begin(57600);
  if(!BLE.begin()){
    SerialUSB.println("BLE Failed");
  }

  //Sets the name of the bluetooth device
  BLE.setDeviceName("FlexibleSensorBLE");
  BLE.setLocalName("FlexibleSensorBLE");
  //Adds the data as characteristics so it can be sent using GATT bluetooth protocol
  MessageService.addCharacteristic(float_1);
  MessageService.addCharacteristic(float_2);
  MessageService.addCharacteristic(float_3);
  MessageService.addCharacteristic(float_4);
  MessageService.addCharacteristic(float_5);
  MessageService.addCharacteristic(float_6);
  //Add the service to the bluetooth.
  BLE.addService(MessageService);
  //Adverts the bluetooth 
  BLE.advertise();
  SerialUSB.println("Nano is waiting for connections...");
}
void loop() {
  BLEDevice central = BLE.central();

  if(central){
    SerialUSB.print("Connected to device: ");
    SerialUSB.println(central.address());
    while(central.connected()){
      float_1.writeValue(1.11);
      float_2.writeValue(2.22);
      float_3.writeValue(3.33);
      float_4.writeValue(4.44);
      float_5.writeValue(5.55);
      float_6.writeValue(6.66);
    }
    SerialUSB.print("Disconnected from Device: ");
    SerialUSB.println(central.address());
  }
}

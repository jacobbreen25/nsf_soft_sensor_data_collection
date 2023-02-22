/*
* Name: six_capacitive_sensor_bluetooth
* Purpose: The purpose of this program is to controll a peripheral device(Flexible Sensor Board) and send that data to a Server(PC)
* Author: Jacob Breen
* Date Started: 11/11/22
* Date Last Worked on: 11/15/22
*
* Version: 00.00.01
*/

// Server UUID is eb523250-6513-11ed-9c9d-0800200c9a66

// Extra UUID is eb523257-6513-11ed-9c9d-0800200c9a66 if needed for sending commands through another characteristic.

// ***** 1. Import libraries *****
#include <Wire.h>
#include <math.h> // For log base n
#include <ArduinoBLE.h>
#include <String.h>



// ***** 2. Initialize Variables *****
// 2.1 Control driver's high-level behavior
bool use_mpr = true; // **USER** True: read from MPR. False: read from Faboratory circuit
bool print_verbose = false; // **USER** True: display the time elapsed since starting (in milliseconds). False: don't display time elapsed.

// 2.2. General Variables. No need to modify these.
bool first = 1;

int avg = 0;
int avg_count = 0;
int fin = 710;
bool led_on = false;

unsigned long initial_time = 0.0; // The time after setup
unsigned long sample_rate = 100; // How many samples per second. For highest timing accuracy, choose something that divides evenly into 1000
unsigned long current_time = 0; // The time elapsed since startup until the beginning of the current sample
unsigned long time_int = 0;
unsigned long start_time = 0;
unsigned long sample_number = 0; // How many samples we have taken since startup
String comp_data;
String data_1;
String data_2;
String data_3;
String data_4;
String data_5;
String data_6;
String data_7;
String data_8;
String time_data;

//uint8_t *byte_data;
//create the service that will send data to the arduino
BLEService MessageService("eb523250-6513-11ed-9c9d-0800200c9a66"); 
//create the characteristics that will be used to send the data through bluetooth and initialize tham as Readable and Notifyable
BLEStringCharacteristic data_char("eb523251-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify, 51);
// ***** 3. Set up Arduino *****
void setup() {
// 3.1 Initialize communication lines
  Serial.begin(57600);

  pinMode(A1, OUTPUT);
  pinMode(A0, INPUT);

  initial_time = millis(); // Initial time
  current_time = 0;

  // initialize BLE
  if(!BLE.begin()){
    Serial.println("BLE Failed");
  }
  touchSetCycles(0x0000, 0xFFFF);
  analogReadResolution(12);
  //Sets the name of the bluetooth device, both locally and for a device
  BLE.setDeviceName("FlexibleSensorBLE");
  BLE.setLocalName("FlexibleSensorBLE");
  //Adds the data as characteristics so it can be sent using GATT bluetooth protocol
  MessageService.addCharacteristic(data_char);
  //Add the service to the bluetooth.
  BLE.addService(MessageService);
  //Adverts the bluetooth 
  BLE.advertise();
  Serial.println("\nNano is waiting for connections...");
}

// ***** 4. Read sensors and send to PC over Bluetooth, forever *****
void loop() {
  int value;
  // 4.1 Print current time, increment sample number
  if (print_verbose) {
    Serial.print(current_time); Serial.print('\t'); // Print time elapsed since setup finished
  }
  sample_number++; // Increment sample number

  //set central device variable
  BLEDevice central = BLE.central();
  //if central is initialized
  if(central){
    //we are connected to a device. Print out such and the devices address
    //if we actually have a connection, send the data recieved from the sensors
    if(central.connected()){
      initial_time = millis();
      Serial.print("Connected to device: ");
      Serial.println(central.address());
      if(first){
        start_time = millis();
        first = 0;
      }
      
      data_1 = String(touchRead(A2));
      data_2 = String(touchRead(A3));
      data_3 = String(touchRead(SDA));
      data_4 = String(touchRead(SCL));
      data_5 = String(touchRead(TX));
      data_6 = String(touchRead(MOSI));
      data_7 = String(touchRead(MISO));
      data_8 = String(touchRead(SCK));
      time_data = String(millis() - start_time);

      comp_data = time_data+'\t'+data_1+'\t'+data_2+'\t'+data_3+'\t'+data_4+'\t'+data_5+'\t'+data_6+'\t'+data_7+'\t'+data_8;

      data_char.writeValue(comp_data);

      finishCycle();
    }else{//if we are disconnected from the device, we print out such.
      first = 1;
      Serial.print("Disconnected from Device: ");
      Serial.println(central.address());
    }
  }
  int current_volt = analogReadMilliVolts(A0);
  //Serial.println(current_volt);
  if(avg_count < 1000){
    avg += current_volt;
    avg_count++;
  }else{
    fin = (float)avg/avg_count;
    avg_count = 0;
    avg = 0;
  }
  if(fin < 830){
    //Serial.println("Low");
    digitalWrite(A1, HIGH);
  }else if(fin > 840){
    digitalWrite(A1, LOW);
  }
  // 4.4 Delay so that we have the proper sample rate (samples/second), as defined by 
  //finishCycle(); // Print over serial
}

// ***** 5. Helper Functions *****
void finishCycle() {
  // Delay for 'time_per_sample' [ms], print newline character
  unsigned long comp_time = millis() - initial_time;
  int time_per_sample = 1000/sample_rate;
  if(time_per_sample > comp_time){
    delay(time_per_sample - comp_time);
    //Serial.println("Waiting")    
  }else{
    Serial.print("ERR: Not Waiting "); Serial.print("time_per_sample = "); Serial.print(time_per_sample); Serial.print("comp_time = "); Serial.println(comp_time);
  }
  //current_time = millis() - initial_time; // Store current millis for future
  //SerialUSB.print("\n");
}

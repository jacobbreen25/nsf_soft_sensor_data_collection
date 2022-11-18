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
#include "Adafruit_MPR121.h" // For MPR 121
#include <ArduinoBLE.h>



// ***** 2. Initialize Variables *****
// 2.1 Control driver's high-level behavior
bool use_mpr = true; // **USER** True: read from MPR. False: read from Faboratory circuit
bool print_verbose = false; // **USER** True: display the time elapsed since starting (in milliseconds). False: don't display time elapsed.

// 2.2. General Variables. No need to modify these.
unsigned long initial_time = 0.0; // The time after setup
unsigned long sample_rate = 100; // How many samples per second. For highest timing accuracy, choose something that divides evenly into 1000
unsigned long current_time = 0; // The time elapsed since startup until the beginning of the current sample
unsigned long sample_number = 0; // How many samples we have taken since startup
Adafruit_MPR121 cap = Adafruit_MPR121(); // An MPR121 object. Can initialize more MPR121s as additional objects. The address is specified later, in setup as a cap.begin() call

//create the service that will send data to the arduino
BLEService MessageService("eb523250-6513-11ed-9c9d-0800200c9a66"); 
//create the characteristics that will be used to send the data through bluetooth and initialize tham as Readable and Notifyable
BLEIntCharacteristic int_1("eb523251-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEIntCharacteristic int_2("eb523252-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEIntCharacteristic int_3("eb523253-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEIntCharacteristic int_4("eb523254-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEIntCharacteristic int_5("eb523255-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);
BLEIntCharacteristic int_6("eb523256-6513-11ed-9c9d-0800200c9a66", BLERead | BLENotify);


// ***** 3. Set up Arduino *****
void setup() {
// 3.1 Initialize communication lines
  Wire.begin(); // Start the I2C bus for communicating with the sensors' PCBs over the green (clock or SCL) and blue (data or SDA) wires
  //Serial.begin(2e6); // Start serial port for communicating with the PC over USB
  SerialUSB.begin(57600);
  while (!SerialUSB) {}
  // 3.2 Initialize MPR121, if we are using that. 
  // Most users don't need to read through this section. We kept the comments to help understand what the MPR121 is doing.
  if (use_mpr) {
    // Advanced users: Default MPRS121 address is 0x5A. If the ADDR pin on the MPR121 is connected to 3.3V, the I2C address is 0x5B. If connected to SDA it's 0x5C, and if SCL then 0x5D.
    if (!cap.begin(0x5A)) {
      SerialUSB.println("MPR121 not found, check wiring?"); // Something went wrong when the Arduino tried to intialize the MPR121 that has the specified address
    }

    // Auto-configure charge time and charge current for MPR121. 
    // Advanced users: See section 12 (p 16) of 2010 datasheet, or Page 17 of 2013 datasheet. Note that AFES was renamed as FFI, but the register is the same 0x7B (which is what really matters)
    cap.writeRegister(MPR121_AUTOCONFIG0, 0b00010001); // Only keep 8 least-significant bits, convert to binary. FFI --6 samples (matches the Adafruit_MPR121.cpp MPR121_CONFIG1, as required). RETRY --> Retry 2 times. BVA --> No change. Auto-reconfig disabled, enable auto-config

    // Specify the search boundaries and target for the auto-configuration. Values for Vdd = 3.3V are 200, 180, 130.
    //cap.writeRegister(MPR121_UPLIMIT, 200);     // ((Vdd - 0.7)/Vdd) * 256 
    //cap.writeRegister(MPR121_TARGETLIMIT, 180); // UPLIMIT * 0.9
    //cap.writeRegister(MPR121_LOWLIMIT, 130);    // UPLIMIT * 0.65
    cap.writeRegister(MPR121_UPLIMIT, 220);     // ((Vdd - 0.7)/Vdd) * 256 Vdd = 5V
    cap.writeRegister(MPR121_TARGETLIMIT, 198); // UPLIMIT * 0.9
    cap.writeRegister(MPR121_LOWLIMIT, 143);    // UPLIMIT * 0.65


  }

  initial_time = millis(); // Initial time
  current_time = 0;

  // initialize BLE
  if(!BLE.begin()){
    SerialUSB.println("BLE Failed");
  }

  //Sets the name of the bluetooth device, both locally and for a device
  BLE.setDeviceName("FlexibleSensorBLE");
  BLE.setLocalName("FlexibleSensorBLE");
  //Adds the data as characteristics so it can be sent using GATT bluetooth protocol
  MessageService.addCharacteristic(int_1);
  MessageService.addCharacteristic(int_2);
  MessageService.addCharacteristic(int_3);
  MessageService.addCharacteristic(int_4);
  MessageService.addCharacteristic(int_5);
  MessageService.addCharacteristic(int_6);
  //Add the service to the bluetooth.
  BLE.addService(MessageService);
  //Adverts the bluetooth 
  BLE.advertise();
  SerialUSB.println("\nNano is waiting for connections...");
}

// ***** 4. Read sensors and send to PC over Bluetooth, forever *****
void loop() {
  int value;
  // 4.1 Print current time, increment sample number
  if (print_verbose) {
    SerialUSB.print(current_time); SerialUSB.print('\t'); // Print time elapsed since setup finished
  }
  sample_number++; // Increment sample number
  //SerialUSB.println("test");

  // 4.2 Read from sensors, depending on the value of "use_mpr" (set at the beginning of this script)
   //for (int sensor = 0; sensor < NUM_SENSORS; sensor++) {
  //}
  //SerialUSB.print(cap.filteredData(0)); Serial.print('\t');
  //SerialUSB.print(cap.filteredData(1)); Serial.print('\t');
  //SerialUSB.print(cap.filteredData(2)); Serial.print('\t');
  //SerialUSB.print(cap.filteredData(3)); Serial.print('\t');
  //SerialUSB.print(cap.filteredData(4)); Serial.print('\t');
  //SerialUSB.print(cap.filteredData(5)); Serial.print('\t');

  //set central device variable
  BLEDevice central = BLE.central();
  //if central is initialized
  if(central){
    //we are connected to a device. Print out such and the devices address
    SerialUSB.print("Connected to device: ");
    SerialUSB.println(central.address());
    //if we actually have a connection, send the data recieved from the sensors
    if(central.connected()){
      int_1.writeValue(cap.filteredData(0));
      SerialUSB.print(cap.filteredData(0)); Serial.print('\t');
      int_2.writeValue(cap.filteredData(1));
      SerialUSB.print(cap.filteredData(1)); Serial.print('\t');
      int_3.writeValue(cap.filteredData(2));
      SerialUSB.print(cap.filteredData(2)); Serial.print('\t');
      int_4.writeValue(cap.filteredData(3));
      SerialUSB.print(cap.filteredData(3)); Serial.print('\t');
      int_5.writeValue(cap.filteredData(4));
      SerialUSB.print(cap.filteredData(4)); Serial.print('\t');
      int_6.writeValue(cap.filteredData(5));
      SerialUSB.print(cap.filteredData(5)); Serial.print('\t');
    }else{//if we are disconnected from the device, we print out such.
      SerialUSB.print("Disconnected from Device: ");
      SerialUSB.println(central.address());
    }
  }
  // 4.4 Delay so that we have the proper sample rate (samples/second), as defined by 
  //finishCycle(); // Print over serial
}

// ***** 5. Helper Functions *****
void finishCycle() {
  // Delay for 'time_per_sample' [ms], print newline character
  unsigned long temp_millis = millis() - initial_time;
  int time_per_sample = 1000/sample_rate;
  delay(time_per_sample * sample_number - temp_millis);
  current_time = millis() - initial_time; // Store current millis for future
  SerialUSB.print("\n");
}
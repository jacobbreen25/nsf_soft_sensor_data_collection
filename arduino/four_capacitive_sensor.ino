/*************************************
  cap_sensor_driver.ino

  This driver is for testing capacitive sensor(s). There is functionality for the MPR121, our custom signal-conditioning board, and outputting a rising edge to an external device such as an Instron.

  Assumes your PIC firmware will send its previous sensor reading upon a read request. (All firmware as of 2019-10-29 is valid.)
  Sensor units are currently units of [instruction cyles]. A future commit of this repository will have everything in [ms]
  Typical parameters a user wants to edit marked by **USER**

  Written by Dylan Shah. Last edited 2021-01-06 YMD.
*************************************/



// ***** 1. Import libraries *****
#include <Wire.h>
#include <math.h> // For log base n
#include "Adafruit_MPR121.h" // For MPR 121



// ***** 2. Initialize Variables *****
// 2.1 Control driver's high-level behavior
bool use_mpr = true; // **USER** True: read from MPR. False: read from Faboratory circuit
bool print_verbose = false; // **USER** True: display the time elapsed since starting (in milliseconds). False: don't display time elapsed.
const int NUM_SENSORS = 1; // **USER** How many sensors will you use? If you are using Faboratory boards, you will need one Faboratory PCB for each sensor, and you need to add the addresses to the int array below, named "sensor_addresses". Each MPR121 PCB can connect to 12 sensors without needing to modify the rest of this code.
int sensor_addresses[NUM_SENSORS] = {0}; // **USER** Faboratory Sensor addresses. Not used if "use_mpr" is true.

// 2.2. General Variables. No need to modify these.
unsigned long initial_time = 0.0; // The time after setup
unsigned long sample_rate = 100; // How many samples per second. For highest timing accuracy, choose something that divides evenly into 1000
unsigned long current_time = 0; // The time elapsed since startup until the beginning of the current sample
unsigned long sample_number = 0; // How many samples we have taken since startup
Adafruit_MPR121 cap = Adafruit_MPR121(); // An MPR121 object. Can initialize more MPR121s as additional objects. The address is specified later, in setup as a cap.begin() call



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
}



// ***** 4. Read sensors and send to PC over Serial, forever *****
void loop() {
  // 4.1 Print current time, increment sample number
  if (print_verbose) {
    SerialUSB.print(current_time); SerialUSB.print('\t'); // Print time elapsed since setup finished
  }
  sample_number++; // Increment sample number


  // 4.2 Read from sensors, depending on the value of "use_mpr" (set at the beginning of this script)
   for (int sensor = 0; sensor < NUM_SENSORS; sensor++) {
    float temp_sensor = 0;
    // MPR
    if (use_mpr){ 
 //     temp_sensor = cap.filteredData(sensor); 
//        Serial.print(cap.filteredData(0)); Serial.print('\t');
//        Serial.print(cap.filteredData(4)); Serial.print('\t');
//       Serial.print(cap.filteredData(5)); Serial.print('\t');
//        Serial.print(cap.filteredData(6)); Serial.print('\t');
        SerialUSB.print(cap.filteredData(0)); Serial.print('\t');
        SerialUSB.print(cap.filteredData(1)); Serial.print('\t');
        SerialUSB.print(cap.filteredData(2)); Serial.print('\t');
        SerialUSB.print(cap.filteredData(3)); Serial.print('\t');
        SerialUSB.print(cap.filteredData(4)); Serial.print('\t');
        SerialUSB.print(cap.filteredData(5)); Serial.print('\t');
      }
    // Faboratory Board
    else { temp_sensor = read_faboratory_board(sensor_addresses[sensor]); }
    //Serial.print(temp_sensor); Serial.print('\t');
//    if (temp_sensor > 1) {
      //Serial.print(temp_sensor); Serial.print('\t');
//        Serial.print(cap.filteredData(0)); Serial.print('\t');
//        Serial.print(cap.filteredData(4)); Serial.print('\t');
//        Serial.print(cap.filteredData(5)); Serial.print('\t');
//        Serial.print(cap.filteredData(6)); Serial.print('\t');
//      }
  }
  // 4.4 Delay so that we have the proper sample rate (samples/second), as defined by 
  finishCycle(); // Print over serial
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


float read_faboratory_board(int in_address) {
  // Read the capacitive sensor
  Wire.requestFrom(in_address, 2); byte b1_local = Wire.read(); byte b2_local = Wire.read();
  float sensor_reading = (float)b1_local * 256 + (float)b2_local; // Convert into 16-bit timer value
  return sensor_reading;
}

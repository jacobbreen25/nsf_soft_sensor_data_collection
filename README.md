# nsf_soft_sensor_data_collection

## Installation
Firstly, Download the “NSF Soft Sensor Wizard”, run the application, and follow the download instructions.

![Install Wizard](https://user-images.githubusercontent.com/91704735/229606666-1a73bde9-ed8f-473c-a515-7631109a012f.PNG) 

## Usage
To use the app, firstly run the “NSF Soft Sensor Application” application

![Fullscreen App](https://github.com/jacobbreen25/nsf_soft_sensor_data_collection/assets/91704735/ac2e1287-854b-4136-aa3d-f0d12d549f21)

Next, choose where you would like to keep the .csv file created when collecting. Note: If you do not choose a file path, you will not be able to run the program.

Choose a name for the .csv file. The Program will automatically set a name for the file, depending on the time and if mocap is enabled. You will also see a "Set Sample Rate" drop down menu which allows you to choose what sample rate you will be testing at.

![File Name   File Path](https://github.com/jacobbreen25/nsf_soft_sensor_data_collection/assets/91704735/0be86d5e-f055-4603-a627-ff5536775653)

Once open, use the checkbox labeled “Check for Smart MOCAP Enabling” to specify if you are syncing with a MOCAP system. If you are using Smart MOCAP, choose which COM port you are using.

![COM Port](https://github.com/jacobbreen25/nsf_soft_sensor_data_collection/assets/91704735/5c8839d1-6d39-488e-8597-446dc533535b)

Use the “Connect Bluetooth” button to automatically find the bluetooth device. Once the bluetooth device is found, the terminal will say so and the “Begin Testing” button will become unshaded and the “Connect Bluetooth” will say “Disconnect Bluetooth”

![Connect+Disconnect Button](https://github.com/jacobbreen25/nsf_soft_sensor_data_collection/assets/91704735/aa05eb93-df9b-4f9d-bea9-065e1d2934be)

When ready to begin collecting data, press “Begin Testing”. You will see the terminal clear and show current data coming in, including local time to the QT Py, all sensors, including those that are not connected, and a final “Task” number. 

![Begin Testing](https://github.com/jacobbreen25/nsf_soft_sensor_data_collection/assets/91704735/ba2442cf-00e9-4d64-a47c-c4ac43af195e)

![Begin Testing 2](https://github.com/jacobbreen25/nsf_soft_sensor_data_collection/assets/91704735/e7c7da1a-ded8-4663-9193-b4a1e8c2c2ed)

While collecting, if you would like to change the “Task” of the participant, you can set how long you would liek to have the task run for and press the Data Collection Label buttons, which you will be able to visually see in the terminal when collecting. It is important that you set the timer first before pressing a task, as if you do not it will immediately go back to idle. When the task finishes, it will automatically go back to idle and flash the terminal red.

![Data Collection Labels](https://github.com/jacobbreen25/nsf_soft_sensor_data_collection/assets/91704735/1023e441-c6aa-4829-9377-c805aa5e9cac)

Once Finished Collecting, press the “Stop Testing” button which will end the collection.

![Stop Testing](https://github.com/jacobbreen25/nsf_soft_sensor_data_collection/assets/91704735/483ea17c-b1a6-4490-95c5-1c796b29e631)

Important Notes:

The program automatically adds a timestamp to the name of each .csv file to allow for continuous collection without rewriting of data.

## Arduino Installation

To use the QT Py's using Arduino, you will have to download the needed libraries for ESP-32 devices like so:

1. Open Arduino and open the File drop down
2. Got to Preferences
3. Add the following link ot the "Additional boards manager URLs" box at the bottom on the Preferences menu: https://adafruit.github.io/arduino-board-index/package_adafruit_index.json,https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_dev_index.json
4. Select ok
5. Go to Tools
6. Go To Board
7. Go to Board Manager
8. Use the search bar to look up esp32 in the search bar and download "esp32 by Espressif"

You will also have to download the ArduinoBLE library like so:
1. Open Arduino and Open the Tools drop down
2. Open Manage Libraries
3. Use the search bar to look up "ArduinoBLE by Arduino" and select the install button


### Contributors

Janelle Clark,
Jacob Breen,
Jacob Lorusso,
Emily LaBelle

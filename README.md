# nsf_soft_sensor_data_collection

## Installation
Firstly, Download the “NSF Soft Sensor Wizard”, run the application, and follow the download instructions.

![Install Wizard](https://user-images.githubusercontent.com/91704735/223492719-3708a12a-7776-49c9-8c02-6149e26e21e8.PNG)

## Usage

To use the app, firstly run the “NSF Soft Sensor Application” application. 

![Fullscreen App](https://user-images.githubusercontent.com/91704735/223492915-7d6fd88d-2ac9-4316-ac36-76304bbd3b42.PNG)

Once open, use the checkbox labeled “Are you syncing with MOCAP?” to specify if you are syncing with a MOCAP system. 

![MOCAP Checkbox](https://user-images.githubusercontent.com/91704735/223492961-399da026-9095-4a5b-8d9b-5b9fae6050f7.PNG)

Next, choose where you would like to keep the .csv file created when collecting. Note: If you do not choose a file path, you will not be able to run the program.

![File Path](https://user-images.githubusercontent.com/91704735/223493035-d420b2f0-04ff-4a75-b326-51151f299048.PNG)

Choose a name for the .csv file. The Program will automatically set a name for the file, depending on the time and if mocap is enabled. 

![File Name](https://user-images.githubusercontent.com/91704735/223493127-efa2bf05-6e5a-478b-9110-96cab65a19be.PNG)

Use the “Connect Bluetooth” button to automatically find the bluetooth device. Once the bluetooth device is found, the terminal will say so and the “Begin Testing” button will become unshaded and the “Connect Bluetooth” will say “Disconnect Bluetooth”

![Connect Button](https://user-images.githubusercontent.com/91704735/223493175-f3f96a70-1d96-40be-b0a2-5ab3e9deb13d.PNG)

Finally, if you are using MOCAP, choose the COM port the MOCAP is connected to. If none is chosen, it is essentially unchecking the MOCAP check box.

![COM Port](https://user-images.githubusercontent.com/91704735/223493211-8aa3162d-41a1-4ad3-85eb-2c68494bee1b.PNG)

When ready to begin collecting data, press “Begin Testing”. You will see the terminal clear and show current data coming in, including local time to the QT Py, all sensors, including those that are not connected, and a final “Task” number. 

![Begin Testing](https://user-images.githubusercontent.com/91704735/223493276-dba28c3c-9bbf-481a-aad2-7c4be081c979.PNG)
![Begin Testing 2](https://user-images.githubusercontent.com/91704735/223493307-ab0a08d7-08f5-4666-86d4-42b2ae65d151.PNG)

While collecting, if you would like to change the “Task” of the participant, you can press the Data Collection Label buttons, which you will be able to visually see in the terminal when collecting.

![Data Collection Labels](https://user-images.githubusercontent.com/91704735/223493361-aa7436f7-c03f-4d6e-a75f-3c63897aeaff.PNG)

Once Finished Collecting, press the “Stop Testing” button which will end the collection.

![Stop Testing](https://user-images.githubusercontent.com/91704735/223493399-205f146c-10da-4b5a-a6cb-7d1ddf694f62.PNG)

Important Notes:

The program automatically adds a timestamp to the name of each .csv file to allow for continuous collection without rewriting of data.


### Contributors

Janelle Clark,
Jacob Breen,
Jacob Lorusso,
Emily LaBelle

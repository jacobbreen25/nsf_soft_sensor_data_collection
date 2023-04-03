# nsf_soft_sensor_data_collection

## Installation
Firstly, Download the “NSF Soft Sensor Wizard”, run the application, and follow the download instructions.


## Usage
![Fullscreen App](https://user-images.githubusercontent.com/91704735/229606513-bfe8ea31-8a0b-442b-8cf0-3dc1039afeee.PNG)

To use the app, firstly run the “NSF Soft Sensor Application” application. 

![Fullscreen App](https://user-images.githubusercontent.com/91704735/229606085-1ba6714d-7f96-4025-b6ef-6292c55bfb0c.PNG)

Once open, use the checkbox labeled “Are you syncing with MOCAP?” to specify if you are syncing with a MOCAP system. 

![MOCAP Checkbox](https://user-images.githubusercontent.com/91704735/223492961-399da026-9095-4a5b-8d9b-5b9fae6050f7.PNG)

Next, choose where you would like to keep the .csv file created when collecting. Note: If you do not choose a file path, you will not be able to run the program.

![File Path](https://user-images.githubusercontent.com/91704735/223493035-d420b2f0-04ff-4a75-b326-51151f299048.PNG)

Choose a name for the .csv file. The Program will automatically set a name for the file, depending on the time and if mocap is enabled. You will also see a "Set Sample Rate" drop down menue which allows you to choose what sample rate you will be testing at.

![File Name   Sample Rate](https://user-images.githubusercontent.com/91704735/229606170-f4cfa128-683e-46f4-a748-0aacf1fcc169.PNG)

Use the “Connect Bluetooth” button to automatically find the bluetooth device. Once the bluetooth device is found, the terminal will say so and the “Begin Testing” button will become unshaded and the “Connect Bluetooth” will say “Disconnect Bluetooth”

![Connect Button](https://user-images.githubusercontent.com/91704735/229606210-99ba61b7-af5f-4b25-8431-d4fa4a8f74a2.PNG)

Finally, if you are using MOCAP, choose the COM port the MOCAP is connected to. If none is chosen, it is essentially unchecking the MOCAP check box.

![COM Port](https://user-images.githubusercontent.com/91704735/229606257-c5bf0ffe-74ae-41f0-bc5d-b0b6dd78b492.PNG)

When ready to begin collecting data, press “Begin Testing”. You will see the terminal clear and show current data coming in, including local time to the QT Py, all sensors, including those that are not connected, and a final “Task” number. 

![Begin Testing](https://user-images.githubusercontent.com/91704735/229605950-5d60c1be-aed7-41e7-97d6-03dd5ab430bf.PNG)
![Begin Testing 2](https://user-images.githubusercontent.com/91704735/229606036-78cda8a5-54ed-4f63-b1e2-3e1ac4971a91.PNG)

While collecting, if you would like to change the “Task” of the participant, you can press the Data Collection Label buttons, which you will be able to visually see in the terminal when collecting.

![Data Collection Labels](https://user-images.githubusercontent.com/91704735/229606287-e9537037-84db-4aa8-8f93-294c8c0778ca.PNG)

Once Finished Collecting, press the “Stop Testing” button which will end the collection.

![Stop Testing](https://user-images.githubusercontent.com/91704735/229606332-9c817163-1585-4dac-a6e5-bfcf4a8643e6.PNG)

Important Notes:

The program automatically adds a timestamp to the name of each .csv file to allow for continuous collection without rewriting of data.


### Contributors

Janelle Clark,
Jacob Breen,
Jacob Lorusso,
Emily LaBelle

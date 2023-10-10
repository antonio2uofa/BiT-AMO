# Balls in Tubes Experiment - Antonio Martin-Ozimek

This project aimed to create a software model of a MIMO system. Half of the completed work was put towards transferring the system from running on MATLAB and LabVIEW to running on Python and C++. This was accomplished by directly interfacing with RT-DAC/USB block controlling the system. The interfacing was done in C/C++ using predefined structs created by the company who created the hardware. The C/C++ code was then wrapped in Python code using the c_types library. 

The interfacing computer, the server, was connected to by a client PC using the [OPC-UA](https://github.com/FreeOpcUa/python-opcua) Python library. The client PC collects data from the server and implements multiprocessing to collect sensor data from the Server and collect image data from a live camera feed. The image processing is done mainly through the OpenCV library. The image data is used to track the experiment using a Computer Vision model developed by [Ultralytics](https://www.ultralytics.com/yolo). The model built to track the experiment uses their YOLOv7 algorithm. 

The ML model was used in conjunction with sensors attached to the experiment to create a system model using the optuna Python library. This created a system model that accurately predicted the system's responses to inputs and was able to control the system to a large degree of success.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary libraries for this project.

```bash
pip install -y -r requirements.txt
```

## Server Usage

To compile the necessary libraries on the server PC run these commands in your terminal in the project directory containing the makefile.

```bash
make all
```

To run the server script type this code into the terminal of the server PC.

```bash
python sync_server.py
```

## Client Usage

To run the client update the sync_client.py file as necessary and run this command on the client PC:

```bash
python sync_client.py
```

## Contributing

Please do not update this repository. Rather, copy this repository and then clone it to work on it locally.


# Balls in Tubes Experiment - Dr.Purushottama Rao Dasari

Comments about Antonio Martin-Ozimek on his co-op Term

He worked on the connectivity scheme for the Ball in tube experiment. The experiment was initially controlled via LabVIEW and MATLAB. He debugged the LabVIEW code and rewrote it in C to be able to control the experiment from Python. 

The communication between the experiment was done in LabVIEW and C, but was controlled by a Python program. This Python program was an OPC server that he created. He used a 64-bit machine as the OPC client to control the experiment and read/write data from the OPC server. Once he had created a working client and server, he worked on simulating PID controllers. 

He then worked on system identification as well as object tracking for the experiment. He used MATLAB’s system identification toolkit as well as PySINDy to develop a discrete-time series model. He finished up the model while also working on image processing for the object detection algorithm. He learned how to remove lens distortion and create images for the object detection algorithm to use. Finally, he worked on an MPC controller that would use the discrete-time model to control the experiment. 

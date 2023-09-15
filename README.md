# Balls in Tubes Experiment - Antonio Martin-Ozimek

For all necessary packages please refer to the requirements.txt file and install using pip install -y -r requirements.txt when it is in the current directory. The client is configured to work with the server running on the 32-bit PC. Please ensure the server is running before trying to connect with the client. All data is stored in the Data folder.

# Balls in Tubes Experiment - Dr.Purushottama Rao Dasari

Comments about Antonio Martin-Ozimek on his co-op Term

He worked on the connectivity scheme for the Ball in tube experiment. The experiment was initially controlled via LabVIEW and MATLAB. He debugged the LabVIEW code and rewrote it in C to be able to control the experiment from Python. 

The communication between the experiment was done in LabVIEW and C, but was controlled by a Python program. This Python program was an OPC server that he created. He used a 64-bit machine as the OPC client to control the experiment and read/write data from the OPC server. Once he had created a working client and server, he worked on simulating PID controllers. 

He then worked on system identification as well as object tracking for the experiment. He used MATLAB’s system identification toolkit as well as PySINDy to develop a discrete-time series model. He finished up the model while also working on image processing for the object detection algorithm. He learned how to remove lens distortion and create images for the object detection algorithm to use. Finally, he worked on an MPC controller that would use the discrete-time model to control the experiment. 

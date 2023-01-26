#include <stdio.h>
#include "rtdacusb.h"

int main() {
	RTDACUSBBufferType RTDACUSBBuffer;
	//unsigned int distance;

	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices > 0) {
		CommandRead_0111(&RTDACUSBBuffer);
		// write code to read from Ultrasonic Sensor
		//printf("%d", distance);
		USBClose();
	}
}

#include <stdio.h>
#include "rtdacusb.h"

int main() {
	// Initialize buffer that stores data for RT-DAC/USB
	RTDACUSBBufferType RTDACUSBBuffer;

	// Initialize variables that describe PWM
	unsigned int mode, prescaler, width;

	// Check if we successfully connected to RT-DAC/USB
	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices > 0) {
		// Check for values of PWM and return values
		CommandRead_0111(&RTDACUSBBuffer);
		mode = RTDACUSBBuffer.PWM[3].Mode;
		prescaler = RTDACUSBBuffer.PWM[3].Prescaler;
		width = RTDACUSBBuffer.PWM[3].Width;
		printf("%d,%d,%d", mode, prescaler, width);
		USBClose();
	}
}

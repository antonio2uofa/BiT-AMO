#include <stdio.h>
#include "rtdacusb.h"

int main() {
	RTDACUSBBufferType RTDACUSBBuffer;
	unsigned int mode, prescaler, width;

	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices > 0) {
		CommandRead_0111(&RTDACUSBBuffer);
		mode = RTDACUSBBuffer.PWM[2].Mode;
		prescaler = RTDACUSBBuffer.PWM[2].Prescaler;
		width = RTDACUSBBuffer.PWM[2].Width;
		printf("%d,%d,%d", mode, prescaler, width);
		USBClose();
	}
}

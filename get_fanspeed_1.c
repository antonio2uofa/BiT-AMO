#include <stdio.h>
#include "rtdacusb.h"

int main() {
	RTDACUSBBufferType RTDACUSBBuffer;
	unsigned int mode, prescaler, width;

	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices > 0) {
		CommandRead_0111(&RTDACUSBBuffer);
		mode = RTDACUSBBuffer.PWM[0].Mode;
		prescaler = RTDACUSBBuffer.PWM[0].Prescaler;
		width = RTDACUSBBuffer.PWM[0].Width;
		printf("%d,%d,%d", mode, prescaler, width);
		USBClose();
	}
}

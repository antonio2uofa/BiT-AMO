#include <stdio.h>
#include "rtdacusb.h"

int main() {
	RTDACUSBBufferType RTDACUSBBuffer;

	int NoOfDetectedUSBDevices = USBOpen();
	int level;

	if(NoOfDetectedUSBDevices <= 0) {
		printf("Cannot detect any USB devices.\n\n");
	} else {
		CommandRead_0111(&RTDACUSBBuffer);
		scanf("%d", &level);
		printf("Tube 2 set to: %d\n", level);
		RTDACUSBBuffer.PWM[1].Mode = 1;
		RTDACUSBBuffer.PWM[1].Prescaler = 127;
		RTDACUSBBuffer.PWM[1].Width = level;
		CommandSend_0111(&RTDACUSBBuffer);
		USBClose();
	}	
	return 0;
}

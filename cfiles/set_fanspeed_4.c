#include <stdio.h>
#include "rtdacusb.h"

int main() {
	// Initialize buffer that stores data for RT-DAC/USB
	RTDACUSBBufferType RTDACUSBBuffer;

	int level;

	// Check if we successfully connected to RT-DAC/USB
	int NoOfDetectedUSBDevices = USBOpen();
	
	if(NoOfDetectedUSBDevices <= 0) {
		printf("Cannot detect any USB devices.\n\n");
	} else {
		// Set width of selected PWM
		CommandRead_0111(&RTDACUSBBuffer);
		scanf("%d", &level);
		printf("Tube 4 set to: %d\n", level);
		RTDACUSBBuffer.PWM[3].Width = level;
		CommandSend_0111(&RTDACUSBBuffer);
		USBClose();
	}	
	return 0;
}

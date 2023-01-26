#include <stdio.h>
#include "rtdacusb.h"

int main() {
	RTDACUSBBufferType RTDACUSBBuffer;

	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices <= 0) {
		printf("Cannot detect any USB devices.\n\n");
	} else {
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.CN1PinMode = 0x0F;
		RTDACUSBBuffer.CN1Direction = 0x3FFFFF0;
		RTDACUSBBuffer.CN1Output = 0x0000000;
		CommandSend_0111(&RTDACUSBBuffer);

		USBClose();
	}	
	return 0;
}

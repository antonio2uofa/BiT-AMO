#include <stdio.h>
#include "rtdacusb.h"

int main() {
	RTDACUSBBufferType RTDACUSBBuffer;

	int NoOfDetectedUSBDevices = USBClose();

	if(NoOfDetectedUSBDevices <= 0) {
		printf("Cannot detect any USB device to close.\n\n");
	}
	return 0;
}

#include <stdio.h>
#include "rtdacusb.h"

RTDACUSBBufferType RTDACUSBBuffer;

int GetLevel(int tube) {

	int NoOfDetectedUSBDevices = USBOpen();
	int i;


	if(NoOfDetectedUSBDevices <= 0) {
		printf("Cannot detect any USB devices.\n\n");
	} else {
		CommandRead_0111(&RTDACUSBBuffer);
		while(i) {
			printf("%s\n", RTDACUSBBuffer.ApplicationName);
		}
		// To be written: code to find how to activate Trigger Pin,
		// Then calculate time between two falling edges between
		// Trigger pin and Echo Pin. Then calculate distance travelled
		// based on the speed of sound.
	}

	USBClose();

	return tube;
}

int main() {

	int myVar2 = GetLevel(1);

	return 0;
}
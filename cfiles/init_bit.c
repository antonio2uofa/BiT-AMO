#include <stdio.h>
#include "rtdacusb.h"

int main() {
	// Initialize buffer that stores data for RT-DAC/USB
	RTDACUSBBufferType RTDACUSBBuffer;

	// Initialize iterator
	int PWMPin;

	// Check if we successfully connected to RT-DAC/USB
	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices <= 0) {
		printf("Cannot detect any USB devices.\n\n");
	} else {
		CommandRead_0111(&RTDACUSBBuffer);
		// Set modes of DIO pins
		RTDACUSBBuffer.CN1PinMode = 0x1F;
		RTDACUSBBuffer.CN1Direction = 0x0033060;
		RTDACUSBBuffer.CN1Output = 0x0000000;

		// Reset both counters
		RTDACUSBBuffer.TmrCnt[0].Mode = 0;
		RTDACUSBBuffer.TmrCnt[0].Reset = 1;
		RTDACUSBBuffer.TmrCnt[1].Mode = 0;
		RTDACUSBBuffer.TmrCnt[1].Reset = 1;

		// Initialize signal generator with default values
		RTDACUSBBuffer.Generator[0].St1Len = 10;
		RTDACUSBBuffer.Generator[0].St2Len = 10;
		RTDACUSBBuffer.Generator[0].Enable = 1;
		RTDACUSBBuffer.Generator[0].SwStart = 1;
		RTDACUSBBuffer.Generator[0].InfiniteGeneration = 1;

		// Initialize PWM pulse values
		for(PWMPin = 0; PWMPin < 4; PWMPin++) {
			RTDACUSBBuffer.PWM[PWMPin].Mode = 1;
			RTDACUSBBuffer.PWM[PWMPin].Prescaler = 65;
			RTDACUSBBuffer.PWM[PWMPin].Width = 0;
		}

		CommandSend_0111(&RTDACUSBBuffer);

		USBClose();
	}	
	return 0;
}

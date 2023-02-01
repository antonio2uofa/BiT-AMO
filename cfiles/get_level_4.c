#include <stdio.h>
#include "rtdacusb.h"

int main() {
	// Initialize buffer that stores data for RT-DAC/USB
	RTDACUSBBufferType RTDACUSBBuffer;

	// Initialize variables
	int input, clock_1;
	int input_final = -1;

	// Check if we successfully connected to RT-DAC/USB
	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices > 0) {

		// Reset 1st counter in counter mode (Sensor 1 & 2 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.TmrCnt[0].Mode = 0;
		RTDACUSBBuffer.TmrCnt[0].Reset = 1;
		CommandSend_0111(&RTDACUSBBuffer);

		// Start 1st counter in counter mode (Sensor 1 & 2 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.TmrCnt[0].Mode = 0;
		RTDACUSBBuffer.TmrCnt[0].Reset = 0;
		CommandSend_0111(&RTDACUSBBuffer);
		
		// Set SEL0 signal to high (Sensors 1 & 3 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.CN1Output = 0x0000080;
		CommandSend_0111(&RTDACUSBBuffer);

		// Set Trigger pin to high (Sensor 1 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.CN1Output = 0x0400080;
		CommandSend_0111(&RTDACUSBBuffer);

		// Set Trigger pin to high (Sensor 1 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.CN1Output = 0x0000080;
		CommandSend_0111(&RTDACUSBBuffer);

		// Wait for echo pin to go to low state (Sensor 1 on schema.)
		while( input_final != 0) {
			CommandRead_0111(&RTDACUSBBuffer);
			input = RTDACUSBBuffer.CN1Input;
			input_final = input & 0x0001000;
		}

		// As soon as sensor goes to low read from counter (Sensor 1 on schema.)
		clock_1 = RTDACUSBBuffer.TmrCnt[0].Counter;
		CommandSend_0111(&RTDACUSBBuffer);

		printf("%d\n", clock_1);

		USBClose();
	}
}

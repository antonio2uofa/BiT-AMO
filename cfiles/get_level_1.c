#include <stdio.h>
#include "rtdacusb.h"

int main() {
	// Initialize buffer that stores data for RT-DAC/USB
	RTDACUSBBufferType RTDACUSBBuffer;

	// Initialize variables 
	int input, clock_2;
	int input_final = -1;

	// Check if we successfully connected to RT-DAC/USB
	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices > 0) {

		// Reset 2nd counter in counter mode (Sensor 3 & 4 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.TmrCnt[1].Mode = 0;
		RTDACUSBBuffer.TmrCnt[1].Reset = 1;
		CommandSend_0111(&RTDACUSBBuffer);

		// Start 2nd counter in counter mode (Sensor 3 & 4 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.TmrCnt[1].Mode = 0;
		RTDACUSBBuffer.TmrCnt[1].Reset = 0;
		CommandSend_0111(&RTDACUSBBuffer);
		
		// Set SEL1 signal to high (Sensors 2 & 4 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.CN1Output = 0x0000100;
		CommandSend_0111(&RTDACUSBBuffer);

		// Set Trigger pin to high (Sensor 4 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.CN1Output = 0x2000100;
		CommandSend_0111(&RTDACUSBBuffer);

		// Set Trigger pin to low (Sensor 4 on schema.)
		CommandRead_0111(&RTDACUSBBuffer);
		RTDACUSBBuffer.CN1Output = 0x0000100;
		CommandSend_0111(&RTDACUSBBuffer);

		// Wait for echo pin to go to low state (Sensor 4 on schema.)
		while( input_final != 0) {
			CommandRead_0111(&RTDACUSBBuffer);
			input = RTDACUSBBuffer.CN1Input;
			input_final = input & 0x0010000;
		}

		// As soon as sensor goes to low read from counter (Sensor 4 on schema.)
		clock_2	= RTDACUSBBuffer.TmrCnt[1].Counter;
		CommandSend_0111(&RTDACUSBBuffer);

		printf("%d\n", clock_2);

		USBClose();
	}
}
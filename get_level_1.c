#include <stdio.h>
#include "rtdacusb.h"

int main() {
	RTDACUSBBufferType RTDACUSBBuffer;
	//unsigned int distance;

	int NoOfDetectedUSBDevices = USBOpen();

	if(NoOfDetectedUSBDevices > 0) {
		CommandRead_0111(&RTDACUSBBuffer);
		// write code to read from Ultrasonic Sensor

		/**
		pseudo code:

		def trigger():
			write(High, trigger)

		def get_echo_state():
			echo_state = RTDACUSBBuffer.GetOutPut
			return echo_state

		def get_echo_width():

			int counter, distance, speed_of_sound
	
			if echo == High:
				while get_echo_state() == High:
					counter++

			distance = counter/speed_of_sound
			return distance

		**/

		//printf("%d", distance);
		USBClose();
	}
}

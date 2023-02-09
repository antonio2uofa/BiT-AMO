#include "ballsInTubesForML.h"
#include <stdio.h>

int main() {

	unsigned int num_of_tubes = 4;
	unsigned int loop;
	short unsigned int fan_speeds[] = {0, 0, 0, 0};
	short unsigned int *ptr = fan_speeds;

	BallsReadFanSpeedDll(fan_speeds, num_of_tubes);

	for(loop = 0; loop < 4; loop++) {
		printf("%d ", *ptr);
		ptr++;
	}

	return 0;
}
import serial

ser = serial.Serial(
	'COM4',
	9600,
	timeout=0,
	parity=serial.PARITY_NONE
	)

while(True):

	if(ser.in_waiting > 0):
		serialString = ser.read()
		print(serialString)
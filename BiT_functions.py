from subprocess import run
import sys

#------------------------------------------------------------------------#
#	Functions Used to Connect to USB and Initialize Pin Functions		 #
#------------------------------------------------------------------------#

def usb_open():
	run("./cfiles/usb_open")

def usb_close():
	run("./cfiles/usb_close")

def init_bit():
	run("./cfiles/init_bit")

#------------------------------------------------------------------------#
#	Functions Used to Process Output from C Executables					 #
#------------------------------------------------------------------------#

def text_processor(subp_output):
	output_text = subp_output.stdout.decode()

	if output_text == '':
		print("Cannot detect any USB devices.\n")
		return

	text_arr = output_text.split(",")
	output_dict = {
	'mode':int(text_arr[0]),
	'prescaler':int(text_arr[1]),
	'width':int(text_arr[2]),
	}

	return output_dict

def int_processor(subp_output):
	output_text = subp_output.stdout.decode()

	if output_text == '':
		print("Cannot detect any USB devices.\n")
		return

	output_val = int(output_text)

	return output_val

#------------------------------------------------------------------------#
#	Functions Used to Monitor and Control Fanspeed					 	 #
#------------------------------------------------------------------------#

def get_fanspeed(tube_num):
	executable = "./cfiles/get_fanspeed_" + str(tube_num)
	output = run(executable, capture_output=True)
	fan_data = text_processor(output)

	return fan_data

def set_fanspeed(tube_num, level):
	executable = "./cfiles/set_fanspeed_" + str(tube_num)
	max_width = 4095
	level = round((level/100)*max_width)
	level = str(level)
	run(executable, input=level, text=True)

#------------------------------------------------------------------------#
#	Function Used to Get Level of the Ball in a Specified Tube			 #
#------------------------------------------------------------------------#

def get_level(tube_num):
	executable = "./cfiles/get_level_" + str(tube_num)
	output = run(executable, capture_output=True)
	level = int_processor(output)
	
	return level
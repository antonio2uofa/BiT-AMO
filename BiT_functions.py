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

def array_processor(subp_output):
	output_text = subp_output.stdout.decode()

	if output_text == '':
		print("Cannot detect any USB devices.\n")
		return

	fanspeed_array = [int(speed) for speed in output_text.split()]

	return fanspeed_array

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

def set_fanspeed(tube_num, level):
	executable = "./cfiles/set_fanspeed_" + str(tube_num)
	max_width = 4095
	level = round((level/100)*max_width)
	level = str(level)
	run(executable, input=level, text=True)

def set_fanspeeds(fan_4, fan_3, fan_2, fan_1, normalized=False):
	fanspeeds = [fan_4, fan_3, fan_2, fan_1]
	executable = "./cfiles/set_fanspeeds"
	max_width = 4095
	if(normalized):
		scaled_vars = [round(speed * max_width) for speed in fanspeeds]
	else:
		scaled_vars = [round((speed / 100) * max_width) for speed in fanspeeds]
	scaled_vars = [str(speed) for speed in scaled_vars]
	speeds = ' '.join(scaled_vars)
	byte_speeds = speeds.encode('utf-8')
	run(executable, input=byte_speeds)

#------------------------------------------------------------------------#
#	Function Used to Get Level of the Ball in a Specified Tube			 #
#------------------------------------------------------------------------#

def get_level(tube_num):
	executable = "./cfiles/get_level_" + str(tube_num)
	output = run(executable, capture_output=True)
	level = int_processor(output)
	
	return level

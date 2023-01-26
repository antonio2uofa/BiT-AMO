from subprocess import run
import sys

def usb_open():
	run("./usb_open")

def usb_close():
	run("./usb_close")

def init_bit():
	run("./init_bit")

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

def get_fanspeed(tube_num):
	executable = "./get_fanspeed_" + str(tube_num)
	output = run(executable, capture_output=True)
	fan_data = text_processor(output)

	return fan_data

#------------------------------------------------------------------------#

def set_fanspeed(tube_num, level):
	executable = "./set_fanspeed_" + str(tube_num)
	level = str(level)
	run(executable, input=level, text=True)

#------------------------------------------------------------------------#

def get_level(tube_num):
	executable = "./get_level_" + str(tube_num)
	output = run(executable, capture_output=True)
	level = int_processor(output)
	
	return level
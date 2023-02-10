from pywrapper import *

if __name__ == "__main__":
	c_lib = load_bit()
	delay_millis(c_lib, 5000);
	initialize_bit(c_lib)

	for x in range(3):
		print("Starting...")
		set_fan_speed(c_lib, 0, 2)
		delay_millis(c_lib, 10000)
		print(get_level_3(c_lib))
		#set_fan_speed(c_lib, 30, 1)
		#delay_millis(c_lib, 2000)
		#set_fan_speed(c_lib, 30, 2)
		#delay_millis(c_lib, 2000)
		#set_fan_speed(c_lib, 30, 3)
		#delay_millis(c_lib, 5000)
		set_fan_speed(c_lib, 50, 2)
		delay_millis(c_lib, 10000)
		#set_fan_speed(c_lib, 50, 1)
		#delay_millis(c_lib, 3000)
		#set_fan_speed(c_lib, 50, 2)
		#delay_millis(c_lib, 3000)
		#set_fan_speed(c_lib, 50, 3)
		#delay_millis(c_lib, 3000)

		print(get_level_3(c_lib))
		#print(get_level_2(c_lib))
		#print(get_level_3(c_lib))
		#print(get_level_4(c_lib))

	print(close_usb(c_lib))
	unload_bit(c_lib)
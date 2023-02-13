import ctypes
import numpy as np
import bit_functions as bit
import matplotlib.pyplot as plt
 
path_name = './fanspeed_lv/ballsInTubesForML.DLL'

class FanSpeedWrapper:
	"""
	Wrapper class for loading BallsReadFanSpeedDll and retrieving a c-type
	array. Then converting it into an integer list of fan speed values.
	"""
	def __init__(self):
		self.c_lib = ctypes.cdll.LoadLibrary(path_name)
		self.c_type_arr = (ctypes.c_ushort * 4)()
		self.get_fan_speeds()
		bit.init_bit()

	def get_fan_speeds(self):
		self.c_lib.BallsReadFanSpeedDll(self.c_type_arr, ctypes.c_int(4))
		c_list = np.ctypeslib.as_array(self.c_type_arr)
		py_map = map(lambda x: x.item(), c_list)
		return list(py_map)

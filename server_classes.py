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
		self.get_fanspeeds()

	def get_fanspeeds(self):
		self.c_lib.BallsReadFanSpeedDll(self.c_type_arr, ctypes.c_int(4))
		c_list = np.ctypeslib.as_array(self.c_type_arr)
		py_map = map(lambda x: x.item(), c_list)
		return list(py_map)

	def setup_bit(self):
		bit.init_bit()
		bit.set_fanspeed(1, 100)

		for i in range(1, 5, 1):
			bit.get_level(i)

	def reset_bit(self):
		for i in range(2, 5, 1):
			bit.set_fanspeed(i, 0)


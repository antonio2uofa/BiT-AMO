import ctypes
import numpy as np
import time

path_name = './ballsInTubesForML_2017.DLL'

class FanSpeedsWrapper:
	def __init__(self):

		self.c_lib = ctypes.cdll.LoadLibrary(path_name)
		self.c_type_arr = np.ctypeslib.as_ctypes(np.zeros((1, 4), dtype=np.uint16))
		self.get_fan_speeds()

	def get_fan_speeds(self):
		self.c_lib.BallsReadFanSpeedDll(self.c_type_arr, ctypes.c_int(4))
		return np.ctypeslib.as_array(self.c_type_arr)[0]


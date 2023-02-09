import ctypes
import numpy as np
import time

path_name = './ballsInTubesForML_2017.DLL'

class FanSpeedsWrapper:
	def __init__(self):

		self.c_lib = ctypes.cdll.LoadLibrary(path_name)
		#self.c_type_arr = np.ctypeslib.as_ctypes(np.zeros((1, 4), dtype=np.uint16))
		self.c_type_arr = (ctypes.c_ushort * 4)()
		self.get_fan_speeds()

	def get_fan_speeds(self):
		self.c_lib.BallsReadFanSpeedDll(self.c_type_arr, ctypes.c_int(4))
		c_list = np.ctypeslib.as_array(self.c_type_arr)
		py_map = map(lambda x: x.item(), c_list)
		return list(py_map)





# start = time.time()
# c_lib = ctypes.cdll.LoadLibrary(path_name)
# py_values = np.ctypeslib.as_ctypes(np.zeros((1, 4), dtype=np.uint16))
arr = (ctypes.c_ushort * 4)()
print(arr)

# length = 4
count = 0
# c_lib.BallsReadFanSpeedDll(py_values, ctypes.c_int(length))
# print(time.time()-start)

# start_1 = time.time()
fanspeeds = FanSpeedsWrapper()
t1 = time.time()
while count < 1:
	mylist = fanspeeds.get_fan_speeds()
	mylist = list(map(lambda x: x.item(), mylist))
	print(type(mylist[0]))

	count += 1

t2 = time.time()
print(t2-t1)



#void __cdecl BallsReadFanSpeedDll(uint16_t FanSpeeds[], int32_t len);
